# intent-lock reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step                 | Command                                                                      | `intent-bundle` recipe                    |
| -------------------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| 1 Preflight          | `gh auth status`, `gh repo clone` or `git pull --rebase`                     | Local layout, Repo location, Git identity |
| 2 Resolve board item | `gh project view`, `gh project field-list`, `gh project item-list`           | Board: Resolve IDs, Find the item         |
| P2 Final sync        | Apply the `intent-sync` skill for this intent                                | None                                      |
| P3 Move to Ready     | `gh project item-edit` with `$READY`                                         | Board: Set status                         |
| P4 Record            | `gh issue comment <url> --body "Promoted to **Ready** for planning."`        | None                                      |
| R2 Move to Create    | `gh project item-edit` with `$CREATE`                                        | Board: Set status                         |
| R3 Unlock            | `gh workflow run intent-lock.yaml`, `gh run watch`, then `git pull --rebase` | Sync the lock, Lock file                  |
| R4 Record            | `gh issue comment <url> --body "Revoked: moved back to **Create**."`         | None                                      |
