# Claude Desktop: app behaviour

How the board runs in the Claude Desktop app (Code tab): the CTO and the Orchestrator are top-level sessions, each lane is a child session of the Orchestrator. The rules in [contract.md](contract.md) rely on the points below.

Each point is labelled:

- **Observed**: seen in a real session. The source is the project these rules were extracted from (November 2026, Claude Code 2.1.x) unless said otherwise.
- **Assumed**: from a tool description or reasoning, not tried.
- **To verify**: nobody has checked yet. Check it on your first run and log the answer in the board diary.

The app changes. When your project sees something different, log a `[general] [Observed]` diary entry and fix this file.

---

## Starting lanes: `start_session`

- `start_session` is refused on a turn started by an automated event or by another session's message. It is not turned into a card. **Observed.** So on such turns the Orchestrator only proposes a card (`initiation: "own_initiative"`) and the user clicks it.
- A turn that started from a lane's message but where the user sent a message mid-turn counts as the user's turn: `start_session` with `user_asked` worked. **Observed.**
- Starting several sessions in a row can be refused by the auto-mode classifier with no reason given (the third start in a row was refused). **Observed.** Ask the user before a third start in a row; never retry by another route.
- A card the user clicks starts the lane at once. **Observed.** So the Orchestrator claims the ticket on main before proposing the card (contract §5).
- The app does not enforce capacity: the user can click two pending HITL cards and get two HITL lanes. **Observed.** Hence "one pending HITL card at a time" (contract §7).
- Branch names: a lane started by `start_session` gets `claude/<slug>-<suffix>`; a lane started from a card gets a random name, and `branch_name` is dropped. **Observed.** Set no branch convention; record the real branch in the lane ledger.
- A lane can't be moved to a new parent. Lanes that live for days stay under the old Orchestrator; the new one messages them by id. **Assumed.**

## User-only skills

- A lane prompt that starts with a slash command does **not** run a skill marked `disable-model-invocation: true` (`/mattpocock-skills:wayfinder`, `to-spec`, `to-tickets`, `implement`, `retro`, `handoff`, `setup-matt-pocock-skills`, …). **Observed.** The user must type the command inside the lane; the lane stops with `CHECK` and gives the exact command (contract §3).

## Titles: `set_session_title` on `"self"`

- A lane sets its own title on `"self"` and it changes without asking the user. **Observed.**
- The tool says the app asks the user to approve when the current title was set by the user. **Assumed** (from the tool description).
- The sidebar cuts titles by pixel width, around 55 characters at default width. **Observed.** Keep the short name ≤ 25 characters; the tag stays first.

## Messages: `SendMessage`

- Sending by **title** usually arrives, but failed three times across lane → Orchestrator and Orchestrator → CTO, apparently after a session process restarted (the session's ref in `ListAgents` had changed). **Observed.** Sending by **`local_…` id** always arrived. **Observed.** Hence "send by id by default" (contract §4).
- The receiver sees `from-name` (the sender's current title, tag included) and `from-session` (its `local_…` id), so it can reply by id. **Observed.**
- A second message sent to a lane while it is mid-turn can be queued, and the lane may report done before acting on it. **Observed.** Put every request in one message.

## Turn-end notes

- When a child ends a turn, the parent gets a note with the first 400 characters of the child's report, and the app wakes the parent if it is idle. **Observed.** So a lane's report opens with `<title> — <what it needs>`.
- A lane waiting on background subagents ends its turn many times, and each one sends a note (about 15 a night for one worker lane). It can't be suppressed. **Observed.** The Orchestrator ignores worker-lane notes unless they open with `DONE` or `CHECK` (contract §10).
- Every lane turn wakes the Orchestrator, so its transcript grows fast with 3 lanes. **Assumed.** Hand over when it gets long.

## Shared notes folder

- Every child session gets a shared notes folder keyed by its parent's id (e.g. `…\Claude-Data\<profile>\side-session-notes\<parent local_id>`), named in the child's brief. The path differs by install: take it from the brief, never hard-code it. **Observed.**
- Lanes under different parents (old and new Orchestrator) don't share a folder. **Assumed** (the folder is keyed by parent id).
- Whether the folder survives the parent being archived: **To verify**.

## Session layout

- The CTO and the Orchestrator as two top-level peers, talking by id: works, including a full Orchestrator handover (old one writes the handover with the CTO's id, renames itself `(old) …`; the new one checks in with the CTO by id and gives its own id). **Observed.**
- Three levels (CTO starts the Orchestrator, which starts lanes as grandchildren): how the app handles it is **To verify**. Avoid it: keep the CTO and the Orchestrator top-level.
- Old lanes (children of a previous Orchestrator) sending to the new Orchestrator by id, and the old Orchestrator forwarding their turn-end notes: **To verify**.

## Subagent tokens

- A background subagent's completion notification carries a `subagent_tokens` figure. **Observed** (06/11/2026, outside the source project). Use it for the session record's `Tokens:` field; whether a foreground Agent call reports it too is **To verify**.

## Git worktrees

- Gitignored files are not in a lane's worktree. **Observed.** Give the lane their absolute path in the main checkout.
- `check_ticket.py` run from main with `--rev <lane branch>` must read the ticket from that branch, not from main's working tree: an early version read main's copy and passed a ticket whose record was incomplete. **Observed**, fixed in the shipped script.
