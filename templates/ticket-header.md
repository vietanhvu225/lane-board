# Ticket header

Project convention on top of `docs/agents/issue-tracker.md` (local markdown, written by `/mattpocock-skills:setup-matt-pocock-skills`). `tools/check_ticket.py` reads it.

The header is the `Key: value` lines right under the `#` title, before the first `##` heading.

| Line | Value | Written by |
|---|---|---|
| `Type:` | `research` / `prototype` / `grilling` / `task` / `implement` (replaces the `wayfinder:<type>` label) | ticket creator |
| `HITL/AFK:` | `HITL` / `AFK` | ticket creator |
| `Status:` | `open` / `claimed` / `resolved` / `needs-info` / `wontfix` | creator; Orchestrator (claim); lane (resolved) |
| `Blocked by:` | `NN, NN` or `—` (replaces native blocking links) | ticket creator |
| `Lane:` | the session name of the lane holding the ticket | Orchestrator, when claiming |
| `Scope:` | globs in backticks, comma separated, e.g. `` `docs/research/*.md`, `GLOSSARY.md` `` | Orchestrator, when claiming (contract §5) |

Tickets live at `.scratch/<effort>/issues/<NN>-<slug>.md`; the ticket id is `<effort>-<NN>` (e.g. `p1-04`), used in titles and the `Ticket:` commit trailer.

A chart lane (no ticket beforehand) creates `issues/00-chart.md` for itself, `Status: resolved` when done, to hold its session record.

Example:

```markdown
# Pick the persistence layer

Type: grilling
HITL/AFK: HITL
Status: claimed
Blocked by: 02, 03
Lane: p1-04 persistence
Scope: `docs/adr/*.md`, `GLOSSARY.md`, `.scratch/p1/issues/04-*.md`

## Question
…

## Done when
…
```
