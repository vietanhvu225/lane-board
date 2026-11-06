# Why the rules look like this

Each rule below changed because something went wrong (or right) in the project these rules came from. Dates are when it happened, November 2026.

| Rule | What happened | Where now |
|---|---|---|
| CTO and Orchestrator are two top-level peers | A CTO starting the Orchestrator as its child would make lanes grandchildren and wake the CTO on every Orchestrator turn | README §Sessions |
| Session titles in plain ASCII | Titles are matched as strings when sending by title; accented letters can differ by Unicode form | contract §2 |
| Send by `local_…` id by default | Sending by title failed three times (lane → Orchestrator twice, Orchestrator → CTO once); by id it always arrived | contract §4 |
| A lane stops with `CHECK` for user-only skills | A lane prompt starting with `/…:wayfinder` did not run the skill (`disable-model-invocation`) | contract §3, chart lane prompt |
| Lane ledger `lanes.md` | A chart lane has no ticket, so there was nowhere to claim it | contract §5 |
| Claim when proposing the card | A clicked card starts the lane at once, before the Orchestrator's claim commit; the lane then hit a conflict on `Status:` | contract §5, orchestrator.md |
| No branch naming convention | The app names branches itself; cards drop `branch_name` | contract §6 |
| One pending HITL card at a time | The user clicked two pending HITL cards and got two HITL lanes | contract §7 |
| Trailers in the same last paragraph | A blank line between `Ticket:` and `Co-Authored-By:` made git drop the trailers | workflow §4 |
| Session record fields `Check:`, `Tokens:` | After the first overnight run, check traces were uneven between lanes and nothing measured cost | workflow §3 |
| `check_ticket.py` | The first retro found no automatic check at all: missing trailers, records, check traces and out-of-scope edits were only caught by eye | workflow §5 |
| `--rev` reads the ticket from the branch | Run from main, an early checker read main's `claimed` copy and passed a lane whose record lacked a field | tools/check_ticket.py |
| Deleted artifacts only warn | A later ticket deleted an earlier prototype by decision; the checker flagged the old ticket | tools/check_ticket.py |
| Yolo mode: worker lanes | `start_session` is refused on automated turns, and the classifier refused a third start in a row, so a night's batch can't start new lanes midway | contract §10 |
| Checker subagent reads `Done when` and samples 3 files | The first overnight run passed 104 files lacking the source citation the ticket required; the checker had only run the generic steps | contract §10 |
| Worker lanes run tickets sequentially | Checking ticket N while doing N+1 in one worktree mixed files into the wrong commits | contract §10 |
| Ignore worker-lane notes unless `DONE` / `CHECK` | A lane waiting on background subagents sent about 15 turn-end notes a night | contract §10, claude-desktop.md |
| Lanes in one stopped queue don't stop the others | The user wanted this explicit after the first yolo run | contract §10 |
| Token estimate per ticket in proposals | The user liked seeing the budget a batch would spend before approving it | orchestrator.md |
| Glossary ticket after ≥ 10 tickets | Lanes in a batch may not edit `GLOSSARY.md`, so terms piled up in session records | orchestrator.md |
| All fix requests in one message | A second message to a lane mid-turn queued, and the lane reported done before applying it | orchestrator.md, claude-desktop.md |
| "A checker subagent passing is not ok to merge" | An overnight lane read "self-check with a subagent" as permission and merged before the Orchestrator's check | lane.md, lane prompt |
| Checks listed by path touched | A project added a build step that every code-touching lane had to run before merge | contract §6, workflow §5 |
| Criteria planned for data without lines | "Cite file:line" could not be met for binary data, found only after the batch | workflow §5 |
| Compare reruns with `--check` / `git diff`, not hashes | `core.autocrlf=true` changed line endings on the main checkout | workflow §5 |
| Handover with "Open lanes" and ids | The first Orchestrator handover worked end to end: the new Orchestrator checked in with the CTO by id | orchestrator.md, templates/handover.md |
