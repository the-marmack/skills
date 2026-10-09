# plan-create reference

Use `gh`'s built-in `-q` for JSON queries rather than `jq`.

## Step map

| Step                    | Recipe below                                             |
| ----------------------- | -------------------------------------------------------- |
| 1 Preflight             | Board                                                    |
| 2 Select intent         | List plannable intents                                   |
| 3 Start planning (lock) | Move to Plan, Sync the lock                              |
| 4 Read intent           | Read the intent                                          |
| 5 Choose repo           | Find candidate repos                                     |
| 6 Survey repo           | Survey the target repo                                   |
| 7 Break down            | Task rules, [../templates/plan.md](../templates/plan.md) |
| 8 Review                | None                                                     |
| 9 Write plan            | plan.json, Publish                                       |

## Board

The intents board is the org project `the-marmack` #2 ("Intents (test)"). Its Status options are `Create`, `Ready`,
`Plan`, `In progress`, `Test` and `Done`. Promoted intents are `Ready`. Moving one to `Plan` starts planning and locks
it. An intent is locked exactly when its Status is `Plan` or any later status, and `intents/<issue>-<short>/intent.lock`
in the PM repo records that.

## List plannable intents

```sh
F='.items[]|select((.status=="Ready" or .status=="Plan") and .content.type=="Issue")'
gh project item-list 2 --owner the-marmack --limit 1000 --format json \
  -q "$F|[.status, .content.repository, .content.number, .content.title, .content.url, .id]|@tsv"
```

The last column is the item ID that "Move to Plan" needs.

`content.repository` is `the-marmack/<pmRepo>`. An item already has a plan when `plans/<pmRepo>/<number>-*/plan.md`
exists here.

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

## Sync the lock

The PM repo's `intent-lock` workflow reads the issue's Status and adds or removes `intent.lock` to match. Never write or
delete the lock yourself.

```sh
REPO=the-marmack/<pmRepo>; N=<issue>
gh workflow run intent-lock.yaml -R "$REPO" -f issue="$N"
sleep 5
RUN=$(gh run list -R "$REPO" --workflow intent-lock.yaml --event workflow_dispatch --limit 1 --json databaseId -q '.[0].databaseId')
gh run watch "$RUN" -R "$REPO" --exit-status
```

## Read the intent

```sh
O=the-marmack; R=<pmRepo>; I=<issue>
DIR=$(gh api "repos/$O/$R/contents/intents" -q ".[]|select(.type==\"dir\" and (.name|startswith(\"$I-\"))).name")
gh api "repos/$O/$R/contents/intents/$DIR/intent.md" -H "Accept: application/vnd.github.raw"
gh api "repos/$O/$R/contents/intents/$DIR/intent.lock" -H "Accept: application/vnd.github.raw"   # 404 = not promoted
```

`intent.lock` is JSON with `status`, `lockedBy`, `lockedAt`, `commit`, `issue` and `run`. Its `commit` (the last commit
that changed `intent.md`) is `lockCommit`, so the plan records exactly which version of the intent it was built from.

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

```json
{
    "intent": {
        "repo": "the-marmack/<pmRepo>",
        "issue": 1,
        "url": "<issue url>",
        "path": "intents/<issue>-<short>/intent.md",
        "lockCommit": "<intent.lock commit>"
    },
    "targetRepo": "the-marmack/<name>",
    "newRepo": false,
    "plannedBy": "<gh api user -q .login>",
    "plannedAt": "<UTC ISO-8601 timestamp>",
    "tasks": [{ "id": 1, "title": "…", "dependsOn": [], "repo": "the-marmack/<name>" }]
}
```

## Publish

Only after the user says yes:

```sh
git add "plans/<pmRepo>/<issue>-<short>"
git commit -m "plan(<pmRepo>#<issue>): plan <short>"
git push origin HEAD:main
PLAN="https://github.com/the-marmack/intents/blob/main/plans/<pmRepo>/<issue>-<short>/plan.md"
gh issue comment <intent url> --body "Plan ready: $PLAN (target repo: <targetRepo>)"
```
