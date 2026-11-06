# Changelog

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
