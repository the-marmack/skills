---
name: intent-interview
description: Fills in a PM's intent by chat, one section at a time, straight on GitHub — reads intent.md from main, drafts each required section (problem, proposed outcome with testable success criteria, affected users and systems, constraints, out of scope) from the PM's own words, asks only about the gaps with a recommended answer for each question, and commits each accepted answer to main as it goes, parking anything unsettled under Open questions. It is the default door of intent-create; on its own it continues any unlocked intent from its short name, issue number or issue URL. Use when a PM wants to fill in, complete, flesh out or continue an intent by answering questions. Not for starting a new intent (intent-create), publishing Word edits (intent-sync), checking an intent without changing it (intent-bundle), promoting (intent-promote) or planning (plan-create).
user-invocable: false
license: MIT
---

# Interview for an intent

The default door of the `intent-create` skill. It turns the PM's words into content for every required section and
puts each answer on GitHub as soon as the PM accepts it, so nothing is lost if the chat stops halfway. The user is a
product manager, so speak in plain language and keep git out of it. `intent.md` on `main` is the truth; the section
rules, the frontmatter, the GitHub recipes and Word conversion are in the `intent-bundle` skill. The interview rules
and the step map are in [references/REFERENCE.md](references/REFERENCE.md).

## Input

- **From `intent-create`:** the issue number, `short` and `request`, the PM's raw words. `intent-create` has already
  committed a bare `intent.md` to `main`.
- **On its own:** a short name, an issue number, `<issue>-<short>`, an issue URL or `intent-<login>#<issue>`. With
  none, list the unlocked intents the way the `intent-sync` skill does, and ask which one.

## Step 1 — Read

- **In:** the input.
- **Out:** `pmRepo`, `repoPath`, the current `intent.md` from `main`, and the head of `main`.

1. Read `.config.json` (the `intent-bundle` skill). Resolve the intent: from a local `.intent.json` when there is one,
   otherwise find the `intents/<issue>-*` folder on `main` ("List a folder" in "GitHub recipes"). An issue URL also
   gives the repo.
2. Run "Lock check". If it's locked, stop and tell the PM: "*(intent title)* is being planned and is locked. To change
   it, start a new intent that supersedes it: `/intent-create … supersedes <issue URL>`." If it's unknown, stop and say
   the lock couldn't be confirmed.
3. Read `<repoPath>/intent.md` and the head of `main` from GitHub ("Read a file", "Head of `main`"). Never start from the
   Word file: the interview works on what's on `main`.

## Step 2 — Draft

- **In:** the current content, and `request` when there is one.
- **Out:** a draft for every required section.

Draft each empty or weak section from what the PM has already said. Keep the PM's words. Never rewrite the Request.

## Step 3 — Interview, one section at a time

- **In:** the draft.
- **Out:** every required section filled on `main`, one commit per accepted section, leftovers under Open questions.

Go through the required sections in order. Skip a section that is already good enough ("Required sections" in the
`intent-bundle` skill). **Superseding** (the frontmatter has `supersedes`): first ask the PM what should change from the
intent it replaces, and interview those sections even if they already look good enough; keep the rest as they are.
For each section to interview:

1. Show the draft and ask about its gaps only, following "Interview rules" in
   [references/REFERENCE.md](references/REFERENCE.md).
2. When the PM accepts it, update that section alone in the working `intent.md`. Set the frontmatter's `door` to
   `interview` and `harness` to the running tool ("Frontmatter"); keep every other key.
3. If a real Python is present, run the gate script without `--ready` for early feedback ("Gate script"), and mention
   any problem it finds in this section.
4. Commit it to `main` with "Commit to main", headline `intent(<issue>): interview <section>`. The new commit is the
   head for the next section. If GitHub says `main` moved, follow the recipe's retry rule.

Anything the PM can't settle goes under Open questions, as `(owner: <author>)`, in the same commit. Mark it
`(blocking)` only if planning can't start without the answer.

## Step 4 — Finish

- **From `intent-create`:** hand back to `intent-create`, which reviews the result with the PM. Stop here.
- **On its own:**
  1. Run the ready gate on the final `intent.md` (`--ready`, or its rules when there's no Python) and report it.
  2. If this machine has the intent's Word file, run "Refresh the Word file", so it matches `main` again.
  3. Never move the card. Tell the PM that moving it to **Ready** (or `/intent-promote`) is how they approve it, and
     list any Open questions that are still unanswered.
