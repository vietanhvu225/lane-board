"""Check one ticket against docs/agents/workflow.md §3-§5 and contract §5-§6.

    python -I tools/check_ticket.py .scratch/p1/issues/04-persistence.md
    python -I tools/check_ticket.py <ticket> --base main                # also check file scope on the lane's branch
    python -I tools/check_ticket.py <ticket> --base main --rev <branch>  # from main: read ticket and artifacts at <branch>

Checks:
  0. Without `--rev`: read the working tree. With `--rev`: read the ticket and artifacts from that commit.
  1. Header: `Type:`, `HITL/AFK:`, `Status:` present; the ticket is `resolved` (or `wontfix` / `needs-info`).
  2. A `resolved` ticket has `## Answer`, and its last `## Session record` has every field (workflow.md §3).
  3. Every backticked path on the `Artifacts:` line exists (globs, `<...>` and branch names are skipped).
     An artifact a later ticket deleted (still present in a commit carrying this ticket's trailer) only warns.
  4. A commit (reachable from `--rev`, default HEAD) has a `Ticket:` trailer naming this ticket, and a `Skill:` trailer.
  5. With `--base`: files changed from the merge-base to `--rev` match the `Scope:` globs in the header.
It cannot check the ticket's own `Done when`: that is the checker subagent's job.
The repo is the git top level of the current directory, so run it from the checkout (or worktree) you mean.
Exit 1 on any ERROR; WARNINGs don't change the exit code.
"""

import argparse
import fnmatch
import pathlib
import posixpath
import re
import subprocess
import sys
import unicodedata

sys.dont_write_bytecode = True

FIELDS = ["Ticket", "Type", "Skills used", "Artifacts", "Done criteria", "Own choices",
          "Check", "Tokens", "Process deviations", "Open questions / new tickets"]
HEADER = ["Type", "HITL/AFK", "Status"]
CLOSED = ("resolved", "wontfix", "needs-info")
BRANCH_PREFIXES = ("claude/", "lane/", "prototype/")


def nfc(s):
    return unicodedata.normalize("NFC", s.strip())


def toplevel():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode:
        sys.exit("not inside a git repository")
    return pathlib.Path(r.stdout.strip()).resolve()


REPO = toplevel()


def git(*args):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def git_ok(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True).returncode == 0


def header(lines):
    """`Key: value` lines before the first `##` heading."""
    out = {}
    for line in lines:
        if line.startswith("## "):
            break
        m = re.match(r"^([\w/ ]+):\s*(.*)$", line)
        if m:
            out[nfc(m.group(1))] = nfc(m.group(2))
    return out


def sections(lines, prefix):
    """(title, lines) for every `## <prefix>...` heading."""
    out, cur = [], None
    for line in lines:
        if line.startswith("## "):
            cur = (line[3:].strip(), []) if line[3:].startswith(prefix) else None
            if cur:
                out.append(cur)
        elif cur:
            cur[1].append(line)
    return out


def record_fields(body):
    """{field: first-line value} from the top-level `- Field: ...` lines of a session record."""
    out = {}
    for line in body:
        m = re.match(r"^- ([^:]+):\s*(.*)$", line)
        if m:
            out[nfc(m.group(1))] = nfc(m.group(2))
    return out


def strip_id(s):
    return re.sub(r"^[\w.]+-\d+\s+", "", s)


def match(trailer, names):
    """The trailer names the ticket id `<effort>-<NN>`, or its title (with or without the id prefix)."""
    return trailer in names or strip_id(trailer) in {strip_id(n) for n in names if n}


