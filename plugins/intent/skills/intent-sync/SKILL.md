---
name: intent-sync
description: Publish a PM's edits to one intent at a time — convert its ~/Documents/intents/<issue>-<short-name>/intent.docx Word file to markdown using only built-in OS tools and commit it as intents/<issue>-<short-name>/intent.md straight to main in their intent-<user> GitHub repo through the GitHub API (gh only, no git or clone), warning first if intent.md changed on GitHub since the last sync. With no intent named, lists the unlocked intents and asks which one. Refuses to touch a locked intent, one whose lock.yaml is in the-marmack/intents (engineering has started planning it). Use when a PM wants to sync, save, publish, upload or push their intent changes, or runs /intent-sync. Not for creating a new intent (intent-create), promoting one (intent-promote), or general git pushes in code repositories.
license: MIT
---

# Sync intents to GitHub

The user is a product manager. Their Word file, `intent.docx`, is the source of truth. This skill
converts it to markdown and pushes it to `main`, and does the git work. The local layout, `.config.json` and Word
conversion are in the `intent-bundle` skill. Which command and recipe each step uses is in
[references/REFERENCE.md](references/REFERENCE.md).

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others.

## Step 1 — Preflight

- **In:** nothing.
- **Out:** `.config.json`.

1. Run `gh auth status`. If it fails, ask the PM to run `gh auth login` and stop.
2. Read `~/Documents/intents/.config.json`. If it is missing, tell the PM to run `/intent-create` first and stop.
3. Nothing is cloned and git isn't needed: every GitHub step uses "GitHub recipes" in the `intent-bundle` skill.

## Step 2 — Select

- **In:** an optional short-name argument, which may also contain the word `refresh`.
- **Out:** exactly one intent folder, and whether this is a refresh.

Sync publishes one intent at a time. An intent is **locked** when planning has started: `the-marmack/intents` holds its
`lock.yaml` (see the `intent-bundle` skill), so engineering is planning or building it and it can't change here. Find
out with "Lock check" in the `intent-bundle` skill, which reads GitHub. If the check comes back
unknown, say the lock couldn't be confirmed and stop.

- **A short name was given:** pick the `~/Documents/intents/*-<short>/` folder (an issue number or `<issue>-<short>`
  also works).
- **No argument:** list every child folder that has a `.intent.json` and isn't locked, showing each intent's title and
  `<issue>-<short>`, and ask the PM to pick one (use the interactive question UI when it exists). Leave locked intents
  out of the list. If none are unlocked, say so and stop.

A folder with an `intent.docx` but no `.intent.json` was never created through `/intent-create`, so never offer it.

**Refresh mode:** if the argument contains `refresh` (`/intent-sync refresh <short>`, or `/intent-refresh`), run
"Refresh the Word file" in the `intent-bundle` skill for this intent after Step 3 and stop. Nothing is pushed.

## Step 3 — Lock check

- **In:** the chosen intent's `repoPath` from `.intent.json`.
- **Out:** the intent, confirmed unlocked.

Run "Lock check" in the `intent-bundle` skill for this intent, right before converting. It reads `main` on GitHub.

- **locked:** stop and tell the PM: "*(intent title)* is being planned and is locked. To change it, start a new intent
  that supersedes it: `/intent-create … supersedes <issue URL>`."
- **unknown:** stop and tell the PM the lock couldn't be confirmed on GitHub, so nothing was synced.

Never edit, delete or bypass a lock here.

## Step 3b — Changed on GitHub?

- **In:** `syncedSha` from `.intent.json`.
- **Out:** the go-ahead to overwrite `intent.md`, or a refreshed Word file and a stop.

`intent.md` on `main` is the truth, and the Word file is one way to change it. Run "Changed on GitHub" in the
`intent-bundle` skill. If `main` moved since `syncedSha` (or `syncedSha` is missing), tell the PM: "*(intent title)*
changed on GitHub since your last sync. Syncing your Word file would overwrite those changes." Then ask (use the
interactive question UI when it exists):

- **Refresh my Word file** (recommended): run "Refresh the Word file" and stop. The PM re-applies their Word edits to
  the refreshed file and syncs again; their old file is kept as a backup.
- **Overwrite anyway:** continue to Step 4.

If nobody can answer, don't overwrite: report the question and stop.

## Step 4 — Convert

- **In:** `~/Documents/intents/<issue>-<short>/intent.docx`.
- **Out:** a fresh working `intent.md` in the temp folder.

Extract the Word file's content and write a working `intent.md` in the temp folder from it. Never write an `intent.md`
into the local intent folder. Word can't hold frontmatter, so start the file with the frontmatter of the currently
published `intent.md`: keep every key, set `door: word` (or the door the caller passed, such as `interview`) and
`harness` to the running tool. See "Frontmatter" in the `intent-bundle` skill. Follow "Word conversion → Word to
markdown" in the `intent-bundle` skill. Only built-in tools are used. Formatting may differ slightly from run to run,
and that's fine: content is what matters.

Check that the converted file still contains these headings: `## Problem`, `## Proposed outcome`,
`## Affected users and systems`, `## Constraints`, `## Out of scope`. If any are missing, warn the PM which ones, but
still sync, because the PM owns the content.

## Step 5 — Push

- **In:** the converted `intent.md`.
- **Out:** a commit on `main` and a one-line report.

Compare the new file with the published copy ("Read a file" in the `intent-bundle` skill). If the only differences are
formatting (whitespace, bullet characters, blank lines, emphasis markup), don't commit: report **no changes** and set
`syncedSha` to the `HEAD` from Step 3b.

Otherwise commit it to `<repoPath>/intent.md` on `main` with "Commit to main" in the `intent-bundle` skill, headline
`intent(<issue>): sync <short>`. If GitHub says `main` moved, follow that recipe's retry rule; if it still fails, stop
and show the error. Set `syncedSha` in `.intent.json` to the commit it returns.

Report one line: **synced** (with a link to the file on GitHub), **no changes** or **failed**.
