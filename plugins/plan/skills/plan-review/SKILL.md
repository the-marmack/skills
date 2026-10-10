---
name: plan-review
description: Read-only companion for reviewing a draft plan PR in the-marmack/intents — loads the plan (plan.md, plan.json and any plan_rev files at the PR head), its lock.yaml, the intent at the locked commit from the PM's intent-<user> repo, the target repo's README and layout, and the getting-started review and workflow guides, then answers reviewers' questions about the plan with references to tasks, success criteria and constraints, and on request checks the plan for gaps (traceability, plan.md vs plan.json, out of scope, dependency order). It never edits, commits, pushes, comments or merges: people change the plan, one commit per change. Use when someone wants to review, understand, question, discuss or check a plan, open a plan PR to talk to it, or runs /plan-review. Not for writing a plan (plan-create), changing an intent (intent-create, intent-sync), or building the plan's tasks.
license: MIT
---

# Review a plan

A reviewer (a PM, planner or developer) wants to understand a draft plan and decide what should change. Load
everything the plan rests on, then answer their questions. **People are the door:** this skill never changes the
plan or anything else. When a reviewer wants a change, say exactly what to change and where, and they make the edit
themselves as its own commit, so the PR keeps a record of every review decision. The commands are in
[references/REFERENCE.md](references/REFERENCE.md).

## Step 1 — Load

- **In:** a plan PR number or URL in `the-marmack/intents`, or none.
- **Out:** the plan, its lock, the intent it was planned from, the target repo's outline and the review guides.

1. With no PR given, list the open draft plan PRs (`plan/*` branches) and ask which one.
2. Read the PR (title, body, files, head commit) and, at its head commit, every `plan*.md` and `plan*.json` in its
   folder plus `lock.yaml`. Reading at the head commit works even after the branch is gone.
3. Read the intent at the lock's `sha` from the PM repo in `lock.yaml` (`repository`, `intent`). That's the version
   the plan was built from; mention it if the intent has changed on `main` since.
4. Read the target repo's README and top-level layout (`targetRepo` in `plan.json`). For a new repo, say so.
5. Read `docs/getting-started/4-review-a-plan.md` and `docs/getting-started/5-workflow.md` from `the-marmack/intents`
   so you can explain the process too.
6. Give a short orientation: what the plan builds, the target repo, the number of tasks, open questions, and any
   revision files. Then invite questions.

## Step 2 — Answer

Answer in plain language, pointing at the plan's own words: task numbers, section names, the intent's success criteria
(`SC1` …) and constraints (`C1` …). When the plan doesn't say, say that rather than guessing. Useful kinds of answers:

- why a task exists, what it changes, what it depends on, and how it's verified;
- which tasks cover a success criterion or constraint, and which criteria a task serves;
- what the intent asked for that the plan treats as out of scope or as an open question;
- what in the target repo a task touches (from its README and layout).

## Step 3 — Check (when asked)

Run "Checks" in the reference and report each as **ok** or a finding with its location. This is a report only.

## Step 4 — Changes are made by people

When the reviewer wants something changed:

1. Say which file and section to edit (`plan.md` and the matching entry in `plan.json`), and suggest wording if asked.
2. Remind them to make the edit themselves, one change per commit, with a message saying what and why, such as
   `plan(<login>#<issue>): split task 3 — too big for one PR`, and to push to the PR branch.
3. Offer to run the checks again once they've pushed.

Never write, commit, push, comment on or merge anything, even if asked. If the reviewer insists, explain that plan
changes go through people so the PR records each decision.
