# intent-create reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step              | Command                                                                                                             | `intent-bundle` recipe                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Preflight         | `gh auth status`                                                                                                    | Local layout, GitHub recipes                |
| Name              | Look for `~/Documents/intents/*-<short>/` and, on GitHub, `intents/*-<short>/`                                      | Local layout, GitHub recipes: List a folder |
| Issue first       | `gh label create intent` if missing, `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent` | None: `add-to-project` adds the card        |
| Door              | Apply the `intent-interview` skill with `request`                                                                   | Required sections                           |
| Write local files | Fill [../templates/intent.md](../templates/intent.md), write `.intent.json`                                         | Word conversion → Markdown to Word          |
| Publish           | `gh api graphql --input commit.json` (createCommitOnBranch), `gh issue comment`                                     | GitHub recipes: Commit to main              |
| Hand off          | `open` on macOS, `explorer` on Windows                                                                              | None                                        |
