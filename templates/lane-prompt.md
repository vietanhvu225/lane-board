# Lane prompt

The Orchestrator fills in the `<…>` and uses the block as the prompt when starting a lane (orchestrator.md §Starting a lane).

```markdown
You are a lane of "{{PROJECT}} Orchestrator". Do exactly one ticket:

Ticket: .scratch/<effort>/issues/<NN>-<slug>.md
Type: <research | grilling | prototype | task | implement>
Initial title: <effort>-<NN> <short name>
Orchestrator id: <local_… id>
Scope: see the `Scope:` line in the ticket header (changing a file outside it → CHECK, or record it under `Process deviations`)
Merge: <after the Orchestrator says "ok to merge" | needs GATE>. A checker subagent of your own passing is not "ok to merge".

Read first, in order:
1. CLAUDE.md
2. docs/orchestration/lane.md (your role)
3. docs/orchestration/contract.md (title, tags, stop points, merge)
4. docs/agents/workflow.md §1–§4 (skills, artifacts, criteria, session record)
5. The ticket file above

<Optional: gitignored files you need are not in your worktree; read them by absolute path in the main checkout, read-only: <path>>
```
