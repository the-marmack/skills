---
name: intent-lock
description: Promote or revoke a PM's intent on the GitHub project board — promote syncs the latest Word edits, moves the intent's issue from Create to Ready and commits an intent.lock file into intents/<issue>-<short-name>/ so intent-sync can no longer change it; revoke moves the issue from Ready back to Create and deletes the lock so editing can resume. Use when a PM wants to promote, approve, finalize, lock, mark ready, revoke, unlock, reopen or send back an intent, or runs /intent-promote or /intent-revoke. Not for creating a new intent (intent-create), publishing ordinary edits (intent-sync), or moving non-intent issues around a board.
license: MIT
---

# Promote or revoke an intent

The user is a product manager who doesn't know git, so speak in plain language. The local layout and `.config.json`
follow the intent-create skill's reference. Commands and IDs are in [reference.md](reference.md).

| Action      | Board status       | Lock file             |
| ----------- | ------------------ | --------------------- |
| **promote** | Create → **Ready** | `intent.lock` added   |
| **revoke**  | Ready → **Create** | `intent.lock` removed |

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. Steps 1 and 2 run for both actions. After that, run only that action's own steps.

## Step 1 — Preflight

- **In:** the action (`promote` or `revoke`) and a short name.
- **Out:** `.config.json`, an up-to-date `.repo/` and the intent's `.intent.json`.

1. Run `gh auth status`. Read `~/Documents/intents/.config.json`. Run `git -C ~/Documents/intents/.repo pull --rebase
   --quiet`.
   If `.repo/` has no `user.email`, set one following "Git identity" in the intent-create skill's reference.
2. If no short name was given, list the intents (folders with a `.intent.json`) together with their lock state, and
   ask which one.
3. Read `~/Documents/intents/<short>/.intent.json`.

## Step 2 — Resolve board item

- **In:** `url` and `itemId` from `.intent.json`.
- **Out:** `PID`, `ITEM`, `FID` and the option IDs for `statuses.create` and `statuses.ready`.

Follow "Resolve IDs" in reference.md. If the issue isn't on the board, add it and save the new `itemId` to
`.intent.json`.

## Promote — Step P1: Guard

If `.repo/<repoPath>/intent.lock` already exists, tell the PM the intent is already promoted and stop.

## Promote — Step P2: Final sync

Run the intent-sync skill for this one intent, so the latest Word edits are published before the lock goes on. If the
sync fails, stop.

## Promote — Step P3: Move to Ready

Set the item's Status to `statuses.ready` using "Set status" in reference.md.

## Promote — Step P4: Lock

Write `.repo/<repoPath>/intent.lock` using "Lock file" in reference.md, then:

```sh
R=~/Documents/intents/.repo
git -C "$R" add "<repoPath>/intent.lock"
git -C "$R" commit -m "intent(<issue>): promote <short>"
git -C "$R" push origin HEAD:main
```

If the push fails, set Status back to `statuses.create`, remove the local lock, and report the error.

## Promote — Step P5: Record

Run `gh issue comment <url> --body "Promoted to **Ready** and locked at <commit sha>."`. Tell the PM the intent is
locked and that `/intent-revoke <short>` unlocks it.

## Revoke — Step R1: Guard

If `.repo/<repoPath>/intent.lock` doesn't exist, tell the PM the intent isn't promoted. Still make sure the Status is
`statuses.create`, then stop.

## Revoke — Step R2: Move to Create

Set the item's Status to `statuses.create`.

## Revoke — Step R3: Unlock

```sh
R=~/Documents/intents/.repo
git -C "$R" rm -q "<repoPath>/intent.lock"
git -C "$R" commit -m "intent(<issue>): revoke <short>"
git -C "$R" push origin HEAD:main
```

## Revoke — Step R4: Record

Run `gh issue comment <url> --body "Revoked: moved back to **Create** and unlocked."`. Tell the PM they can edit
`intent.docx` again and publish their changes with `/intent-sync`.
