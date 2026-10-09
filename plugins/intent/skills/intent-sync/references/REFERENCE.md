# intent-sync reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step         | Command                                                                                                      | `intent-bundle` recipe                                |
| ------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 1 Preflight  | `gh auth status`, `gh repo clone` or `git pull --rebase`                                                     | Local layout, Repo location, Git identity             |
| 2 Select     | List `~/Documents/intents/*/.intent.json`, leaving out intents locked on GitHub `main`                       | Local layout, Lock check                              |
| 3 Lock check | `gh api repos/<owner>/<pmRepo>/git/trees/main?recursive=1`                                                   | Lock check                                            |
| 4 Convert    | `textutil -convert html -stdout intent.docx` on macOS, `tar -xf intent.docx` on Windows                      | Word conversion → Word to markdown, Required sections |
| 5 Push       | `git add`, `git diff --cached`, `git commit -m "intent(<issue>): sync <short>"`, `git push origin HEAD:main` | None                                                  |
