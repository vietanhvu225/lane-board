---
name: board-init
description: Set up the Orchestrator + lane board in the current folder - rules in docs/orchestration/, ticket workflow, lane ledger, ticket checker - and print the sentences that open the CTO and Orchestrator sessions. Run once per project.
argument-hint: "[project name]"
disable-model-invocation: true
---

# Board init

Install the lane-board rules into the current folder so the project can run as one **Orchestrator** session plus **lane** child sessions, one ticket each, on top of the `mattpocock-skills` plugin. The rules are copied, not linked: from now on they belong to the project and change through `/mattpocock-skills:retro`.

The plugin lives at `${CLAUDE_PLUGIN_ROOT}`. The installer is `${CLAUDE_PLUGIN_ROOT}/tools/board_init.py`.

## 1. Check prerequisites

- **mattpocock-skills.** Look in your available skills for names starting `mattpocock-skills:` (e.g. `mattpocock-skills:grilling`). If none: stop, and tell the user to run `claude plugin install mattpocock-skills@claude-plugins-official` and start a new session.
- **Python 3.8+.** Run `python --version` (or `python3 --version`). If missing: stop and say so; the installer and the ticket checker need it.
- **Git.** Is the current folder a git repo (`git rev-parse --show-toplevel`)? If it is a repo but not at its top level, ask whether to install at the top level instead.

## 2. Look at the folder

Read what exists; don't assume:

- `docs/orchestration/`: already set up? If so, say what is there and ask whether to skip existing files, overwrite them, or stop.
- `CLAUDE.md` / `AGENTS.md`: the installer creates `CLAUDE.md` when neither exists, otherwise appends a short pointer.
- `.scratch/` and `docs/agents/issue-tracker.md`: is a local-markdown tracker already configured?

## 3. Ask (one round)

Ask together, leading with your recommendation:

1. **Project name** for session titles (`<name> CTO`, `<name> Orchestrator`). Plain ASCII, short (≤ 20 characters is best). Suggest one from the argument or the folder name.
2. **PLAY tag.** Does the project have hands-on work outside the chat (install a tool, play-test a build, try a device)? Recommend **yes** when the project ships something a person must run by hand, **no** for a pure code or docs project. If yes, ask for one short phrase of what PLAY covers here.

## 4. Install

1. Not a git repo: run `git init` and say so.
2. Dry run first, show the list:
   ```
   python -I "${CLAUDE_PLUGIN_ROOT}/tools/board_init.py" --project "<name>" [--no-play | --play-what "<phrase>"] --dry-run .
   ```
   Exit code 2 means files already exist: ask whether to `--skip-existing` or `--force`, then rerun.
3. Run it for real (same command without `--dry-run`).
4. Smoke-test the checker: `python -I tools/check_ticket.py --help` exits 0.

Don't commit unless the user asks; offer it.

## 5. Hand over to the user

Tell the user, filling in the name:

1. Type `/mattpocock-skills:setup-matt-pocock-skills` here and pick **Local markdown** as the issue tracker (tickets in `.scratch/`). The board's ticket header convention is in `docs/agents/ticket-header.md`.
2. Open a new top-level session titled `<name> CTO` and send:
   > You are the CTO of <name>. The orchestration rules are in docs/orchestration/. With me: brainstorm, write the roadmap and docs/orchestration/phases.md, fill in docs/agents/workflow.md §2 and §5 for this project, confirm README §Operating decisions, then write the first handover in .scratch/_orchestrator/.
3. Once `phases.md` and the first handover exist, open another top-level session titled `<name> Orchestrator` (not a child of the CTO) and send:
   > You are <name> Orchestrator. Read docs/orchestration/orchestrator.md and follow it.

Then point to `docs/orchestration/README.md` for the full picture, and to `docs/orchestration/claude-desktop.md` for the **To verify** items to watch on the first run.
