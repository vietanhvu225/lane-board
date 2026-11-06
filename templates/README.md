# Orchestration

How this project runs several sessions in parallel: one **Orchestrator** coordinates, each **lane** (child session) does exactly one ticket. Installed by the lane-board plugin ({{SOURCE}}) on {{DATE}}; from here on these files belong to this project and change through `/mattpocock-skills:retro`.

---

## Three levels

Each level reuses the one below; none replaces it.

| Level | Covers | Answers | Where |
|---|---|---|---|
| **Workflow** | 1 ticket | which skill for which ticket type, what artifact, when done | [docs/agents/workflow.md](../agents/workflow.md) |
| **Board** | many tickets in parallel within a phase | how lanes start, report, stop, merge | [contract.md](contract.md), [orchestrator.md](orchestrator.md), [lane.md](lane.md) |
| **Roadmap** | the whole project | which phases, goals, entry/exit gates, first tickets | [phases.md](phases.md) |

## Roles

| Role | Who | Does | Doesn't |
|---|---|---|---|
| **User** (product owner) | you | decides; starts lanes; answers CHECK; approves GATE; does PLAY by hand; types the `/` skills | — | <!--play-->
| **User** (product owner) | you | decides; starts lanes; answers CHECK; approves GATE; types the `/` skills | — | <!--noplay-->
| **CTO** | top-level session **`{{PROJECT}} CTO`** | writes and fixes these rules, the phase briefs, ADRs; takes `/retro` results to fix the process | doesn't run lanes or coordinate day to day |
| **Orchestrator** | top-level session **`{{PROJECT}} Orchestrator`** | picks frontier tickets, proposes lanes, claims tickets, checks finished lanes per workflow §5, writes Decisions-so-far, reports to the user, hands over when its transcript is long | doesn't do a lane's work, doesn't answer a CHECK, doesn't merge for a lane |
| **Lane** | child session of the Orchestrator | does 1 ticket per workflow.md, keeps its title on its state, stops at the right stop points, merges when allowed | doesn't take a second ticket, doesn't edit the tracker beyond its own ticket |

## Sessions

```
{{PROJECT}} CTO            (top level: plans, changes rules)
{{PROJECT}} Orchestrator   (top level: coordinates)
   ├── lane <effort>-<NN> …   (child sessions, started by the Orchestrator)
   └── …
```

- The CTO and the Orchestrator are two top-level peers. Don't let the CTO start the Orchestrator as its child: lanes would become grandchildren, and every Orchestrator turn would wake the CTO.
- Lanes are always started by the Orchestrator. A lane you start by hand is not its child, so the Orchestrator gets none of its turn-end notes.
- The CTO and the Orchestrator talk mostly through files: the Orchestrator writes [board-diary.md](board-diary.md) and `.scratch/_orchestrator/retro-inbox.md`; you carry `/retro` results to the CTO; the CTO fixes the rules and writes the diary. Direct messages only for a few things (orchestrator.md §Talking to the CTO), starting with the check-in.
- The CTO writes the first handover (`.scratch/_orchestrator/handover-<date>.md`, from [templates/handover.md](templates/handover.md)) with its own title and id, so the Orchestrator knows whom to message.

## Start

1. **Set up** (done by `/lane-board:board-init`). Then type `/mattpocock-skills:setup-matt-pocock-skills` and pick **Local markdown** as the issue tracker.
2. **Open the CTO.** A new session titled `{{PROJECT}} CTO`:
   > You are the CTO of {{PROJECT}}. The orchestration rules are in docs/orchestration/. With me: brainstorm, write the roadmap and docs/orchestration/phases.md, fill in docs/agents/workflow.md §2 and §5 for this project, confirm README §Operating decisions, then write the first handover in .scratch/_orchestrator/.
3. **Open the Orchestrator** once `phases.md` and the first handover exist. A new session titled `{{PROJECT}} Orchestrator`:
   > You are {{PROJECT}} Orchestrator. Read docs/orchestration/orchestrator.md and follow it.
4. **Day to day.** The Orchestrator proposes lanes, you click to start them. When a lane shows `CHECK` / `GATE` / `PLAY`, go into that lane. End of a phase: `/mattpocock-skills:retro`, carry the result to the CTO. <!--play-->
4. **Day to day.** The Orchestrator proposes lanes, you click to start them. When a lane shows `CHECK` / `GATE`, go into that lane. End of a phase: `/mattpocock-skills:retro`, carry the result to the CTO. <!--noplay-->
5. **Long transcripts.** The Orchestrator hands over by itself when a phase closes or after its first compaction (orchestrator.md §Handover). For the CTO, open a new CTO session:
   > You are the CTO of {{PROJECT}}. Read CLAUDE.md, docs/adr/ and docs/orchestration/board-diary.md for context.

   or run `/mattpocock-skills:handoff` in the old CTO session.

## Read in this order

1. [contract.md](contract.md): shared rules (titles and tags, stop points, reports, claims, merge, capacity, yolo mode).
2. [orchestrator.md](orchestrator.md), [lane.md](lane.md): each role step by step.
3. [claude-desktop.md](claude-desktop.md): how the app behaves (Observed / Assumed / To verify).
4. [phases.md](phases.md): each phase's goal, gates, first tickets.
5. [docs/adr/](../adr/): settled decisions.

---

## Operating decisions

Defaults from the plugin. The CTO confirms them with the user and records the date.

1. **Merge.** Tickets touching only docs / tracker paths: the lane merges after the Orchestrator's check passes, no GATE. Tickets touching code: user GATE (after PLAY passes) before merge. Paths per kind: workflow.md §5. <!--play-->
1. **Merge.** Tickets touching only docs / tracker paths: the lane merges after the Orchestrator's check passes, no GATE. Tickets touching code: user GATE before merge. Paths per kind: workflow.md §5. <!--noplay-->
2. **Capacity.** At most 3 lanes at once; at most 1 HITL lane (and 1 pending HITL card) at once, so you aren't asked questions from several sides.
3. **One wayfinder map per phase.** Each phase is one effort (`p0`, `p1`, …), rather than one big map.
4. **Parallel phases.** Pair a HITL-heavy phase with an AFK-heavy one when they don't depend on each other.

Confirmed by the user: <date, quote>
