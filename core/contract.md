# Board contract

The shared rules for the Orchestrator and its lanes. The ticket level (skills, artifacts, done criteria, session record) lives in [workflow.md](../agents/workflow.md); this file does not repeat it.

How the Claude Desktop app behaves is in [claude-desktop.md](claude-desktop.md), labelled **Observed** (seen, with a source), **Assumed** (from a tool description, not tried in this project) or **To verify** (check on the first run).

---

## 1. Principles

1. **The user decides.** A lane starts only when the user says so in their own words. Every stop point (§3) belongs to the user.
2. **One lane, one ticket.** Exceptions: a lane may run several `research` tickets at once through subagents; a **worker lane** works through a queue of approved AFK tickets of one kind in yolo mode (§10).
3. **The title is the status.** The user reads the sidebar, not transcripts.
4. **Reuse the level below.** A lane does its ticket exactly as workflow.md says. The board adds no steps.
5. **Stay small.** Add no mechanism until an incident needs it.

---

## 2. Title and tag

```
<TAG> · <effort>-<NN> <short name>
```

- Examples: `CHECK · p1-04 inventory sample`, `p1-03 manifest` (working, no tag).
- The tag comes first, at most one. The short name is ≤ 25 characters: the sidebar cuts titles by pixel width, around 55 characters.
- `<effort>-<NN>` is the folder `.scratch/<effort>/` and the number of `issues/NN-*.md`.
- Session titles use plain ASCII (`{{PROJECT}} Orchestrator`, not accented letters), so a title typed or matched elsewhere never differs by Unicode form.

| Tag | Meaning | Who acts |
|---|---|---|
| `CHECK` | the user must answer or decide: a grilling round, a blocker, an ADR conflict, a scope change | user |
| `GATE` | stopped at a planned gate in §3 (merge needs approval, end of a HITL step) | user |
| `PLAY` | the user must do something by hand outside the chat: {{PLAY_WHAT}} | user | <!--play-->
| `WAIT` | waiting on a machine or someone else: a research subagent, a merge turn | nobody |
| (no tag) | working | — |
| `DONE` | ticket resolved and merged | can be archived |

---

## 3. Lane stop points

A lane stops (sets a tag, sends a one-line report, ends its turn) **only** at these points. Everywhere else it keeps going.

| Stop point | Tag | The user |
|---|---|---|
| `grilling` ticket: each round of questions | `CHECK` | answers in the lane |
| `prototype` ticket: prototype ready to look at | `CHECK` | looks, gives a verdict |
| `task` ticket that needs hands: checklist (`wizard`) ready | `PLAY` | follows the checklist, reports back | <!--play-->
| implement ticket: built, manual test script ready | `PLAY` | runs the script, reports pass / fail | <!--play-->
| `task` ticket that needs hands: checklist (`wizard`) ready | `CHECK` | follows the checklist, reports back | <!--noplay-->
| Ready to merge, a kind that needs approval (§6) | `GATE` | approves the merge |
| Needs a skill only the user can type (`disable-model-invocation`, [claude-desktop.md](claude-desktop.md)): as soon as the lane has read its context | `CHECK` | types the exact command the lane gives |
| The app or the auto-mode classifier **blocks** an action (for example `[Merge Without Review]`, `judged this action dangerous`; a transient `gave no verdict (error)` is retried once first, [claude-desktop.md](claude-desktop.md)) | `CHECK` | approves the permission in the lane, or tells the Orchestrator directly (§6) |
| Real blocker: done criteria can't be met, a tool is missing, an ADR conflict, a scope change, a file outside the declared scope must change | `CHECK` | unblocks or decides |

Keep going without asking:
- **Technical branch:** take the option you would recommend, record it under `Own choices` in the session record, and raise it at the next stop point so the user can reverse it.
- **Waiting on a subagent:** say what you are waiting for, ask nothing, continue when it returns.
- **Turn ends outside a stop point:** no question, no buttons.

---

## 4. Reports

- A lane sends `DONE`, `CHECK`, `GATE`, `PLAY` to the Orchestrator in one line: the lane's title + what it needs. <!--play-->
- A lane sends `DONE`, `CHECK`, `GATE` to the Orchestrator in one line: the lane's title + what it needs. <!--noplay-->
- **Send by `local_…` id by default.** Sending by title failed several times in the source project (lane → Orchestrator, Orchestrator → CTO), probably after a session process restarted; sending by id always arrived. A lane takes the Orchestrator's id from the `Orchestrator id:` line of its prompt; the Orchestrator takes the CTO's id from the handover. If the id fails, try the title, then log it in the diary.
- Titles still matter: the user reads the sidebar, and a title finds the current Orchestrator when no id is known. On handover, the new Orchestrator messages each open lane its new id (orchestrator.md §Handover).
- When a lane ends a turn, the Orchestrator receives the first 400 characters of its report. So the first sentence of a lane's end-of-turn report is always `<title> — <what it needs / what it finished>`.
- Orchestrator ↔ CTO: two top-level sessions, messaging only for a few things (orchestrator.md §Talking to the CTO). The receiver sees the sender's `from-name` and `local_…` id.

