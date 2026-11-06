# Handover template

The Orchestrator writes `.scratch/_orchestrator/handover-<YYYY-MM-DD>.md` from this when its transcript gets long (orchestrator.md §Handover). The CTO writes the first one, so the first Orchestrator knows whom to message.

List every lane that is not `DONE` and archived.

```markdown
# Handover <YYYY-MM-DD>

## Contacts
- CTO: <CTO session title>, id `local_<id>`
- The new Orchestrator sets its title to `{{PROJECT}} Orchestrator`, checks in with the CTO by id, and writes its own id here: `local_<id>`

## Open phase
<phase, what its exit gate still lacks>

## Open lanes

Lanes started by the previous Orchestrator stay its children. Message them directly by id and tell each your new id. They report to the Orchestrator by id.

| Title (as in the sidebar) | Session id | State |
|---|---|---|
| <TAG> · <effort>-<NN> <short name> | local_<id> | <working / CHECK: … / GATE: … / PLAY: … / WAIT: … / DONE, not archived> | <!--play-->
| <TAG> · <effort>-<NN> <short name> | local_<id> | <working / CHECK: … / GATE: … / WAIT: … / DONE, not archived> | <!--noplay-->

Notes folder of these lanes: <path from the lanes' brief>

## Frontier
<ready tickets, in the recommended order>

## Owed outside any lane
<what the user still has to do that belongs to no lane; or "none">

## Retro inbox
<number of open items in .scratch/_orchestrator/retro-inbox.md>
```
