---
name: intent-create
description: Create a new product intent for a PM who has no git experience — open a tracking issue labelled intent in their intent-<user> GitHub repo (the repo's add-to-project workflow puts it on the board in Create), hand over to the intent-interview door until the required sections (problem, proposed outcome with testable success criteria, affected users, constraints, out of scope) are covered, then write ~/Documents/intents/<issue>-<short-name>/intent.docx for editing in Word and publish intents/<issue>-<short-name>/intent.md to their repo. Use when a PM wants to create, start, draft, capture or write up a new intent, idea or feature request, or runs /intent-create. Not for filling in an existing intent (intent-interview), syncing edits (intent-sync), promoting, locking or revoking one (intent-lock), or writing engineering plans and task breakdowns (plan-create).
license: MIT
---

# Create an intent

The user is a product manager who doesn't know git. Do all of the GitHub work for them, through `gh` only (no clone, no
git), and speak in plain language. This is the entry point of the intent flow: it prepares the issue, hands over to a
door skill for the content, then writes and publishes the files. The paths, `.config.json`, the GitHub recipes, the
section rules and the board recipes are in the `intent-bundle` skill. Which command and recipe each step uses is in
[references/REFERENCE.md](references/REFERENCE.md).

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. If a step fails, stop and tell the PM, in one sentence, what went wrong and what to do about it.

## Step 1 — Preflight

- **In:** nothing.
- **Out:** a loaded `.config.json`.

1. Run `gh auth status`. If it fails, ask the PM to run `gh auth login` and stop.
2. Load `~/Documents/intents/.config.json`. If it doesn't exist, create it as described in "Local layout" in the
   `intent-bundle` skill.
3. Nothing is cloned and git isn't needed: every GitHub step uses "GitHub recipes" in the `intent-bundle` skill.

## Step 2 — Name

- **In:** the rough idea passed as the argument, if there is one.
- **Out:** `title`, `short` and `request`.

1. If no idea was passed, ask the PM to describe it in a sentence or two. Their words become `request`.
2. Propose a `title` (5–8 words) and a `short` name (kebab-case, at most 30 characters, matching
   `^[a-z0-9]+(-[a-z0-9]+)*$`). Confirm both with the PM in a single question.
3. If any `~/Documents/intents/*-<short>/` exists locally, or `intents/*-<short>/` exists on `main` on GitHub ("List a
   folder"), say so. Offer a
   different short name, or suggest `/intent-sync` if they meant to update that intent.

## Step 3 — Issue first

- **In:** `title` and `request`.
- **Out:** `issue` (the number) and `url`.

1. Run `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent` with a body of
   `## Request` followed by `request`. If the `intent` label is missing, create it with `gh label create` first.
2. Don't touch the board. The PM repo's `add-to-project` workflow adds every issue labelled `intent` to the project,
   and the board's "Item added to project" workflow puts the card in `statuses.create`. Record `itemId: null`; the
   other skills find the card when they need it ("Board → Find the item" in the `intent-bundle` skill).

## Step 4 — Door

- **In:** `request`.
- **Out:** a filled answer for every required section, with leftovers moved to Open questions.

The door is a word in the request, such as "interview". With no door named, apply the `intent-interview` skill without
waiting for the PM to ask, and pass it `request`. Today the interview is the only door. When it hands the sections back,
continue with Step 5.

## Step 5 — Write local files

- **In:** the section content, `issue` and `url`.
- **Out:** `~/Documents/intents/<issue>-<short>/` containing only `intent.docx` and `.intent.json`, and a working copy
  of `intent.md` in the temp folder.

1. Fill in [templates/intent.md](templates/intent.md). Replace every `{{…}}`: `author` is the `gh api user` name (or
   its login if no name is set), `date` is today's date, `door` is the door used in Step 4 (`interview`), and `harness`
   is the tool you're running in (`claude-code`, `codex`, …). Write the result to a working `intent.md` in the temp
   folder ("GitHub recipes"), never into the local intent folder.
2. Generate `~/Documents/intents/<issue>-<short>/intent.docx` from it using "Word conversion → Markdown to Word" in the
   `intent-bundle` skill. This uses only built-in tools, so nothing needs installing.
3. Write `.intent.json` with `{"issue", "url", "title", "itemId", "repoPath": "intents/<issue>-<short>", "syncedSha": null}`.
   Step 6 fills in `syncedSha`.

## Step 6 — Publish

- **In:** the working `intent.md`.
- **Out:** the intent committed to `main` and linked from the issue.

Commit the working `intent.md` to `intents/<issue>-<short>/intent.md` on `main` with "Commit to main" in the
`intent-bundle` skill, headline `intent(<issue>): create <short>`. Set `syncedSha` in `.intent.json` to the commit it
returns. Then add a comment to the issue that links to the file:
`https://github.com/<owner>/<pmRepo>/blob/main/intents/<issue>-<short>/intent.md`.

## Step 7 — Hand off

Open `~/Documents/intents/<issue>-<short>/` for the PM: `open` on macOS, `explorer` on Windows. Then tell them three things:

- Edit `intent.docx` in Word.
- Run `/intent-sync` to publish their changes.
- Run `/intent-promote` when the intent is ready.

List any Open questions that are still unanswered.
