# lane-board

Run a project bigger than one Claude Code session as **one Orchestrator session plus child lane sessions, one ticket each**, on top of [Matt Pocock's skills](https://github.com/mattpocock/skills) (`wayfinder`, `to-spec`, `to-tickets`, `implement`, `grilling`, `research`, `retro`, …).

lane-board adds no skills of its own besides `/lane-board:board-init`. It is a set of **rules** for how sessions coordinate: who starts a lane, how a lane reports, where it stops for you, who writes which tracker file, how lanes merge, how the Orchestrator hands over when its transcript gets long. Plus a ticket checker script that catches the mistakes rules alone didn't.

Built for the Claude Desktop app (Code tab), where a session can start child sessions and receive their turn-end notes.

## How it works

```
<Project> CTO            top level: plans, writes and fixes the rules
<Project> Orchestrator   top level: picks tickets, starts lanes, checks their work
   ├── lane p1-03 …      child session: one ticket, its own git worktree
   └── lane p1-04 …
```

- **Three levels.** Workflow (one ticket: which skill, which artifact, when done), Board (many tickets in parallel: start, report, stop, merge), Roadmap (phases, each with a wayfinder map).
- **The title is the status.** A lane's sidebar title is `<TAG> · <effort>-<NN> <short name>`; the tag (`CHECK`, `GATE`, `PLAY`, `WAIT`, `DONE`) says whether you need to act. `PLAY` (hands-on work outside the chat) is optional.
- **The user decides.** Lanes only start on your words; they stop only at listed stop points (a grilling round, a prototype to look at, a merge that needs approval, a skill only you can type, a real blocker).
- **One writer per file.** The Orchestrator writes claims, the map and new tickets on main; a lane writes only its own ticket file, in its own worktree.
- **Checked, not trusted.** Each ticket ends with a session record and commit trailers; `tools/check_ticket.py` checks header, record, artifacts, trailers and file scope before merge.
- **Yolo mode.** Before you step away, approve queues of AFK tickets; worker lanes do each one with a doer subagent and a checker subagent, merge, and only report when the queue is empty or stopped.

## Install

Requires Claude Code with plugin support, Python 3.8+, git, and the `mattpocock-skills` plugin (installed with lane-board as a dependency).

```bash
claude plugin marketplace add <path or URL of this repo>
claude plugin install lane-board@lane-board
```

If the dependency didn't come along:

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

## Use

In an empty folder (or an existing repo), start a session and type:

```
/lane-board:board-init <project name>
```

It asks for the project name and whether you want the `PLAY` tag, then writes:

| Path | What |
|---|---|
| `docs/orchestration/README.md` | the brief: levels, roles, how to start, operating decisions |
| `docs/orchestration/contract.md` | shared rules: titles and tags, stop points, reports, tracker ownership, merge, capacity, yolo mode |
| `docs/orchestration/orchestrator.md`, `lane.md` | each role step by step |
| `docs/orchestration/claude-desktop.md` | what the app does, labelled Observed / Assumed / To verify |
| `docs/orchestration/phases.md` | the shape of a phase brief, for the CTO to fill in |
| `docs/orchestration/board-diary.md` | log of what's in no ticket: app behaviour, stuck points, rule changes |
| `docs/orchestration/templates/` | lane prompt, chart lane prompt, handover |
| `docs/agents/workflow.md`, `ticket-header.md` | the per-ticket workflow on top of mattpocock-skills, session record, trailers, checks |
| `docs/adr/0001-orchestrator-and-lanes.md` | the decision to work this way |
| `.scratch/_orchestrator/lanes.md`, `retro-inbox.md` | lane ledger, retro inbox |
| `tools/check_ticket.py` | the ticket checker |

Then it tells you to run `/mattpocock-skills:setup-matt-pocock-skills` (pick local markdown) and gives the sentences that open the CTO and Orchestrator sessions.

The copied files belong to your project from then on. Change them through `/mattpocock-skills:retro`, and log why in the board diary. Entries tagged `[general]` are worth sending back here as issues.

## Layout of this repo

| Folder | Holds | Installed as |
|---|---|---|
| `core/` | the board contract | `docs/orchestration/contract.md` |
| `roles/` | Orchestrator and lane | `docs/orchestration/{orchestrator,lane}.md` |
| `templates/` | brief, prompts, handover, ledger, diary, workflow, ADR | various |
| `adapters/claude-desktop/` | app behaviour the rules rely on | `docs/orchestration/claude-desktop.md` |
| `skills/board-init/` | the `/lane-board:board-init` skill | — |
| `tools/` | `board_init.py` (installer), `check_ticket.py` | `tools/check_ticket.py` |

Files in `core/`, `roles/` and `templates/` are written with links as they resolve **after** install, so some links don't resolve while browsing this repo.

## Where it comes from

Extracted on 2026-11-06 from the orchestration rules of a private solo project (source commit `92242cc`), after it ran two full phases, one `/retro` and one Orchestrator handover with this model. The ideas on titles-as-status, stop points and handover tables were first tried in an earlier private board for team work. [docs/lessons.md](docs/lessons.md) lists why the rules look the way they do.

## Credits and license

MIT, see [LICENSE](LICENSE). Depends on, and does not bundle, [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, © Matt Pocock). lane-board is not affiliated with or endorsed by Matt Pocock.
