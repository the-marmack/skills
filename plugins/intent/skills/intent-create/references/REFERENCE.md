# intent-create reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step              | Command                                                                                                             | `intent-bundle` recipe                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Preflight         | `gh auth status`, `gh repo clone` or `git pull --rebase`                                                            | Local layout, Repo location, Git identity               |
| Name              | Look for `~/Documents/intents/*-<short>/` and `<repoDir>/intents/*-<short>/`                                        | Local layout                                            |
| Issue first       | `gh label create intent` if missing, `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent` | Board: Resolve IDs, Add the issue, Set status `$CREATE` |
| Door              | Apply the `intent-interview` skill with `request`                                                                   | Required sections                                       |
| Write local files | Fill [../templates/intent.md](../templates/intent.md), write `.intent.json`                                         | Word conversion → Markdown to Word                      |
| Publish           | `git add`, `git commit -m "intent(<issue>): create <short>"`, `git push origin HEAD:main`, `gh issue comment`       | None                                                    |
| Hand off          | `open` on macOS, `explorer` on Windows                                                                              | None                                                    |