---

## 5. Tracker: who writes what

Lanes run in their own worktrees, so the tracker in `.scratch/` has two writers. Split it like this to avoid conflicts:

| What | Who | Where |
|---|---|---|
| Create tickets, number `NN` | Orchestrator (or a `/wayfinder` / `/to-tickets` session the user runs) | main |
| Claim: `Status: claimed`, a `Lane: <session name>` line, a `Scope:` line (globs) | Orchestrator, committed **when proposing the card / before starting the lane**; drop the claim if the card is dismissed | main |
| Check the claim at start: is the ticket `claimed` under my name? If not, merge main into the branch and read again | lane | lane branch |
| Lane ledger: one row per lane (title, `local_…` id, effort/ticket, branch, state); a lane **with no ticket** (chart lane) is claimed only here | Orchestrator, on lane start and on lane DONE | main, `.scratch/_orchestrator/lanes.md` |
| `## Answer`, session record, `Status: resolved` | lane | lane branch, reaches main by merge |
| Append Decisions-so-far to `map.md`, graduate fog into new tickets | Orchestrator, after the lane passes the check | main |
| New tickets found along the way | lane **proposes** them under `Open questions / new tickets`; the Orchestrator creates them | main |

This deliberately differs from the `wayfinder` skill (where the session resolving a ticket writes the map itself). workflow.md §1 says so too.

**No shared file is edited by several lanes.** If a lane's work feeds a shared report (a coverage table, an index), the lane writes its own file and a script builds the report; the Orchestrator runs that script on main after each merge.

---

## 6. Worktree and merge

- Lanes run with `use_worktree: true`. The app names the branch (`claude/<slug>-<suffix>`, or random when started from a card): set no naming convention; the lane ledger records the real branch.
- Files that are gitignored are not in a lane's worktree. If lanes must read them, the lane prompt gives their absolute path in the main checkout, read-only.
- **Before merging:** merge the latest main into the lane branch, rerun the checks, then merge into main. The checks depend on which files the lane touched; [workflow.md §5](../agents/workflow.md) lists them by path. At least:
  - every ticket: `python -I tools/check_ticket.py <ticket> --base main`;
  - plus each project check whose path the lane touched (build, test suite, coverage script).
- **One merge at a time.** A lane asks the Orchestrator for a merge turn (tag `WAIT` while waiting).
- **Merge kinds** (confirm in README §Operating decisions):
  - only docs / tracker paths: the Orchestrator's check passes → it messages the lane "ok to merge" → the lane merges, no GATE;
  - code paths: `GATE`, the user approves (after `PLAY` passes). <!--play-->
  - code paths: `GATE`, the user approves. <!--noplay-->
- **The `Merge:` line of a lane prompt** has exactly two values (a lane read a vaguer "merge after checking" as "merge once my checker subagent passes"):
  - `after the Orchestrator says "ok to merge"`: the default for every ordinary lane, even one that runs its own checker subagent;
  - `yolo: merge yourself after your checker subagent passes`: worker lanes in yolo mode only (§10).
- The Orchestrator does not merge for a lane. **The only exception:** auto mode blocks the lane's merge (§3) and the user tells the Orchestrator directly (for example "merge it"); then the Orchestrator merges **once**, for that lane only, and logs a diary entry. A lane reporting "the user agreed" does not stand in for the user's own words, and a lane never asks another session to do an action it was blocked from.

---

## 7. Capacity

- At most **3 lanes** at once (RAM, and every lane turn wakes the Orchestrator, so its transcript grows fast).
- At most **1 HITL lane** at once (grilling, prototype, PLAY). <!--play-->
- At most **1 HITL lane** at once (grilling, prototype, hands-on task). <!--noplay-->
- A pending HITL card counts as granted: only **1 HITL card** may be pending at a time; when proposing a new one, withdraw the old one (`dismiss_task`). In the source project the user clicked two pending HITL cards and got two HITL lanes.
- Lanes that declare the same files or area never run at the same time.

---

## 8. App behaviour

