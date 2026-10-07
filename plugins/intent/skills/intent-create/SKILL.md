---
name: intent-create
description: Create a new product intent for a PM who has no git experience — open a tracking issue in their intent-<user> GitHub repo and put it on the project board in the Create column, interview them until the required sections (problem, proposed outcome with testable success criteria, affected users, constraints, out of scope) are covered, then write ~/Documents/intents/<short-name>/intent.docx for editing in Word and publish intents/<issue>-<short-name>/intent.md to their repo. Use when a PM wants to create, start, draft, capture or write up a new intent, idea or feature request, or runs /intent-create. Not for syncing edits to an existing intent (intent-sync), promoting, locking or revoking one (intent-lock), or writing engineering plans and task breakdowns.
license: MIT
---

# Create an intent

The user is a product manager who doesn't know git. Do all of the git and GitHub work for them, and speak in plain
language. The paths, `.config.json`, the section rules, the interview rules and the `gh project` recipes are in
[reference.md](reference.md).

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. If a step fails, stop and tell the PM, in one sentence, what went wrong and what to do about it.

## Step 1 — Preflight

- **In:** nothing.
- **Out:** a loaded `.config.json` and an up-to-date `.repo/`.

1. Run `gh auth status`. If it fails, ask the PM to run `gh auth login` and stop.
2. Load `~/Documents/intents/.config.json`. If it doesn't exist, create it as described in reference.md.
3. If `.repo/` is missing, run `gh repo clone <owner>/<pmRepo> ~/Documents/intents/.repo`. Otherwise run
   `git -C ~/Documents/intents/.repo pull --rebase --quiet`.
4. If `git -C ~/Documents/intents/.repo config user.email` is empty, set a repo-local identity using "Git identity" in
   reference.md. Most PMs have never configured git, and committing fails without an identity.

## Step 2 — Name

- **In:** the rough idea passed as the argument, if there is one.
- **Out:** `title`, `short` and `request`.

1. If no idea was passed, ask the PM to describe it in a sentence or two. Their words become `request`.
2. Propose a `title` (5–8 words) and a `short` name (kebab-case, at most 30 characters, matching
   `^[a-z0-9]+(-[a-z0-9]+)*$`). Confirm both with the PM in a single question.
3. If `~/Documents/intents/<short>/` already exists, or any `.repo/intents/*-<short>/` does, say so. Offer a
   different short name, or suggest `/intent-sync` if they meant to update that intent.

## Step 3 — Issue first

- **In:** `title` and `request`.
- **Out:** `issue` (the number), `url` and `itemId`.

1. Run `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent` with a body of
   `## Request` followed by `request`. If the `intent` label is missing, create it with `gh label create` first.
2. Add the issue to the project and set **Status** to `statuses.create`, using the recipe in reference.md. If the
   board update fails, keep going, warn the PM, and record `itemId: null`.

## Step 4 — Interview

- **In:** `request`.
- **Out:** a filled answer for every required section, with leftovers moved to Open questions.

1. Draft every section from `request` first.
2. Check each required section against the "good enough" table in reference.md.
3. Interview the PM about the gaps only, following the interview rules in reference.md (batched rounds, a
   recommended answer for each question, at most three rounds).

## Step 5 — Write local files

- **In:** the section content, `issue` and `url`.
- **Out:** `~/Documents/intents/<short>/` containing `intent.docx`, `intent.md` and `.intent.json`.

1. Fill in [templates/intent.md](templates/intent.md). Replace every `{{…}}`: `author` is the `gh api user` name (or
   its login if no name is set), and `date` is today's date. Write the result to `<short>/intent.md`.
2. Generate `intent.docx` from it using "Word conversion → markdown to Word" in reference.md. This uses only
   built-in tools, so nothing needs installing.

3. Write `.intent.json` with `{"issue", "url", "title", "itemId", "repoPath": "intents/<issue>-<short>"}`.

## Step 6 — Publish

- **In:** `<short>/intent.md` and `.intent.json`.
- **Out:** the intent pushed to `main` and linked from the issue.

```sh
R=~/Documents/intents/.repo
mkdir -p "$R/intents/<issue>-<short>"
cp ~/Documents/intents/<short>/intent.md "$R/intents/<issue>-<short>/intent.md"
git -C "$R" add "intents/<issue>-<short>"
git -C "$R" commit -m "intent(<issue>): create <short>"
git -C "$R" push origin HEAD:main
```

If the push is rejected, run `git -C "$R" pull --rebase` and push one more time. Then add a comment to the issue that
links to the file: `https://github.com/<owner>/<pmRepo>/blob/main/intents/<issue>-<short>/intent.md`.

## Step 7 — Hand off

Open the folder for the PM: `open` on macOS, `explorer` on Windows. Then tell them three things:

- Edit `intent.docx` in Word.
- Run `/intent-sync` to publish their changes.
- Run `/intent-promote` when the intent is ready.

List any Open questions that are still unanswered.
