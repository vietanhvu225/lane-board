# Lane ledger

One row per lane. The Orchestrator writes it when a lane starts and when it is DONE (contract §5). A lane with no ticket (chart lane) is claimed only here. Shared by every Orchestrator (contract §11).

Orchestrator: (the Orchestrator writes its `local_…` id here when it checks in)
<!-- With several areas, one id line per area, e.g. `Orchestrator (art): local_…` (contract §11). -->

| Title (as in the sidebar) | Session id | Effort / ticket | Branch | Started | State |
|---|---|---|---|---|---|
