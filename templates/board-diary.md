# Board diary

A log of what is **in no ticket**: how the app really behaves, where the process got stuck and how it was freed, why a rule changed. Who did what is already in `git log`, `.scratch/` and `docs/adr/`; don't copy it here.

## Who writes, when

| Who | When |
|---|---|
| Orchestrator | a **To verify** item gets an answer; the process got stuck or had to break a rule; handover; phase closed |
| CTO | every change to `docs/orchestration/` or `docs/agents/workflow.md` (usually after `/mattpocock-skills:retro`) |

## Entry template

```markdown
### <YYYY-MM-DD> [general|project] [Observed|To verify|Rule change|Stuck|Handover|Phase closed] <short title>
- What: <1–2 lines>
- Evidence: <ticket, session, commit, screenshot>
- Consequence: <which file changes / which ticket opens / nothing>
```

- `[general]`: true for any project using this model; worth sending upstream to the lane-board plugin. `[project]`: true only here.
- `[Observed]`: the answer to a **To verify** item → update its label in [claude-desktop.md](claude-desktop.md).
- `[Rule change]`: record the reason; the diff is in the commit.

---

## Log

### {{DATE}} [project] [Rule change] Set up the board
- What: `/lane-board:board-init` installed the orchestration rules ({{SOURCE}}).
- Evidence: the commit that adds `docs/orchestration/`.
- Consequence: check the **To verify** items in claude-desktop.md on the first run.
