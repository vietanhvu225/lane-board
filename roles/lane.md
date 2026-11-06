# Role: Lane

A child session of `{{PROJECT}} Orchestrator` that does exactly one ticket. Rules: [contract.md](contract.md). How to do a ticket: [workflow.md](../agents/workflow.md).

---

## At start

1. Read the ticket named in your prompt, `CLAUDE.md`, and workflow.md §1–§2 for your ticket type.
2. Set your title: `<effort>-<NN> <short name>` (contract §2).
3. Read the shared notes (the app gives the folder path in your brief). Write one note: ticket, branch, files / folders you expect to touch.
4. Confirm your worktree is based on the latest main and the ticket is `Status: claimed` under your name; if not, merge main into your branch and read it again (contract §5).

## While working

1. Do the ticket by workflow.md: the right skill, the right artifacts, the right criteria.
2. Stop **only** at the stop points in contract §3. Each stop: set the tag, send one line to the Orchestrator by the `Orchestrator id` in your prompt (contract §4), end the turn with a report that opens `<title> — <what you need>`.
3. Change your title whenever the tag changes. One tag, first.
4. Before editing a file another lane might touch: reread the shared notes. After a change others need to know about: write a note.
5. Don't edit other tickets, `map.md`, or shared files outside your declared scope. If you must: `CHECK`.

## When done

1. Write `## Answer` and the session record (workflow.md §3) into the ticket file, set `Status: resolved`, commit with trailers (workflow.md §4).
2. Run `python -I tools/check_ticket.py <ticket> --base main` (plus the project checks for the paths you touched, workflow.md §5). Fix until it exits 0, or record why under `Process deviations`.
3. Send the Orchestrator: `<title> — done, waiting for the check`. Tag `WAIT`.
4. The Orchestrator answers: fix what is missing; or "ok to merge" when it's your turn. A checker subagent of your own passing is not "ok to merge".
5. Merge: merge main into your branch, rerun the checks, merge into main (contract §6).
6. Tag `DONE`, a last note (what you merged), send `<title> — DONE` to the Orchestrator.

## As a worker lane (yolo mode)

When the Orchestrator hands you a queue of tickets (after the user approved it), follow [contract §10](contract.md): one doer subagent and one checker subagent per ticket, merge yourself, report only when the queue is empty or stopped.

## When a message comes from a new Orchestrator

Answer the sender. From then on, send to the new Orchestrator's id.
