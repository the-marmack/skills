# intent-sync reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step         | Command                                                                                                      | `intent-bundle` recipe                                |
| ------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 1 Preflight  | `gh auth status`, `gh repo clone` or `git pull --rebase`                                                     | Local layout, Repo location, Git identity             |
| 2 Select     | List `~/Documents/intents/*/.intent.json` without an `intent.lock` in the repo                               | Local layout                                          |
| 3 Lock check | Look for `<repoDir>/<repoPath>/intent.lock`                                                                  | Lock file                                             |
| 4 Convert    | `textutil -convert html -stdout intent.docx` on macOS, `tar -xf intent.docx` on Windows                      | Word conversion → Word to markdown, Required sections |
| 5 Push       | `git add`, `git diff --cached`, `git commit -m "intent(<issue>): sync <short>"`, `git push origin HEAD:main` | None                                                  |
