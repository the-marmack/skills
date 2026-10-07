# intent-lock reference

## Resolve IDs

```sh
P=<project.number>; O=<project.owner>
PID=$(gh project view "$P" --owner "$O" --format json -q .id)
Q='.fields[]|select(.name=="Status")'
FID=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.id")
CREATE=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.create>\").id")
READY=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.ready>\").id")
```

The item ID is `itemId` in `.intent.json`. If that is missing or stale, look it up by the issue URL:

```sh
ITEM=$(gh project item-list "$P" --owner "$O" --limit 1000 --format json \
  -q ".items[]|select(.content.url==\"$URL\").id")
```

If the item is still missing, add it with `gh project item-add "$P" --owner "$O" --url "$URL" --format json -q .id`.

## Set status

```sh
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$FID" --single-select-option-id "$READY"
```

Use `$CREATE` for revoke. A `project` scope error means the PM must run `gh auth refresh -s project`.

## Lock file

`intents/<issue>-<short>/intent.lock` is JSON:

```json
{
    "promotedBy": "<gh api user -q .login>",
    "promotedAt": "<UTC ISO-8601 timestamp>",
    "commit": "<git -C .repo rev-parse HEAD before the lock commit>",
    "issue": "<issue url>"
}
```

The lock only means anything to the intent-sync skill, which refuses to push a locked intent. Nothing stops a plain
`git push`. Stronger enforcement is tracked in the-marmack/intents#1.
