# intent-lock reference

## Resolve IDs

```sh
P=<project.number>; O=<project.owner>
PID=$(gh project view "$P" --owner "$O" --format json -q .id)
Q='.fields[]|select(.name=="Status")'
FID=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.id")
CREATE=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.create>\").id")
READY=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.ready>\").id")
PLAN=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.plan>\").id")
```

If `.config.json` has no `statuses.plan`, use `Plan`.

The item ID is `itemId` in `.intent.json`. If that is missing or stale, look it up by the issue URL:

```sh
ITEM=$(gh project item-list "$P" --owner "$O" --limit 1000 --format json \
  -q ".items[]|select(.content.url==\"$URL\").id")
```

If the item is still missing, add it with `gh project item-add "$P" --owner "$O" --url "$URL" --format json -q .id`.

The current Status:

```sh
STATUS=$(gh project item-list "$P" --owner "$O" --limit 1000 --format json \
  -q ".items[]|select(.id==\"$ITEM\").status")
```

## Set status

```sh
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$FID" --single-select-option-id "$READY"
```

Use `$CREATE` for revoke. A `project` scope error means the PM must run `gh auth refresh -s project`.

## Sync the lock

The PM repo's `.github/workflows/intent-lock.yaml` reads the issue's Status from the board and adds or removes
`intents/<issue>-<short>/intent.lock` to match. Only that workflow writes the lock. Dispatch it and wait for it:

```sh
REPO=<owner>/<pmRepo>; N=<issue>
gh workflow run intent-lock.yaml -R "$REPO" -f issue="$N"
sleep 5
RUN=$(gh run list -R "$REPO" --workflow intent-lock.yaml --event workflow_dispatch --limit 1 --json databaseId -q '.[0].databaseId')
gh run watch "$RUN" -R "$REPO" --exit-status
```

If the workflow is missing from the repo, ask an admin to add it. Never write or delete `intent.lock` by hand.

## Lock file

`intents/<issue>-<short>/intent.lock` is JSON written by the workflow:

```json
{
    "status": "Plan",
    "lockedBy": "<who dispatched the run>",
    "lockedAt": "<UTC ISO-8601 timestamp>",
    "commit": "<last commit that changed intent.md>",
    "issue": "<issue url>",
    "run": "<workflow run url>"
}
```

The lock only means anything to the intent-sync skill, which refuses to push a locked intent. Nothing stops a plain
`git push`. Stronger enforcement is tracked in the-marmack/intents#1.
