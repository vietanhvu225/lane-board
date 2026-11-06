# Phase briefs

What the CTO hands the Orchestrator, phase by phase. Each phase is one **effort** (`.scratch/<effort>/`, e.g. `p0`, `p1`). Ticket type → skill → artifact → criterion: [workflow.md](../agents/workflow.md) §2, not repeated here.

Tickets listed here are **drafts**. The real tickets are made by the phase's chart lane in `.scratch/<effort>/`; when they differ, `.scratch/` wins.

Phase state lives only in the `Status:` line at the top of `.scratch/<effort>/map.md` (e.g. `Status: closed 2026-11-04`). This file holds briefs, not state.

---

## Overall schedule

```
p0 <name> ─┐
           ├─► p2 <name> ─► p3 <name>
p1 <name> ─┘
```

- Which phases run in parallel and why (e.g. a HITL-heavy phase next to an AFK-heavy one, so the machine works while the user is busy).
- Entry dependencies between phases.
- Each phase opens with a **chart lane**: the user runs `/mattpocock-skills:wayfinder` (planning phases) or `/mattpocock-skills:to-spec` + `/mattpocock-skills:to-tickets` (build phases) in that lane, with the draft below as input.

---

## p0: <name>

**Goal.** <what is known or built when this phase closes, in one or two sentences>

**Entry gate.** <phases or decisions this needs; or "none">

**Draft tickets** (map destination: *<one line>*):

| NN | Ticket | Type | HITL/AFK | Blocked by |
|---|---|---|---|---|
| 01 | <…> | research | AFK | — |
| 02 | <…> | grilling | HITL | 01 |

**Parallel.** <which tickets run at once, respecting at most 1 HITL lane>

**Exit gate.**
- <checkable criterion>
- <checkable criterion>

**Stop criterion** (optional). <what result would stop or reshape the project>
