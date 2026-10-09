# plan-create reference

Use `gh`'s built-in `-q` for JSON queries rather than `jq`.

## Step map

| Step            | Recipe below                                             |
| --------------- | -------------------------------------------------------- |
| 1 Preflight     | Planner rights, Board                                    |
| 2 Select intent | List plannable intents                                   |
| 3 Lock          | Lock, Gate, Lock file, Move to Plan                      |
| 4 Read intent   | Read the intent                                          |
| 5 Choose repo   | Find candidate repos                                     |
| 6 Survey repo   | Survey the target repo                                   |
| 7 Break down    | Task rules, [../templates/plan.md](../templates/plan.md) |
| 8 Review        | None                                                     |
| 9 Publish       | plan.json, Publish                                       |

## Board

The intents board is the org project `the-marmack` #2 ("Intents (test)"). Its Status options are `Create`, `Ready`,
`Plan`, `In progress`, `Test` and `Done`. Promoted intents are `Ready`. Planning locks an intent by writing
`intents/<login>-<issue>-<short>/lock.yaml` to `main` of `the-marmack/intents`, then moves the card to `Plan`. The lock
file is the truth; the column is for people.

## Planner rights

Planning runs as the planner's own `gh` login, with no App. It needs push access to `main` of `the-marmack/intents` (for
`lock.yaml`), read access to the PM repos, and write access to the board:

```sh
gh api repos/the-marmack/intents -q .permissions.push   # must print true
gh auth status 2>&1 | grep -q "'project'" || echo "missing project scope: gh auth refresh -s project"
```

## List plannable intents

```sh
F='.items[]|select((.status=="Ready" or .status=="Plan") and .content.type=="Issue")'
gh project item-list 2 --owner the-marmack --limit 1000 --format json \
  -q "$F|[.status, .content.repository, .content.number, .content.title, .content.url, .id]|@tsv"
```

The last column is the item ID that "Move to Plan" needs.

`content.repository` is `the-marmack/<pmRepo>`. An item already has a plan when `intents/<login>-<number>-*/plan.md`
exists on `main` here, or an open PR's head branch starts with `plan/<login>-<number>-`.

## Move to Plan

```sh
PID=$(gh project view 2 --owner the-marmack --format json -q .id)
Q='.fields[]|select(.name=="Status")'
FID=$(gh project field-list 2 --owner the-marmack --format json -q "$Q.id")
OPT=$(gh project field-list 2 --owner the-marmack --format json -q "$Q.options[]|select(.name==\"Plan\").id")
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$FID" --single-select-option-id "$OPT"
```

Use `Ready` in place of `Plan` to move it back. A `project` scope error means the user must run
`gh auth refresh -s project`.

## Lock

Every call goes to GitHub; nothing is cloned. `<login>` is the PM repo name without `intent-`.

```sh
O=the-marmack; R=<pmRepo>; I=<issue>; L=<login>

# 1. Refuse early: the issue must be open and labelled intent
gh issue view "$I" -R "$O/$R" --json state,labels -q '[.state, ([.labels[].name]|join(","))]|@tsv'

# 2. Existing lock? (a folder <login>-<issue>-* with lock.yaml)
FOLDER=$(gh api repos/$O/intents/contents/intents -q ".[]|select(.type==\"dir\" and (.name|startswith(\"$L-$I-\"))).name")
[ -n "$FOLDER" ] && gh api "repos/$O/intents/contents/intents/$FOLDER/lock.yaml" -H "Accept: application/vnd.github.raw"

# 3. Pin the intent: the last commit that changed intent.md on main, and the file at that commit
DIR=$(gh api "repos/$O/$R/contents/intents" -q ".[]|select(.type==\"dir\" and (.name|startswith(\"$I-\"))).name")
SHA=$(gh api "repos/$O/$R/commits?path=intents/$DIR/intent.md&sha=main&per_page=1" -q '.[0].sha')
gh api "repos/$O/$R/contents/intents/$DIR/intent.md?ref=$SHA" -H "Accept: application/vnd.github.raw" > intent.md

# 5. Write the lock (see "Lock file"); base64 without line breaks
gh api -X PUT "repos/$O/intents/contents/intents/$L-$DIR/lock.yaml" \
  -f message="lock($L#$I): ${DIR#*-}" -f branch=main -f content="$(base64 < lock.yaml | tr -d '\n')"
```

A 404 in step 2 means there's no lock yet. The card's Status comes from "List plannable intents". If the PUT in step 5
answers 422 or 409, the file exists already: re-read it and compare its `sha` (SKILL.md, Step 3).

## Lock file

`intents/<login>-<issue>-<short>/lock.yaml` on `main` of `the-marmack/intents`:

```yaml
repository: the-marmack/intent-<login>
issue: 7
intent: intents/7-label-reprint/intent.md
sha: <commit SHA of intent.md at the head of main when it was locked>
locked_by: <planner's gh login>
locked_at: <UTC ISO-8601 timestamp>
```

It's written once and never rewritten. Only a revoke removes it.

## Gate

The intent must pass the ready gate (the `intent-bundle` skill, "Ready gate") before planning locks it. This skill
carries its own copy of the gate script, byte-identical to `intent-bundle`'s, because one plugin can't reach another
plugin's files by path:

```sh
python3 <skill dir>/scripts/check.py --ready < intent.md
```

Exit `0` means the structure passes. Exit `1` means it fails: stop and show the `errors` from its JSON output.

## Read the intent

Read `intent.md` at the lock's `sha`, never at the head of `main`:

```sh
gh api "repos/the-marmack/<pmRepo>/contents/<intent path from lock.yaml>?ref=<sha>" -H "Accept: application/vnd.github.raw"
```

