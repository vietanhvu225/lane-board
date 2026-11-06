# Workflow: phase → skill → artifact

The contract between the Orchestrator and lane (worker) sessions for **one ticket**: each step has a required skill, an output and a checkable done criterion. The Orchestrator compares this file with the *session record* and artifacts to know whether work followed the process.

This file is the single source for "which skill goes where". Change the process here (usually after `/mattpocock-skills:retro`).

Skills come from the `mattpocock-skills` plugin. A skill written with `/` is one only the user can type (`disable-model-invocation`); an agent can't call it.

---

## 0. Skills along the project

Fill in the project-specific steps in §2. This table is the usual shape.

| Stage | Skill | For |
|---|---|---|
| Setup | `/mattpocock-skills:setup-matt-pocock-skills` | Issue tracker as **local markdown** (files in `.scratch/`), where glossary and ADRs live |
| Setup | `writing-for-agents` | Keep `CLAUDE.md` and agent docs short, each with a clear "read this when" pointer |
| Plan a phase | `/mattpocock-skills:wayfinder` | A map toward one destination; every ticket is research, task, grilling or prototype |
| Any time | `grilling` + `domain-modeling` (`/mattpocock-skills:grill-with-docs` runs both) | Settle decisions; big ones become ADRs, terms go into `GLOSSARY.md` |
| Any time | `research` | A background agent reads primary sources and writes a cited markdown file |
| Hands-on steps | `wizard` | A step-by-step script for what only the user can do |
| Spec | `/mattpocock-skills:to-spec` | A spec for one feature |
| Tickets | `/mattpocock-skills:to-tickets` | Tracer-bullet tickets with blocking edges |
| Build | `/mattpocock-skills:implement` (+ `codebase-design`, `tdd`) | Code one ticket |
| Build | `code-review` | Review a lane's diff before merge |
| Bugs | `diagnosing-bugs` | Find the cause of a bug or crash |
| End of phase / batch | `/mattpocock-skills:retro` | Improve this file, `CLAUDE.md` and the rules for the next sessions |
| Between sessions | `/mattpocock-skills:handoff` | Move work to a new session; the summary points at artifacts |

---

## 1. Contract of a worker session

**Input:** exactly 1 ticket (exception: several `research` tickets at once). Tickets live in the tracker per `issue-tracker.md` and [ticket-header.md](ticket-header.md): local markdown in `.scratch/<effort>/` (`map.md`, `spec.md`, `issues/NN-<slug>.md`). `.scratch/` **is committed to git**, to keep ticket history, answers and session records for the Orchestrator.

**Steps:**
1. Read the ticket, find its type (`Type:` line).
2. Use the skill §2 gives for that type.
3. Make the artifacts at the paths §2 gives.
4. Write the **session record** into the ticket (§3) and commit per §4.

