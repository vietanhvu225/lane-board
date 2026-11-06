"""Install the lane-board rules and templates into a project folder.

    python -I board_init.py --project "Acme" [--no-play] [--play-what "..."] [--date 2026-11-06] [TARGET]

Called by the /lane-board:board-init skill. Writes:
  docs/orchestration/  README, contract, orchestrator, lane, claude-desktop, board-diary, phases, templates/
  docs/agents/         workflow.md, ticket-header.md
  docs/adr/            0001-orchestrator-and-lanes.md
  .scratch/_orchestrator/  lanes.md, retro-inbox.md
  tools/check_ticket.py
  CLAUDE.md            created if missing (or AGENTS.md, if only that exists); otherwise a pointer is appended if absent

Fills {{PROJECT}}, {{DATE}}, {{SOURCE}}, {{PLAY_WHAT}}. A line ending in `<!--play-->` is kept only with
the PLAY tag, one ending in `<!--noplay-->` only without it.
Refuses to overwrite existing files unless --force (or --skip-existing to leave them as they are).
"""

import argparse
import datetime
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parents[1]

FILES = [  # (source in the plugin, target in the project, fill placeholders)
    ("templates/README.md", "docs/orchestration/README.md", True),
    ("core/contract.md", "docs/orchestration/contract.md", True),
    ("roles/orchestrator.md", "docs/orchestration/orchestrator.md", True),
    ("roles/lane.md", "docs/orchestration/lane.md", True),
    ("adapters/claude-desktop/README.md", "docs/orchestration/claude-desktop.md", True),
    ("templates/board-diary.md", "docs/orchestration/board-diary.md", True),
    ("templates/phases.md", "docs/orchestration/phases.md", True),
    ("templates/lane-prompt.md", "docs/orchestration/templates/lane-prompt.md", True),
    ("templates/lane-chart-prompt.md", "docs/orchestration/templates/lane-chart-prompt.md", True),
    ("templates/handover.md", "docs/orchestration/templates/handover.md", True),
    ("templates/workflow.md", "docs/agents/workflow.md", True),
    ("templates/ticket-header.md", "docs/agents/ticket-header.md", True),
    ("templates/adr-0001.md", "docs/adr/0001-orchestrator-and-lanes.md", True),
    ("templates/lanes.md", ".scratch/_orchestrator/lanes.md", True),
    ("templates/retro-inbox.md", ".scratch/_orchestrator/retro-inbox.md", True),
    ("tools/check_ticket.py", "tools/check_ticket.py", False),
]
CLAUDE_POINTER = "docs/orchestration/README.md"


def fill(text, values, play):
    out = []
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        end = line[len(body):]
        if body.endswith("<!--play-->"):
            if not play:
                continue
            line = body[: -len("<!--play-->")].rstrip() + end
        elif body.endswith("<!--noplay-->"):
            if play:
                continue
            line = body[: -len("<!--noplay-->")].rstrip() + end
        out.append(line)
    text = "".join(out)
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if left:
        raise SystemExit(f"unfilled placeholders: {sorted(set(left))}")
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", default=".", help="project folder (default: current folder)")
    ap.add_argument("--project", required=True, help="project name used in session titles, plain ASCII, e.g. 'Acme'")
    ap.add_argument("--no-play", action="store_true", help="drop the PLAY tag (no hands-on work outside the chat)")
    ap.add_argument("--play-what", default="install or configure a tool, try a build by hand",
                    help="what PLAY covers in this project, one short phrase")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--skip-existing", action="store_true", help="leave existing files as they are")
    ap.add_argument("--dry-run", action="store_true", help="list what would be written")
    sys.stdout.reconfigure(encoding="utf-8")
    args = ap.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._-]{0,30}", args.project):
        raise SystemExit("--project must be plain ASCII (letters, digits, space . _ -), at most 31 characters")
    target = pathlib.Path(args.target).resolve()
    if not target.is_dir():
        raise SystemExit(f"target folder does not exist: {target}")

    version = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    values = {"PROJECT": args.project, "DATE": args.date, "SOURCE": f"lane-board {version}",
              "PLAY_WHAT": args.play_what}
    play = not args.no_play

    existing = [dst for _, dst, _ in FILES if (target / dst).exists()]
    if existing and not (args.force or args.skip_existing):
        print("These files already exist; rerun with --skip-existing or --force:")
        for dst in existing:
            print("  ", dst)
        sys.exit(2)

    for src, dst, templated in FILES:
        path = target / dst
        if path.exists() and args.skip_existing:
            print("kept   ", dst)
            continue
        data = (ROOT / src).read_bytes()
        if templated:
            data = fill(data.decode("utf-8"), values, play).encode("utf-8")
        print(("would write" if args.dry_run else "wrote  "), dst)
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    claude = target / "CLAUDE.md"
    if not claude.exists() and (target / "AGENTS.md").exists():
        claude = target / "AGENTS.md"  # never create CLAUDE.md next to an AGENTS.md
    if not claude.exists():
        print(("would write" if args.dry_run else "wrote  "), "CLAUDE.md")
        if not args.dry_run:
            claude.write_text(fill((ROOT / "templates/CLAUDE.md").read_text(encoding="utf-8"), values, play),
                              encoding="utf-8")
    elif CLAUDE_POINTER not in claude.read_text(encoding="utf-8"):
        print(("would append to" if args.dry_run else "appended to"), claude.name)
        if not args.dry_run:
            with claude.open("a", encoding="utf-8") as f:
                f.write("\n## Orchestration\n\n"
                        f"- [{CLAUDE_POINTER}]({CLAUDE_POINTER}): how sessions are coordinated "
                        "(Orchestrator, lanes, CTO). Read when you are one of them.\n"
                        "- [docs/agents/workflow.md](docs/agents/workflow.md): skill, artifact, done criterion "
                        "and session record per ticket type. Read before taking a ticket.\n")
    else:
        print(f"kept    {claude.name} (already points to the orchestration docs)")


if __name__ == "__main__":
    main()
