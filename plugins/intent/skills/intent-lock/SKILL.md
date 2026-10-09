---
name: intent-lock
description: Promote or revoke a PM's intent on the GitHub project board — promote syncs the latest Word edits and moves the intent's issue from Create to Ready so engineering can plan it; revoke moves it from Ready or any later column back to Create and, if planning had started, deletes the intent's lock.yaml in the-marmack/intents (and closes its draft plan PR) so editing can resume. The lock itself is written by plan-create when planning starts, never by this skill. Use when a PM wants to promote, approve, finalize, mark ready, revoke, unlock, reopen or send back an intent, or runs /intent-promote or /intent-revoke. Not for creating a new intent (intent-create), publishing ordinary edits (intent-sync), planning an intent (the plan plugin's plan-create), or moving non-intent issues around a board.
license: MIT
---

# Promote or revoke an intent

The user is a product manager who doesn't know git, so speak in plain language. The local layout, `.config.json`, the
board recipes and the lock are in the `intent-bundle` skill. Which command and recipe each step uses is in
[references/REFERENCE.md](references/REFERENCE.md).

An intent is locked when `the-marmack/intents` holds its `lock.yaml` ("Locked" in the `intent-bundle` skill).
`plan-create` writes it when planning starts, and revoke removes it. This skill never writes a lock.

| Action      | Board status                | Lock                                               |
| ----------- | --------------------------- | -------------------------------------------------- |
| **promote** | Create → **Ready**          | none; `/plan-create` locks it when planning starts |
| **revoke**  | Ready or later → **Create** | central `lock.yaml` deleted, if there is one       |

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. Steps 1 and 2 run for both actions. After that, run only that action's own steps.

## Step 1 — Preflight

- **In:** the action (`promote` or `revoke`) and a short name.
- **Out:** `.config.json`, an up-to-date clone at `repoDir` and the intent's `.intent.json`.

1. Run `gh auth status`. Read `~/Documents/intents/.config.json`. Resolve `repoDir` and clone or pull it, following
   "Repo location" in the `intent-bundle` skill.
   If `<repoDir>` has no `user.email`, set one following "Git identity" in the `intent-bundle` skill.
2. If no short name was given, list the intents (`<issue>-<short>` folders with a `.intent.json`) together with their
   board status, and ask which one.
3. Read `.intent.json` from the `~/Documents/intents/*-<short>/` folder (an issue number or `<issue>-<short>` also
   works).

## Step 2 — Resolve board item

- **In:** `url` and `itemId` from `.intent.json`.
- **Out:** `PID`, `ITEM`, `FID`, the item's current `STATUS`, and the option IDs for `statuses.create`,
  `statuses.ready` and `statuses.plan`.

Follow "Board → Resolve IDs" and "Board → Find the item" in the `intent-bundle` skill. If the issue isn't on the
board, add it and save the new `itemId` to `.intent.json`.

## Promote — Step P1: Guard

If `STATUS` is already `statuses.ready` or a locked status, or "Lock check" in the `intent-bundle` skill says
locked, tell the PM the intent is already promoted and stop. If the lock check is unknown,
stop and say the lock couldn't be confirmed.

## Promote — Step P2: Final sync

Run the intent-sync skill for this one intent, so the latest Word edits are published before engineering picks it up.
If the sync fails, stop.

## Promote — Step P3: Move to Ready

Set the item's Status to `statuses.ready` using "Board → Set status" in the `intent-bundle` skill.

## Promote — Step P4: Record

Run `gh issue comment <url> --body "Promoted to **Ready** for planning."`. Tell the PM:

- the intent is ready for engineering, and they can still edit and sync it until planning starts;
- once it moves to **Plan**, it's locked;
- `/intent-revoke <short>` takes it back.

## Revoke — Step R1: Guard

Run "Lock check" in the `intent-bundle` skill (GitHub's `main`, not the local clone). If `STATUS` is
`statuses.create` and the check says unlocked, tell the PM the intent isn't promoted and stop.

If `STATUS` is a locked status or the lock exists, engineering has started planning or building. Tell the PM, and ask
them to confirm that they want to pull it back before you continue.

## Revoke — Step R2: Move to Create

Set the item's Status to `statuses.create`.

## Revoke — Step R3: Unlock

Skip this step when "Lock check" says unlocked. Otherwise:

1. Delete the central lock with "Remove the central lock" in the `intent-bundle` skill. On 403 or 404, stop and tell
   the PM a planner has to revoke it.
2. Close an open draft plan PR for the intent, if there is one
   (`gh pr list -R the-marmack/intents --head plan/<login>-<issue>-<short>`), with a comment.
3. Run "Lock check" again and confirm it says unlocked. If it doesn't, tell the PM the board says Create but the
   intent is still locked.

## Revoke — Step R4: Record

Remove the `locked` label if the issue has it (`gh issue edit <url> --remove-label locked`). Then run
`gh issue comment <url> --body "Revoked: moved back to **Create**."`. Tell the PM they can edit `intent.docx` again
and publish their changes with `/intent-sync`.
