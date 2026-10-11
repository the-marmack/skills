---
name: intent-promote
description: Promote a PM's intent for planning — publishes the latest Word edits with intent-sync, then moves the intent's issue from Create to Ready on the GitHub project board, which is the PM's approval. Moving the card to Ready by hand is approval too. Once planning starts the intent is locked for good (locked means locked); to change it after that, the PM starts a new intent that supersedes it, and to drop it, closes its issue as not planned. Use when a PM wants to promote, approve, finalize, mark ready or submit an intent for planning, or runs /intent-promote. Not for creating or superseding an intent (intent-create), publishing ordinary edits (intent-sync), planning an intent (the plan plugin's plan-create), or moving non-intent issues around a board.
user-invocable: false
license: MIT
---

# Promote an intent

The user is a product manager, so speak in plain language and keep git out of it. The local layout, `.config.json`, the
board recipes and the lock are in the `intent-bundle` skill. Which command and recipe each step uses is in
[references/REFERENCE.md](references/REFERENCE.md).

Promoting is approval: it moves the card from **Create** to **Ready**, and engineering can then plan it. Moving the card
by hand does the same. This skill never writes or removes a lock: `plan-create` locks an intent when planning starts,
and **locked means locked**. After that, the intent changes only through a new intent that supersedes it
(`/intent-create … supersedes <issue URL>`), or is dropped by closing its issue as not planned.

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others.

## Step 1 — Preflight

- **In:** a short name.
- **Out:** `.config.json` and the intent's `.intent.json`.

1. Run `gh auth status`. Read `~/Documents/intents/.config.json`. Nothing is cloned and git isn't needed: GitHub
   steps use "GitHub recipes" in the `intent-bundle` skill.
2. If no short name was given, ask which intent to promote. The options are the intents that can be promoted: the
   `<issue>-<short>` folders with a `.intent.json` whose card is in Create and that aren't locked. Each option is one
   intent, newest first, at most four. Don't mark one as recommended or add an option for another intent: the PM types
   any other name in the free-text answer. If none can be promoted, say so and stop.
3. Read `.intent.json` from the `~/Documents/intents/*-<short>/` folder (an issue number or `<issue>-<short>` also
   works).

## Step 2 — Resolve board item

- **In:** `url` and `itemId` from `.intent.json`.
- **Out:** `PID`, `ITEM`, `FID`, the item's current `STATUS`, and the option ID for `Ready`.

Follow "Board → Resolve IDs" and "Board → Find the item" in the `intent-bundle` skill. If the issue isn't on the
board, add it and save the new `itemId` to `.intent.json`.

## Step 3 — Guard

If `STATUS` is already `Ready` or a locked status, or "Lock check" in the `intent-bundle` skill says locked,
tell the PM the intent is already promoted and stop. If it's locked, add that a change now needs a new intent that
supersedes it. If the lock check is unknown, stop and say the lock couldn't be confirmed.

## Step 4 — Final sync

Run the intent-sync skill for this one intent, so the latest Word edits are published before engineering picks it up.
If the sync fails, stop.

## Step 5 — Move to Ready

Set the item's Status to `Ready` using "Board → Set status" in the `intent-bundle` skill.

## Step 6 — Record

Run `gh issue comment <url> --body "Promoted to **Ready** for planning."`. Tell the PM:

- the intent is ready for engineering, and they can still edit and sync it until planning starts;
- once planning starts it's locked for good: a change after that is a new intent that supersedes it
  (`/intent-create … supersedes <issue URL>`);
- to drop it before planning, move the card back to **Create**; to drop it for good, close its issue as not planned.
