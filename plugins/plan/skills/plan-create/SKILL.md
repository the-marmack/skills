---
name: plan-create
description: Turn a promoted (Ready) PM intent into a technical plan for AI agents — check the issue and its board card, run the ready gate, lock it by writing lock.yaml (pinned to the intent's commit) to the-marmack/intents and move the card to Plan, read the intent at that commit, find the existing repo in the the-marmack GitHub org where the work belongs (or ask which new repo to create), survey that repo, and break the intent into small ordered tasks with acceptance criteria traced to the intent's success criteria, written to plans/<pm-repo>/<issue>-<short-name>/plan.md in a clone of the central the-marmack/intents repo. Use when someone wants to plan, break down, scope, or hand off an intent to AI, or runs /plan-create. Not for writing or editing the intent itself (intent-create, intent-interview, intent-sync), promoting or revoking it (intent-lock), or doing the implementation work.
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
- **Out:** an up-to-date checkout of `the-marmack/intents`, the board settings, and confirmed planner rights.

1. Run `gh auth status`. If it fails, ask the user to run `gh auth login` and stop.
2. Check that `git rev-parse --show-toplevel` is a clone of `the-marmack/intents` (`gh repo view --json nameWithOwner`).
   If it isn't, stop and ask the user to run planning from a clone of it (`gh repo clone the-marmack/intents`). Then
   run `git pull --rebase --quiet`.
3. Planning runs as the planner's own `gh` login. Check the rights in "Planner rights" in the reference: push to `main`
   of `the-marmack/intents` and write access to the board. If either is missing, stop and say which.
4. Use the board from "Board" in the reference.

## Step 2 — Select intent

- **In:** an optional issue URL or `intent-<user>#<issue>`.
- **Out:** `pmRepo`, `login` (`pmRepo` without `intent-`), `issue`, `url` and `title`.

- **An argument was given:** parse it into `pmRepo` and `issue`.
- **No argument:** list the board items whose Status is `Ready` or `Plan` (see "List plannable intents" in the
  reference), showing each title, status and `<pmRepo>#<issue>`, and ask which one (use the interactive question UI).
  Mark any that already have a plan. If there are none, say so and stop.

## Step 3 — Lock

- **In:** `pmRepo`, `login` and `issue`.
- **Out:** `intents/<login>-<issue>-<short>/lock.yaml` on `main` of `the-marmack/intents`, its `sha`, and the card in
  `Plan`.

Planning locks the intent first, so it can't change under the plan. The lock is `lock.yaml` in `the-marmack/intents`,
pinned to the exact commit of `intent.md` it was planned from. It is written once and never rewritten. Follow "Lock" in
the reference; every step uses `gh` and nothing is cloned.

1. **Refuse early**, with a one-line reason and no changes, when the issue is closed, when it has no `intent` label, or
   when its card isn't in `Ready` and there's no lock yet. A card in `Create` means the PM must run `/intent-promote`
   (or move the card to Ready) first.
2. **Reuse an existing lock:** if `intents/<login>-<issue>-*/lock.yaml` exists on `main`, read its `sha` and go to
   step 6. Never rewrite it, even if `intent.md` has changed since: locked means locked.
3. **Pin the intent:** find the last commit that changed `intents/<issue>-<short>/intent.md` on `main` of `pmRepo`, and
   read the file at that commit.
4. **Gate:** run the gate script ("Gate" in the reference) on that text, then judge each required section against the
   `intent-bundle` skill's "Required sections". If either fails, stop and show the reasons. Nothing is locked.
5. **Write the lock** ("Lock file" in the reference) to `main` of `the-marmack/intents`. If GitHub says the file now
   exists, someone locked it first: re-read it, and continue only if its `sha` is the one you pinned. Otherwise refuse
   with "already locked at `<sha>`".
6. **Move the card to `Plan`** ("Move to Plan"), unless it's already in Plan or a later column.
7. **Transition:** while the PM repo still has the `intent-lock` workflow, also run "Sync the lock", so the PM-side
   skills, which still read `intent.lock` in the PM repo, see the intent as locked. A failed run is a warning, not a
   stop.

## Step 4 — Read intent

- **In:** the lock.
- **Out:** `short`, `intentPath`, the intent's markdown at the locked `sha`, and `lockCommit` (the lock's `sha`).

1. Read `intent.md` at the lock's `sha` (see "Read the intent" in the reference), never the head of `main`. If `main`
   has moved on since, say that later edits aren't part of this plan.
2. If `plans/<pmRepo>/<issue>-<short>/plan.md` already exists, ask whether to replace it or stop.

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

If planning is abandoned, an unlock is a revoke: the PM runs `/intent-revoke`, which removes the lock and moves the
card back. Don't delete `lock.yaml` here.
