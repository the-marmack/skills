---
name: plan-create
description: Turn a promoted (Ready) PM intent into a technical plan for AI agents — move it to Plan on the board and run its repo's intent-lock workflow so the intent is locked, read the intent from its intent-<user> repo, find the existing repo in the the-marmack GitHub org where the work belongs (or ask which new repo to create), survey that repo, and break the intent into small ordered tasks with acceptance criteria traced to the intent's success criteria, written to plans/<pm-repo>/<issue>-<short-name>/plan.md in a clone of the central the-marmack/intents repo. Use when someone wants to plan, break down, scope, or hand off an intent to AI, or runs /plan-create. Not for writing or editing the intent itself (intent-create, intent-interview, intent-sync), promoting or revoking it (intent-lock), or doing the implementation work.
license: MIT
---

# Plan an intent

The user is an engineer or lead working in a clone of `the-marmack/intents`, where plans live. The plan is the hand-off
to AI agents that will do the work, so every task must stand on its own. What an intent holds and how its lock works is
in the intent plugin's `intent-bundle` skill. Commands, the repo-matching rules and the task rules are in
[references/REFERENCE.md](references/REFERENCE.md).

Each step below has its own inputs and outputs, so steps can be reordered, swapped or removed without touching the
others. If a step fails, stop and say in one sentence what went wrong and what to do about it.

## Step 1 — Preflight

- **In:** nothing.
- **Out:** an up-to-date checkout of `the-marmack/intents` and the board settings.

1. Run `gh auth status`. If it fails, ask the user to run `gh auth login` and stop.
2. Check that `git rev-parse --show-toplevel` is a clone of `the-marmack/intents` (`gh repo view --json nameWithOwner`).
   If it isn't, stop and ask the user to run planning from a clone of it (`gh repo clone the-marmack/intents`). Then
   run `git pull --rebase --quiet`.
3. Use the board from "Board" in the reference.

## Step 2 — Select intent

- **In:** an optional issue URL or `intent-<user>#<issue>`.
- **Out:** `pmRepo`, `issue`, `url` and `title`.

- **An argument was given:** parse it into `pmRepo` and `issue`.
- **No argument:** list the board items whose Status is `Ready` or `Plan` (see "List plannable intents" in the
  reference), showing each title, status and `<pmRepo>#<issue>`, and ask which one (use the interactive question UI).
  Mark any that already have a plan. If there are none, say so and stop.

## Step 3 — Start planning (lock)

- **In:** `pmRepo`, `issue` and the item's board Status.
- **Out:** the item in `Plan` and `intent.lock` committed in `pmRepo`.

Planning starts by locking the intent, so it can't change under the plan. The board decides and the lock file records
it, and only the PM repo's `intent-lock` workflow writes the lock.

- **Status is `Create`:** stop. The intent isn't promoted, so tell the user the PM must run `/intent-promote` first.
- **Status is `Ready`:** set it to `Plan` (see "Move to Plan" in the reference), then run "Sync the lock". If the run
  fails, set the Status back to `Ready`, show the run's link and stop.
- **Status is `Plan`:** planning is resuming. If `intent.lock` is missing, run "Sync the lock" to repair it.

## Step 4 — Read intent

- **In:** `pmRepo` and `issue`.
- **Out:** `short`, `intentPath`, the intent's markdown and `lockCommit`.

1. Find the `intents/<issue>-*` folder in `pmRepo` and read its `intent.md` and `intent.lock` (see "Read the intent" in
   the reference). `short` is the folder name after `<issue>-`.
2. If `intent.lock` is still missing, stop and say the lock didn't land.
3. If `plans/<pmRepo>/<issue>-<short>/plan.md` already exists, ask whether to replace it or stop.

## Step 5 — Choose repo

- **In:** the intent.
- **Out:** `targetRepo` (`the-marmack/<name>`) and `newRepo` (true or false).

1. Search the org for repos where this work belongs, following "Find candidate repos" in the reference.
2. **Candidates found:** ask one question listing up to four of them, best match first and marked `(Recommended)`, each
   with a one-line reason. The question's free-text answer is the override: the user can type any other repo name,
   existing or new. Say so in the question text.
3. **No candidates:** tell the user no existing repo fits, and ask what repo to create. Offer a recommended name
   (`short`, or a broader product name if the intent hints at one) and let them type their own.
4. Check the answer with `gh repo view the-marmack/<name>`. If it exists, `newRepo` is false; otherwise it's true. Never
   create the repo here. Creating it is the plan's first task.

## Step 6 — Survey repo

- **In:** `targetRepo` and `newRepo`.
- **Out:** notes on stack, layout, conventions, test and lint commands, and the code each affected system maps to.

- **Existing repo:** follow "Survey the target repo" in the reference. Find the concrete files and modules behind each
  item in the intent's **Affected users and systems**. Record anything the intent assumes but the repo doesn't have.
- **New repo:** choose a stack from the intent's constraints and the org's existing repos, and propose it in the plan's
  Approach section. Base it on `the-marmack/aidd-template` unless the user says otherwise.

## Step 7 — Break down

- **In:** the intent and the survey notes.
- **Out:** a draft plan filled from [templates/plan.md](templates/plan.md).

1. Write the Summary and Approach: how the outcome will be met in this repo, and any design choice an agent would
   otherwise have to guess.
2. Split the work into tasks following "Task rules" in the reference. If `newRepo` is true, task 1 creates and scaffolds
   the repo.
3. Fill the traceability table. Every success criterion and every constraint must map to at least one task, and nothing
   in **Out of scope** may appear in any task.
4. Copy the intent's open questions that still matter, add new ones from the survey, and mark which tasks each one
   blocks.

## Step 8 — Review

- **In:** the draft plan.
- **Out:** a plan the user has approved.

Show the task list (number, title, depends on) and the target repo, and ask one question: approve, or what to change.
Apply the changes and ask again, at most three rounds. Don't ask what you can look up in the repo.

## Step 9 — Write plan

- **In:** the approved plan.
- **Out:** `plans/<pmRepo>/<issue>-<short>/plan.md` and `plan.json`, and a short report.

1. Write `plan.md`, and `plan.json` as described in "plan.json" in the reference.
2. Report the path, the target repo (and whether it still has to be created), the task count, and any blocking open
   questions. Offer to commit the plan, push it, and comment on the intent's issue with a link (see "Publish" in the
   reference). Do that only when the user says yes.

If planning is abandoned, move the item back to `Ready` and run "Sync the lock" so the PM can edit the intent again.
