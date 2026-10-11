---
name: intent-create
description: Create a new product intent for a PM — open a tracking issue labelled intent in their intent-<user> GitHub repo (the repo's add-to-project workflow puts it on the board in Create), commit a bare intents/<issue>-<short-name>/intent.md to main, hand over to the intent-interview door, which commits each required section (problem, proposed outcome with testable success criteria, affected users, constraints, out of scope) as the PM accepts it, review the result and the ready gate with the PM, then write ~/Documents/intents/<issue>-<short-name>/intent.docx for editing in Word. Use when a PM wants to create, start, draft, capture or write up a new intent, idea or feature request, or runs /intent-create. Not for filling in an existing intent (intent-interview), syncing edits (intent-sync), promoting one (intent-promote), or writing engineering plans and task breakdowns (plan-create).
user-invocable: false
license: MIT
---

# Create an intent

The user is a product manager. Do all of the GitHub work for them, through `gh` only (no clone, no
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

- **In:** the rough idea passed as the argument, if there is one, which may include `supersedes <issue URL>`.
- **Out:** `title`, `short`, `request`, and `supersedes` when it replaces a locked intent.

1. **Superseding:** if the argument says `supersedes <issue URL>`, or the PM wants to change an intent that's locked,
   follow "Supersedes" in the `intent-bundle` skill. The old issue must be in this PM's repo and its intent locked
   ("Lock check"); if it isn't locked, tell the PM to edit it instead (`/intent-sync` or the interview) and stop.
   Read the old `intent.md` from `main`; propose a title based on the old one. `request` is what the PM wants to
   change and why.
2. If no idea was passed, ask the PM to describe it in a sentence or two. Their words become `request`.
3. Propose a `title` (5–8 words) and a `short` name (kebab-case, at most 30 characters, matching
   `^[a-z0-9]+(-[a-z0-9]+)*$`). Confirm both with the PM in a single question.
4. If any `~/Documents/intents/*-<short>/` exists locally, or `intents/*-<short>/` exists on `main` on GitHub ("List a
   folder"), say so. Offer a
   different short name, or suggest `/intent-sync` if they meant to update that intent.

## Step 3 — Issue first

- **In:** `title` and `request`.
- **Out:** `issue` (the number) and `url`.

1. Run `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent` with a body of
   `## Request` followed by `request`, plus `Supersedes <old issue URL>` when superseding. If the `intent` label is
   missing, create it with `gh label create` first.
2. Don't touch the board. The PM repo's `add-to-project` workflow adds every issue labelled `intent` to the project,
   and the board's "Item added to project" workflow puts the card in `Create`. Record `itemId: null`; the
   other skills find the card when they need it ("Board → Find the item" in the `intent-bundle` skill).
3. **Superseding:** comment on the old issue: `Superseded by <new issue URL>. This intent stays locked; the new one
   replaces it once it's planned.`

## Step 4 — Bare intent

- **In:** `title`, `short`, `request`, `issue` and `url`.
- **Out:** `intents/<issue>-<short>/intent.md` on `main`, and the issue linking to it.

Every door works on a folder that already exists on GitHub, so publish a bare intent first:

1. Fill in [templates/intent.md](templates/intent.md): the frontmatter (`door: interview`, `harness`: the tool you're
   running in, such as `claude-code` or `codex`), the title, `author` (the `gh api user` name, or the login if no name
   is set), today's `date`, the issue URL and the **Request** (`request`, grammar and typos fixed only). Leave the
   other sections empty: keep their headings and the `Success criteria:` line, and drop the `{{…}}` hints.
   **Superseding:** add `supersedes: <old issue URL>` to the frontmatter, and copy the old intent's sections (Problem
   to Open questions) instead of leaving them empty, so the door starts from what was locked.
2. Write it to a working `intent.md` in the temp folder ("GitHub recipes"), never into the local intent folder, and
   commit it to `intents/<issue>-<short>/intent.md` on `main` with "Commit to main", headline
   `intent(<issue>): create <short>`.
3. Comment on the issue with a link to the file:
   `https://github.com/<owner>/<pmRepo>/blob/main/intents/<issue>-<short>/intent.md`.

## Step 5 — Door

- **In:** `issue`, `short` and `request`.
- **Out:** every required section filled on `main`, one commit per accepted section.

The door is a word in the request, such as "interview". With no door named, apply the `intent-interview` skill without
waiting for the PM to ask, and pass it the issue, `short` and `request`. It reads the bare intent from `main` and
commits each accepted section. Today the interview is the only door. When it hands back, continue with Step 6.

## Step 6 — Review

- **In:** `intent.md` on `main`.
- **Out:** an intent the PM has accepted.

Read `intent.md` from `main`, show it to the PM in plain language, and run the ready gate (the gate script with
`--ready` when a real Python is present, otherwise its rules; see "Ready gate" in the `intent-bundle` skill). Report the
result. Then ask one question: **accept, or edit a section?** An edit goes back to the `intent-interview` skill for that
section only, then returns here. At most three rounds.

## Step 7 — Write local files

- **In:** the accepted `intent.md` on `main`.
- **Out:** `~/Documents/intents/<issue>-<short>/` containing only `intent.docx` and `.intent.json`.

1. Build `~/Documents/intents/<issue>-<short>/intent.docx` from `intent.md` on `main`, using "Word conversion →
   Markdown to Word" in the `intent-bundle` skill. This uses only built-in tools, so nothing needs installing.
2. Write `.intent.json` with `{"issue", "url", "title", "itemId": null, "repoPath": "intents/<issue>-<short>",
   "syncedSha"}`, where `syncedSha` is the last commit of `intent.md` on `main` ("Last commit of a file").

## Step 8 — Hand off

Open `~/Documents/intents/<issue>-<short>/` for the PM: `open` on macOS, `explorer` on Windows. Then tell them:

- **Next step:** when the intent is ready, move its card to **Ready** on the board, or run `/intent-promote`. That's
  their approval; nothing is planned before it.
- To change it later: edit `intent.docx` in Word and run `/intent-sync`, or run the interview again.

List any Open questions that are still unanswered.
