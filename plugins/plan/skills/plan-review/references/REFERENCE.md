# plan-review reference

Read-only. Every command below reads; none writes. Use `gh`'s built-in `-q` for JSON queries rather than `jq`.

## Step map

| Step      | Commands                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------- |
| 1 Load    | "Find the plan PR", "Read the plan", "Read the intent", "Read the target repo", "Read the guides" |
| 2 Answer  | None                                                                                              |
| 3 Check   | "Checks"                                                                                          |
| 4 Changes | None: people make the edits                                                                       |

## Find the plan PR

```sh
gh pr list -R the-marmack/intents --state open --json number,title,headRefName,isDraft \
  -q '.[]|select(.headRefName|startswith("plan/"))|[.number, .isDraft, .title]|@tsv'
gh pr view <n> -R the-marmack/intents --json title,body,state,headRefOid,files
```

## Read the plan

The plan's folder is `intents/<login>-<issue>-<short>/`, from the PR's files. Read at the PR's head commit, which works
for open and closed PRs alike:

```sh
H=<headRefOid>; F=intents/<login>-<issue>-<short>
gh api "repos/the-marmack/intents/contents/$F?ref=$H" -q '.[].name'          # plan*.md, plan*.json, lock.yaml
gh api "repos/the-marmack/intents/contents/$F/plan.md?ref=$H" -H "Accept: application/vnd.github.raw"
gh api "repos/the-marmack/intents/contents/$F/lock.yaml?ref=$H" -H "Accept: application/vnd.github.raw"
```

In a checkout of the PR (`gh pr checkout <n>`), reading the files from disk is the same thing.

## Read the intent

`lock.yaml` names the PM repo (`repository`), the file (`intent`) and the commit (`sha`):

```sh
gh api "repos/<repository>/contents/<intent>?ref=<sha>" -H "Accept: application/vnd.github.raw"
gh api "repos/<repository>/commits?path=<intent>&sha=main&per_page=1" -q '.[0].sha'   # differs from sha → changed since
```

## Read the target repo

```sh
T=<targetRepo from plan.json>
gh api "repos/$T/readme" -H "Accept: application/vnd.github.raw"          # 404: no README or new repo
gh api "repos/$T/git/trees/HEAD" -q '.tree[].path'                          # top-level layout
```

## Read the guides

```sh
for g in 4-review-a-plan 5-workflow; do
  gh api "repos/the-marmack/intents/contents/docs/getting-started/$g.md" -H "Accept: application/vnd.github.raw"
done
```

## Checks

Report each as **ok** or a finding with its location:

1. **plan.md ↔ plan.json:** the same task ids, titles, `dependsOn` and target repos; `intent.sha` matches `lock.yaml`.
2. **Traceability:** every success criterion and constraint of the intent (at the locked `sha`) appears in the
   Traceability table and maps to at least one existing task.
3. **Out of scope:** no task does something the intent lists under Out of scope.
4. **Order:** `Depends on` names only earlier tasks; nothing depends on a later task.
5. **Self-contained tasks:** each task has a goal, changes, acceptance checks and a verify command; no "see above".
6. **Leftovers:** no `{{…}}` placeholders; open questions name the tasks they block.
7. **Revisions:** if there are `plan_rev<N>` files, the newest one opens with what changed and why.

## Commit messages for reviewers' edits

Suggest one commit per change, `plan(<login>#<issue>): <what> — <why>`. Plan PRs are merged with rebase, not squash, so
these commits stay as the review record.