`plan.json` records the lock's `sha`, so the plan says exactly which version of the intent it was built from.

## Find candidate repos

1. List the org's repos:

    ```sh
    gh repo list the-marmack --no-archived --limit 200 \
      --json name,description,primaryLanguage,repositoryTopics,pushedAt \
      -q '.[]|[.name, .description, .primaryLanguage.name, ([.repositoryTopics[]?.name]|join(",")), .pushedAt]|@tsv'
    ```

2. Leave out repos that hold intents or plans rather than product code: `intents` and every `intent-*` repo.
3. Pull search terms from the intent: the systems, screens and services named in **Affected users and systems**, the
   nouns in **Proposed outcome** and **Constraints** (for example "order screen", "label print service"), and their
   likely code spellings (`order`, `label`, `print`, `reprint`).
4. Search code in the org for the strongest three to five terms:

    ```sh
    gh search code --owner the-marmack "<term>" --limit 30 --json repository,path -q '.[]|[.repository.nameWithOwner, .path]|@tsv'
    ```

5. A repo is a candidate when its name, description, topics or code clearly match a named system or a constraint (for
   example "must reuse the existing label print service" points at the repo that holds that service). Rank by how many
   named systems it covers, then by recent activity. A repo that only shares generic words (`test`, `config`) is not a
   candidate.
6. Give each candidate a one-line reason, such as "has `src/orders/OrderScreen.tsx` and the label print client".

If several repos each own part of the work, recommend the one that owns the user-facing change. Name the others in the
plan's Approach and give their tasks a `Repo:` line.

## Survey the target repo

Read without cloning when you can. Clone shallowly into the scratchpad only when the tree is large:

```sh
T=the-marmack/<name>
gh api "repos/$T/git/trees/HEAD?recursive=1" -q '.tree[]|select(.type=="blob").path'
gh api "repos/$T/contents/<path>" -H "Accept: application/vnd.github.raw"
```

Read `README.md`, `AGENTS.md` or `CLAUDE.md`, the build or task files (`Makefile`, `mise.toml`, `tasks.toml`,
`package.json`, `go.mod`, `pyproject.toml`), CI workflows, and the code behind each affected system. Note the exact
commands for building, testing and linting, since every task's verification uses them.

## Task rules

Each task is handed to an AI agent that has only the plan, the intent and the repo. So:

- **Size:** one focused pull request, which an agent can finish in one session. If a task touches more than one area or
  needs more than about 400 changed lines, split it.
- **Order:** list tasks in a runnable order. `Depends on` names earlier task numbers only, and tasks without
  dependencies on each other can run in parallel.
- **Self-contained:** state the goal, the files or modules to change (real paths from the survey), the approach in a few
  bullets, and any decision already made. Never write "see above" or "as discussed".
- **Acceptance:** testable checks, each traced to an intent success criterion (`SC1`, `SC2`, …) or constraint (`C1`, …)
  where one applies. Use the intent's own numbers, such as "under 5 seconds", and don't loosen them.
- **Verification:** the exact commands the agent runs to prove the task is done (tests, lint, build).
- **Scope:** nothing from **Out of scope**. If a task looks like it needs something out of scope, raise it as an open
  question instead.
- **Measurement:** a success criterion that can only be measured after launch (for example "over two weeks") gets a task
  that adds the logging or metric needed to measure it, plus a line in the plan's Follow-up section.

## plan.json

`intents/<login>-<issue>-<short>/plan.json` (or `plan_rev<N>.json`), next to `plan.md`:

```json
{
    "intent": {
        "repo": "the-marmack/<pmRepo>",
        "issue": 1,
        "url": "<issue url>",
        "path": "intents/<issue>-<short>/intent.md",
        "sha": "<the sha in lock.yaml>",
        "lock": "intents/<login>-<issue>-<short>/lock.yaml"
    },
    "revision": 0,
    "targetRepo": "the-marmack/<name>",
    "newRepo": false,
    "plannedBy": "<gh api user -q .login>",
    "plannedAt": "<UTC ISO-8601 timestamp>",
    "tasks": [{ "id": 1, "title": "…", "dependsOn": [], "repo": "the-marmack/<name>" }]
}
```

`revision` is `0` for `plan.json` and `N` for `plan_rev<N>.json`.

## Publish

Through the API only: never clone, commit locally or push to `main`.

```sh
O=the-marmack; F=intents/<login>-<issue>-<short>; B=plan/<login>-<issue>-<short>   # add -rev<N> for a revision

# An open plan PR for this folder? Then add the files to its branch instead of creating one.
gh pr list -R $O/intents --state open --json number,headRefName -q ".[]|select(.headRefName|startswith(\"$B\"))"

# New branch from the head of main
MAIN=$(gh api repos/$O/intents/git/ref/heads/main -q .object.sha)
gh api repos/$O/intents/git/refs -f ref="refs/heads/$B" -f sha="$MAIN"

# Add each file (plan.md and plan.json, or the revision's pair) to the branch
gh api -X PUT "repos/$O/intents/contents/$F/plan.md" -f message="plan(<login>#<issue>): <short>" \
  -f branch="$B" -f content="$(base64 < plan.md | tr -d '\n')"

# Draft PR, then a comment on the intent
gh pr create -R $O/intents --draft --base main --head "$B" --title "plan(<login>#<issue>): <short>" \
  --body "Plan for <intent url>, locked at <sha> ($F/lock.yaml)."
gh issue comment <intent url> --body "Draft plan: <PR url> (target repo: <targetRepo>)"
```

When updating a file that already exists on the branch, pass its blob `sha` (`-f sha=…`) to the PUT.