def artifact_paths(value):
    for tok in re.findall(r"`([^`]+)`", value):
        tok = tok.strip()
        if any(c in tok for c in "*<>?{,") or " " in tok or tok.startswith(BRANCH_PREFIXES):
            continue
        if "/" in tok or re.search(r"\.\w{1,5}$", tok):
            yield tok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticket")
    ap.add_argument("--rev", help="read ticket, artifacts, trailers and scope at this commit / branch (default: working tree + HEAD)")
    ap.add_argument("--base", help="base branch for the file scope check, e.g. main")
    sys.stdout.reconfigure(encoding="utf-8")
    args = ap.parse_args()

    path = pathlib.Path(args.ticket)
    path = (path if path.is_absolute() else pathlib.Path.cwd() / path).resolve()
    rel = path.relative_to(REPO).as_posix()
    rev = args.rev or "HEAD"
    if args.rev:
        lines = git("show", f"{rev}:{rel}").splitlines()
        tracked = git("ls-tree", "-r", "--name-only", rev).splitlines()
        exists = lambda p: p in tracked or any(t.startswith(p.rstrip("/") + "/") for t in tracked)
    else:
        lines = path.read_text(encoding="utf-8").splitlines()
        tracked = git("ls-files").splitlines()
        exists = lambda p: (REPO / p).exists()
    errors, warns = [], []

    head = header(lines)
    for k in HEADER:
        if not head.get(k):
            errors.append(f"header lacks `{k}:`")
    status = head.get("Status", "")
    if status not in CLOSED:
        errors.append(f"`Status: {status}`: ticket not resolved (checking the copy in {args.rev or 'the working tree'})")
    tid = f"{path.parent.parent.name}-{path.stem.split('-')[0]}"
    names = {tid}
    if lines and lines[0].startswith("# "):
        names.add(nfc(lines[0][2:]).split(" (")[0])

    missing = []  # (path as written, path relative to the ticket)
    if status == "resolved":
        if not sections(lines, "Answer"):
            errors.append("resolved but no `## Answer`")
        records = sections(lines, "Session record")
        if not records:
            errors.append("resolved but no `## Session record`")
        else:
            rec = record_fields(records[-1][1])
            for f in FIELDS:
                if f not in rec:
                    errors.append(f"last session record lacks `- {f}:` (workflow.md §3)")
            names.add(rec.get("Ticket", "").split(" (")[0])
            here = path.parent.relative_to(REPO).as_posix()
            for p in artifact_paths(rec.get("Artifacts", "")):
                near = posixpath.normpath(posixpath.join(here, p))
                if exists(p) or exists(near) or any(t == p or t.endswith("/" + p) for t in tracked):
                    continue
                missing.append((p, near))

        log = git("log", rev, "--format=%H%x1f%(trailers:key=Ticket,valueonly,separator=;)"
                  "%x1f%(trailers:key=Skill,valueonly,separator=;)%x1e")
        hits = []
        for entry in log.split("\x1e"):
            parts = entry.strip().split("\x1f")
            if len(parts) == 3 and any(match(nfc(t), names) for t in parts[1].split(";") if t):
                hits.append(parts)
        if not hits:
            errors.append(f"no commit (from {rev}) has the trailer `Ticket: {tid}`; trailers must share the last paragraph with `Co-Authored-By:` (workflow.md §4)")
        elif not any(h[2].strip() for h in hits):
            errors.append(f"commits with the `Ticket:` trailer of {tid} lack a `Skill:` trailer")
        # Gone at rev but present in one of this ticket's commits: a later ticket deleted it.
        for p, near in missing:
            was = next((h[0][:7] for h in hits if any(git_ok("cat-file", "-e", f"{h[0]}:{q}") for q in (p, near))), None)
            if was:
                warns.append(f"artifact `{p}` is gone at {rev} but exists in this ticket's commit {was} (deleted by a later ticket?)")
            else:
                (warns if "/" not in p else errors).append(f"artifact not in the repo: `{p}`")

    if args.base:
        scope = [nfc(s) for s in re.findall(r"`([^`]+)`", head.get("Scope", ""))]
        if not scope:
            errors.append("header lacks `Scope:` (globs in backticks), cannot check file scope")
        else:
            base = git("merge-base", args.base, rev).strip()
            changed = [nfc(f) for f in git("diff", "--name-only", f"{base}..{rev}").splitlines() if f]
            outside = [f for f in changed if f != rel and not any(fnmatch.fnmatch(f, g) for g in scope)]
            for f in outside:
                errors.append(f"file outside the declared scope: `{f}` (needs CHECK, or a `Process deviations` entry)")

    for w in warns:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{rel}: {'pass' if not errors else f'{len(errors)} error(s)'}" + (f", {len(warns)} warning(s)" if warns else ""))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
