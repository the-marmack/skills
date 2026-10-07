---
name: intent-lock
description: Promote or revoke a PM's intent on the GitHub project board — promote syncs the latest Word edits and moves the intent's issue from Create to Ready so engineering can plan it; revoke moves it from Ready or Plan back to Create and, if planning had started, runs the repo's intent-lock workflow to remove intents/<issue>-<short-name>/intent.lock so editing can resume. The lock itself is set by that workflow when the issue reaches Plan, never by this skill. Use when a PM wants to promote, approve, finalize, mark ready, revoke, unlock, reopen or send back an intent, or runs /intent-promote or /intent-revoke. Not for creating a new intent (intent-create), publishing ordinary edits (intent-sync), planning an intent (the intents repo's /plan), or moving non-intent issues around a board.
license: MIT
---

# Promote or revoke an intent

The user is a product manager who doesn't know git, so speak in plain language. The local layout and `.config.json`
follow the intent-create skill's reference. Commands and IDs are in [reference.md](reference.md).

The board decides whether an intent is locked, and `intent.lock` in the repo records it. The PM repo's `intent-lock`
workflow is the only thing that writes or removes the lock. It locks the intent while its Status is `statuses.plan`.

| Action      | Board status               | Lock file                             |
| ----------- | -------------------------- | ------------------------------------- |
| **promote** | Create → **Ready**         | none; `/plan` locks it later via Plan |
| **revoke**  | Ready or Plan → **Create** | removed by the workflow if present    |

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. Steps 1 and 2 run for both actions. After that, run only that action's own steps.

## Step 1 — Preflight

- **In:** the action (`promote` or `revoke`) and a short name.
- **Out:** `.config.json`, an up-to-date clone at `repoDir` and the intent's `.intent.json`.

1. Run `gh auth status`. Read `~/Documents/intents/.config.json`. Resolve `repoDir` and clone or pull it, following
   "Repo location" in the intent-create skill's reference.
   If `<repoDir>` has no `user.email`, set one following "Git identity" in the intent-create skill's reference.
2. If no short name was given, list the intents (`<issue>-<short>` folders with a `.intent.json`) together with their
   board status, and ask which one.
3. Read `.intent.json` from the `~/Documents/intents/*-<short>/` folder (an issue number or `<issue>-<short>` also
   works).

## Step 2 — Resolve board item

- **In:** `url` and `itemId` from `.intent.json`.
- **Out:** `PID`, `ITEM`, `FID`, the item's current `STATUS`, and the option IDs for `statuses.create`,
  `statuses.ready` and `statuses.plan`.

Follow "Resolve IDs" in reference.md. If the issue isn't on the board, add it and save the new `itemId` to
`.intent.json`.

## Promote — Step P1: Guard

If `STATUS` is already `statuses.ready` or `statuses.plan`, or `<repoDir>/<repoPath>/intent.lock` exists, tell the PM
the intent is already promoted and stop.

## Promote — Step P2: Final sync

Run the intent-sync skill for this one intent, so the latest Word edits are published before engineering picks it up.
If the sync fails, stop.

## Promote — Step P3: Move to Ready

Set the item's Status to `statuses.ready` using "Set status" in reference.md.

## Promote — Step P4: Record

Run `gh issue comment <url> --body "Promoted to **Ready** for planning."`. Tell the PM:

- the intent is ready for engineering, and they can still edit and sync it until planning starts;
- once it moves to **Plan**, it's locked;
- `/intent-revoke <short>` takes it back.

## Revoke — Step R1: Guard

If `STATUS` is `statuses.create` and there's no `<repoDir>/<repoPath>/intent.lock`, tell the PM the intent isn't
promoted and stop.

If `STATUS` is `statuses.plan` or the lock exists, engineering has started planning. Tell the PM, and ask them to
confirm that they want to pull it back before you continue.

## Revoke — Step R2: Move to Create

Set the item's Status to `statuses.create`.

## Revoke — Step R3: Unlock

Skip this step when there's no `intent.lock`. Otherwise run "Sync the lock" in reference.md for this issue, then pull
`<repoDir>` and check that `intent.lock` is gone. If the run fails, tell the PM that the board says Create but the
intent is still locked, and show them the run's link.

## Revoke — Step R4: Record

Run `gh issue comment <url> --body "Revoked: moved back to **Create**."`. Tell the PM they can edit `intent.docx` again
and publish their changes with `/intent-sync`.
