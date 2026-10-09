# intent-sync reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step         | Command                                                                                   | `intent-bundle` recipe                                |
| ------------ | ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1 Preflight  | `gh auth status`                                                                          | Local layout, GitHub recipes                          |
| 2 Select     | List `~/Documents/intents/*/.intent.json`, leaving out intents locked on GitHub `main`    | Local layout, Lock check                              |
| 3 Lock check | `gh api repos/<owner>/intents/git/trees/main?recursive=1`                                 | Lock check                                            |
| 4 Convert    | `textutil -convert html -stdout intent.docx` on macOS, `tar -xf intent.docx` on Windows   | Word conversion → Word to markdown, Required sections |
| 5 Push       | Read the published file, then `gh api graphql --input commit.json` (createCommitOnBranch) | GitHub recipes: Read a file, Commit to main           |