**Done when:** the artifacts exist, the criteria in §2 are met, the session record has every field, the commit has trailers, and `python -I tools/check_ticket.py <ticket> --base main` exits 0 (run on the lane's branch, before reporting done).

**Under an Orchestrator** ([docs/orchestration/](../orchestration/README.md)): the Orchestrator claims the ticket, writes Decisions-so-far into `map.md` and creates new tickets; the lane writes only its own ticket file ([contract.md §5](../orchestration/contract.md)). Stop points, titles and merge follow contract.md.

When the skill in the table doesn't fit the ticket: do what makes most sense and say so in the session record's `Process deviations`. The Orchestrator gathers deviations for the retro.

---

## 2. Tables by phase

**HITL/AFK** column: HITL = the user must answer directly, the agent never answers for them; AFK = the agent works alone.

### Setup
| Step | Skill | HITL/AFK | Artifact | Done criterion |
|---|---|---|---|---|
| Tracker, domain docs | `/mattpocock-skills:setup-matt-pocock-skills` (user types) | HITL | `docs/agents/issue-tracker.md`, `## Agent skills` in `CLAUDE.md` | Both exist, tracker = local markdown |
| Chart a phase | `/mattpocock-skills:wayfinder` (in a chart lane) | HITL | Map + tickets in the tracker | Map has Destination, Notes, Not yet specified; every ticket has a type and blocking edges |

### Tickets on a wayfinder map (every phase)
| Ticket type | Skill | HITL/AFK | Artifact | Done criterion |
|---|---|---|---|---|
| `research` | `research` (background subagent) | AFK | `docs/research/<name>.md` | Every claim has a primary source; the ticket's answer points to the file |
| `grilling` | `grilling` + `domain-modeling` | HITL | Answer in the ticket; `GLOSSARY.md` / `docs/adr/NNNN-*.md` when there's a new term / decision | Frontier empty, the user confirms shared understanding |
| `prototype` | `prototype` for HTML / logic demos; **(none)** when the prototype must run inside a tool the skill can't drive | HITL | Prototype on a `prototype/<name>` branch, or trial code + screenshots in `.scratch/<effort>/assets/<NN>-*`; verdict in the ticket | Ticket records the question and the verdict; branch / screenshots are linked |
| `task` | `wizard` if the user must do it by hand; none if the agent does it | HITL / AFK | Result in the ticket (paths, figures, URLs…) | Ticket records what was done and the facts later tickets need |

### Spec and tickets
| Step | Skill | HITL/AFK | Artifact | Done criterion |
|---|---|---|---|---|
| Feature spec | `/mattpocock-skills:to-spec` (user types) | HITL | Spec in the tracker | User stories, implementation decisions |
| Split into tickets | `/mattpocock-skills:to-tickets` (user types) | HITL | Implement tickets in the tracker | Each ticket is a tracer bullet with blocking edges and a **manual test script** |

### Build
| Step | Skill | HITL/AFK | Artifact | Done criterion |
|---|---|---|---|---|
| Code one ticket | `/mattpocock-skills:implement` (+ `codebase-design` for new modules, `tdd` for pure logic) | AFK | Code, commit | The ticket's test script passes; `code-review` has run |
| Bug / crash | `diagnosing-bugs` | AFK | Fix + commit | Reproduced before, gone after |
| End of phase / batch | `/mattpocock-skills:retro` (user types) | HITL | Changes to this file, `CLAUDE.md`, the rules | Each proposal accepted or dropped with a reason |
| Change session | `/mattpocock-skills:handoff` | AFK | New session | Summary points at artifacts, copies nothing |

<!-- The CTO adds one table per project phase here (step, ticket type, skill, artifact, done criterion). -->

---

## 3. Session record

Append at the end of the ticket when done:

```markdown
## Session record
- Ticket: <effort>-<NN> <name>
- Type: <research | grilling | prototype | task | implement>
- Skills used: <list>
- Artifacts: <paths in backticks, branch>
- Done criteria: <met / not, with evidence>
- Own choices: <none | technical branches you chose yourself, with reasons>
- Check: <who checked (self / checker subagent), passed in which round, commands run and results>
- Tokens: <figure from the Agent tool result if any, or an estimate; "not measured">
- Process deviations: <none | description>
- Proposed terms: <none | new GLOSSARY.md terms with meanings>
- Open questions / new tickets: <…>
```

`tools/check_ticket.py` requires every field except `Proposed terms`.

---

## 4. Commit trailers

Every worker commit carries two trailers, so the Orchestrator can check through `git log`:

```
<commit subject>

<body>

Ticket: <effort>-<NN>
Skill: <main skill | (none)>
Co-Authored-By: …
```

- The trailer lines sit **in the same last paragraph**, with no blank line between them: git only reads the last paragraph as trailers.
- Check: `git log -1 --format=%(trailers)`.

---

## 5. Orchestrator check

Steps 1, 3, 4 and file scope are checked by `python -I tools/check_ticket.py <ticket> --base main` (on the lane's branch; from main add `--rev <lane branch>`; after merge drop `--base`). The lane, the checker subagent and the Orchestrator all run it.

**Checks by path** (the CTO fills this in; a lane runs every row whose path it touched, before reporting done and again before merging):

| Path touched | Check | Merge kind |
|---|---|---|
| any ticket | `python -I tools/check_ticket.py <ticket> --base main` | — |
| `docs/`, `.scratch/` | — | after the Orchestrator's check, no GATE |
| `<code path>` | `<build / test command>` exits 0 | GATE |

For each closed ticket:
1. The session record has every field.
2. `Skills used` matches §2 for the ticket type, or there is a `Process deviations` entry.
3. Every artifact in the record exists.
4. A commit carries the ticket's `Ticket:` trailer (except answer-only tickets).
5. The done criteria have evidence.

A failing ticket is reopened or gets a fix ticket. Deviations go to the retro.

**Lessons carried over:**
- Criteria such as "every file cites its source line" must plan, before handing out, for data that has no lines (binary files, generated data): write the alternative citation in the ticket.
- A script that regenerates files can change line endings on a checkout with `core.autocrlf=true`: check "running twice changes nothing" with `--check` or `git diff`, not by hashing files.
- An artifact is a snapshot when its ticket closes, not a promise to exist forever: `check_ticket.py` only warns when a later ticket deleted it.
