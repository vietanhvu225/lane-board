# Changelog

## 0.5.0 (2026-11-25)

- After a handover, old lanes only finish their work in progress; new tickets and new yolo queues go to new lanes the new Orchestrator starts; finished old lanes are archived when the user agrees; the old Orchestrator forwards notes until then (orchestrator.md §Handover, §Yolo mode step 4, handover template).
- Adapter: "a lane can't move to a new parent" is now Observed; old lanes' turn-end notes go to the old Orchestrator.

## 0.4.0 (2026-11-22)

From the source project's art-phase retro:

- No separate lane cap per area (contract §11).
- The checker subagent and the Orchestrator check look at ≥ 2 images when a conclusion rests on images (contract §10, workflow §5 step 6).
- Trailers are required on the commit that closes a ticket, and recommended on work-in-progress commits (workflow §4).
- A worker lane prepares the worktree's build dependencies before starting subagents (contract §10).

## 0.3.0 (2026-11-21)

- Several Orchestrators by area (contract §11, optional): each area has its own title, brief, effort range, folder and id line in the lane ledger; the ledger is shared; a shared file needs the other Orchestrator's word before a claim; no Orchestrator touches another area's efforts.
- Capacity (contract §7): the lane cap and the new exclusive-resource cap (one GPU, a single-client app) count across all Orchestrators; the HITL cap counts per Orchestrator.
- orchestrator.md speaks of `<title>`, `<brief>`, `<folder>` from an area table; the lane prompts name `<Orchestrator title>`; the chart lane reads its area's brief; the handover template lists the other area's Orchestrator; the lane ledger template has the Orchestrator's id line.
- Sending: when the Orchestrator's id fails, fall back to its latest message's `from`, then its id line in the lane ledger, then the title (contract §4).

## 0.2.0 (2026-11-07)

From the source project's second retro:

- An auto-mode block is a `CHECK` stop point; the Orchestrator merges for a lane only when auto mode blocked it and the user says so directly (contract §3, §6).
- Adapter: real classifier blocks vs the transient `gave no verdict (error)` (retry once); `subagent_tokens` observed in worker lanes; a lane with nothing running is woken by nothing.
- Worker lanes end a turn only while a background subagent runs, or at `DONE` / `CHECK`; the Orchestrator wakes an untagged lane quiet for over 30 minutes.
- The `Merge:` line of a lane prompt has exactly two values.
- `Done when` uses checks reachable inside the lane's scope; read a scanning script's exclusions before declaring scope in its folder.
- The Orchestrator hands over when a phase closes or after its first compaction.
- Batch token estimates use the previous phase's real-to-estimate factor.

## 0.1.0 (2026-11-06)

- First public version: board contract, Orchestrator and lane roles, templates, Claude Desktop adapter, `/lane-board:board-init`, `tools/check_ticket.py`. Extracted from a private project's rules at commit `92242cc`.