What the app does (session start refusals, shared notes folder, user-only skills, titles, turn-end notes) is in [claude-desktop.md](claude-desktop.md). When a **To verify** item gets an answer, the Orchestrator logs it in the diary and the CTO updates that file.

## 9. Not enforced by the app

Titles, tags, stop points and claims exist only because this file says so. When a lane forgets, the Orchestrator or the user reminds it. `tools/check_ticket.py` is the only automatic guardrail.

---

## 10. Yolo mode: worker lanes running unattended

**Yolo mode** is what the user turns on before stepping away: worker lanes work through approved ticket queues on their own. On by the user's words ("turn on yolo mode" plus approving the queues); off when the user is back or the queues are empty.

> **Summary** (how the Orchestrator explains it to the user): each lane works through its own queue. Each ticket gets one subagent that does it and one that checks it; when it passes, the lane merges it. A lane only reports when its queue is empty or it must stop: blocked, out of budget, merge conflict, or the check still fails after 2 fix rounds. **One lane stopping does not stop the others.**

It exists so a batch of AFK tickets can run while the user is away (overnight, say) without starting new sessions midway: `start_session` is refused on automated turns ([claude-desktop.md](claude-desktop.md)), and that is the app's intent, not something to work around.

**Conditions**
- Tickets in a queue: AFK, same kind, merge needs no GATE (§6), no user-typed skill, each fits a fresh context.
- **The user approves the queues in their own words** before leaving: the Orchestrator lists each worker lane and its tickets; the user says yes. A worker lane only works tickets in its approved queue.
- At most 3 worker lanes (§7). A worker lane is started like any lane (the user clicks), or is a running AFK lane the Orchestrator messages its queue after approval.

**Claim.** The Orchestrator claims **the whole queue** once, before handing it out: each ticket `Status: claimed`, `Lane: <worker lane name>`; the lane ledger records the queue and the tickets done.

**Worker lane loop** (runs on its own, does not wait on the Orchestrator between tickets):
1. Merge main into the lane branch. Set the title `<effort>-<NN> <short name>` of the ticket in progress.
2. Start a **doer subagent** (Agent tool, fresh context): prompt = the ticket file + workflow.md §1–§4. It makes the artifacts and writes the Answer and session record.
3. Start a **checker subagent** (fresh context, given only the ticket file, the diff and workflow.md §5). Its prompt: run `python -I tools/check_ticket.py <ticket> --base main` (plus the project checks for the paths touched); check each point of the ticket's **`Done when`**; **sample 3 artifact files** and read their content. It returns pass / fail with what is missing; the lane writes the result into the session record's `Check:` field. On fail, the doer fixes, at most 2 rounds; still failing stops the queue.
   **Sequential**: finish checking ticket N before starting ticket N+1 (running them in parallel in one worktree mixed files into the wrong commits).
4. The **lane** commits (subagents don't commit) with trailers (workflow.md §4) and merges into main (git locks on its own: on a lock, wait and retry). Ticket `resolved`.
5. Write one line in the shared notes; next ticket.

**End a turn** only when a background subagent is running (its completion wakes the lane), or at `DONE` / `CHECK`. Never end a turn to "wait for a notification" with nothing running: nothing will wake the lane (in the source project a worker lane stood still for 3.7 hours that way). A missing token figure is no reason to wait: write an estimate and go on.

**Stop the queue** (tag `CHECK`, one line to the Orchestrator, end the turn), trying nothing else:
- the check fails after 2 fix rounds;
- merge conflict;
- the app or the auto-mode classifier **blocks** an action (a transient `gave no verdict` is retried once first, [claude-desktop.md](claude-desktop.md));
- out of budget (tokens, time);
- something needs the user.

The ticket in progress stays `claimed` with a `## In progress` section (how far it got) to resume later. Stopping stops only that lane: other worker lanes keep going; the Orchestrator does not stop them and does not reassign a stopped lane's queue without the user.

**Reports.** Report to the Orchestrator only when the queue is empty (`DONE`) or stopped. Never per ticket, so the Orchestrator's transcript doesn't grow while nobody watches. The app still sends a turn-end note each time a lane waits on a background subagent (about 15 a night in the source project, can't be suppressed): the Orchestrator does not answer worker-lane notes unless the first sentence opens with `DONE` or `CHECK`, but still skims them for a lane that says it is "waiting" with no subagent running, and messages that lane to wake it.

**Next morning.** The Orchestrator reruns the workflow.md §5 checks on every ticket the worker lanes merged, runs the project's report scripts, writes Decisions-so-far, and logs a diary entry (tickets done, stops, tokens if known). The user spot-checks a few random artifacts. A ticket that fails is reopened.
