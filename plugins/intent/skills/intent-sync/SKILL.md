---
name: intent-sync
description: Publish a PM's edits to one intent at a time — convert its ~/Documents/intents/<issue>-<short-name>/intent.docx Word file to markdown using only built-in OS tools and push it as intents/<issue>-<short-name>/intent.md straight to main in their intent-<user> GitHub repo, a thin layer over git for people who have never used it. With no intent named, lists the unlocked intents and asks which one. Refuses to touch an intent that has an intent.lock (engineering has started planning it). Use when a PM wants to sync, save, publish, upload or push their intent changes, or runs /intent-sync. Not for creating a new intent (intent-create), promoting, locking or revoking one (intent-lock), or general git pushes in code repositories.
license: MIT
---

# Sync intents to GitHub

The user is a product manager who doesn't know git. Their Word file, `intent.docx`, is the source of truth. This skill
converts it to markdown and pushes it to `main`, and the PM never sees git. The local layout, `.config.json` and Word
conversion are in the `intent-bundle` skill. Which command and recipe each step uses is in
[references/REFERENCE.md](references/REFERENCE.md).

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others.

## Step 1 — Preflight

- **In:** nothing.
- **Out:** `.config.json` and an up-to-date clone at `repoDir`.

1. Run `gh auth status`. If it fails, ask the PM to run `gh auth login` and stop.
2. Read `~/Documents/intents/.config.json`. If it is missing, tell the PM to run `/intent-create` first and stop.
3. Resolve `repoDir` and clone or pull it, following "Repo location" in the `intent-bundle` skill.
4. If `<repoDir>` has no `user.email`, set one following "Git identity" in the `intent-bundle` skill.

## Step 2 — Select

- **In:** an optional short-name argument.
- **Out:** exactly one intent folder.

Sync publishes one intent at a time. An intent is **locked** when `<repoDir>/<repoPath>/intent.lock` exists: it has
moved to Plan on the board and engineering is planning it, so it can't change here.

- **A short name was given:** pick the `~/Documents/intents/*-<short>/` folder (an issue number or `<issue>-<short>`
  also works).
- **No argument:** list every child folder that has a `.intent.json` and isn't locked, showing each intent's title and
  `<issue>-<short>`, and ask the PM to pick one (use the interactive question UI when it exists). Leave locked intents
  out of the list. If none are unlocked, say so and stop.

A folder with an `intent.docx` but no `.intent.json` was never created through `/intent-create`, so never offer it.

## Step 3 — Lock check

- **In:** the chosen intent's `repoPath` from `.intent.json`.
- **Out:** the intent, confirmed unlocked.

If `<repoDir>/<repoPath>/intent.lock` exists, stop and tell the PM: "*(intent title)* is being planned and is locked.
Run `/intent-revoke <short>` first if it needs changes." Never edit, delete or bypass a lock here.

## Step 4 — Convert

- **In:** `~/Documents/intents/<issue>-<short>/intent.docx`.
- **Out:** a fresh `<repoDir>/<repoPath>/intent.md`.

Extract the Word file's content and write `<repoDir>/<repoPath>/intent.md` from it. Never write an `intent.md` into the
local intent folder. Follow "Word conversion → Word to markdown" in the `intent-bundle` skill. Only built-in tools
are used. Formatting may differ slightly from run to run, and that's fine: content is what matters.

Check that the converted file still contains these headings: `## Problem`, `## Proposed outcome`,
`## Affected users and systems`, `## Constraints`, `## Out of scope`. If any are missing, warn the PM which ones, but
still sync, because the PM owns the content.

## Step 5 — Push

- **In:** the converted `intent.md`.
- **Out:** a commit on `main` and a one-line report.

```sh
R=<repoDir>
git -C "$R" add "<repoPath>/intent.md"
```

Before committing, compare the new file with the published copy (`git -C "$R" diff --cached`). If the only
differences are formatting (whitespace, bullet characters, blank lines, emphasis markup), run
`git -C "$R" restore --staged --worktree "<repoPath>/intent.md"` and report **no changes**. Otherwise, commit:

```sh
git -C "$R" commit -m "intent(<issue>): sync <short>"
```

Then run `git -C "$R" push origin HEAD:main`. If the push is rejected, run
`git -C "$R" pull --rebase` and push once more. If it fails again, stop and show the error.

Report one line: **synced** (with a link to the file on GitHub), **no changes** or **failed**.
