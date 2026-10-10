# intent-promote reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step                 | Command                                                               | `intent-bundle` recipe            |
| -------------------- | --------------------------------------------------------------------- | --------------------------------- |
| 1 Preflight          | `gh auth status`                                                      | Local layout, GitHub recipes      |
| 2 Resolve board item | `gh project view`, `gh project field-list`, `gh project item-list`    | Board: Resolve IDs, Find the item |
| 3 Guard              | The item's Status, then the lock check                                | Lock check                        |
| 4 Final sync         | Apply the `intent-sync` skill for this intent                         | None                              |
| 5 Move to Ready      | `gh project item-edit` with `$READY`                                  | Board: Set status                 |
| 6 Record             | `gh issue comment <url> --body "Promoted to **Ready** for planning."` | None                              |
