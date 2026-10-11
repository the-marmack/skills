---
name: intent-repo-setup
description: Admin setup for a PM's intent repository — creates or updates the-marmack/intent-<github-login> with gh only, idempotently: the private repo itself, the standard files (PM README, the no-plugin guide docs/basic-path.md, .claude/settings.json enabling the intent and plan plugins, the add-to-project workflow that puts intent issues on the board, the intent-check workflow that reports each pushed intent against the ready gate, intents/.gitkeep) committed in one commit, the intent and locked labels, the board App's secrets, a check that the App can see the repo, and access (write on their repo, read on the-marmack/intents). Re-running it brings an existing repo up to date and changes nothing that's already right. Use when an admin wants to onboard a new PM, set up, create, provision, repair or update a PM's intent repo, or runs /intent-repo-setup. Not for PMs writing intents (intent-create, intent-interview, intent-sync), promoting (intent-promote), or planning (plan-create).
user-invocable: false
license: MIT
---

# Set up a PM's intent repository

For **admins**. It replaces a template repository: a template copies files once and can't set labels, secrets, App
access or permissions, while this skill does all of it and can be re-run. Every step checks first and changes only
what's missing or out of date. It uses `gh` alone, with no clone and no git. The exact calls are in
[references/REFERENCE.md](references/REFERENCE.md); committing uses "Commit to main" in the `intent-bundle` skill.

## Input

The PM's GitHub login. The repo is `the-marmack/intent-<login>`. Stop if the login doesn't exist
(`gh api users/<login>`).

## Step 1 — Preflight

1. Run `gh auth status`. The admin needs to be an owner of `the-marmack` (creating repos, setting secrets and access).
2. The board is project #2 in `the-marmack` ("Board" in the `intent-bundle` skill).

## Step 2 — Repository

If `the-marmack/intent-<login>` doesn't exist, create it private with an initial commit ("Create the repository").
Otherwise leave it as it is. Never make it public, and never delete or rename anything.

## Step 3 — Files

Compare each file in [templates/](templates/) with the same path on `main` ("Template files" in the reference).

- **Missing:** add it.
- **Identical:** leave it.
- **Different:** show the PM-repo version next to the template's and ask the admin whether to overwrite it. The PM
  may have edited `README.md` on purpose. With nobody to answer, leave it and report it.

Commit every added or overwritten file in **one** commit with "Commit to main", headline
`chore: set up the intent repo`. In `README.md`, replace `{{login}}` with the PM's login first.

## Step 4 — Labels

Make sure the `intent` and `locked` labels exist ("Labels"). Existing labels are left as they are.

## Step 5 — Secrets

The `add-to-project` workflow needs `INTENT_LOCK_CLIENT_ID` and `INTENT_LOCK_PRIVATE_KEY` on the repo; org secrets
don't reach private repos on the free plan. List the repo's secrets ("Secrets"). Set only the missing ones: ask the
admin for the App's client id and the path to its `.pem` private key, and pipe the file into `gh secret set`. Never
print, echo, copy or commit the key.

## Step 6 — App access

Check that the board App can see the repo ("App access"). If it's installed on all repositories, nothing to do. If it's
installed on selected repositories and this one isn't among them, tell the admin to add it in the App's settings; it
can't be done here.

## Step 7 — Access

1. The PM gets **write** on their repo.
2. The PM gets **read** on `the-marmack/intents`: the intent skills check the lock there, and without read access
   every check fails closed.

Leave access that's already at least that level alone ("Access").

## Step 8 — Report

List each step as **created**, **updated**, **already fine** or **needs the admin** (with what to do). Remind the
admin that the board's "Item added to project" workflow must stay on with Status **Create**, and that the PM installs
`gh` and runs `gh auth login` once, then `/intent-create`.
