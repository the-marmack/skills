# intent-create reference

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step              | Command                                                                                                                        | `intent-bundle` recipe                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Preflight         | `gh auth status`                                                                                                               | Local layout, GitHub recipes                                              |
| Name              | Look for `~/Documents/intents/*-<short>/` and, on GitHub, `intents/*-<short>/`                                                 | Local layout, GitHub recipes: List a folder                               |
| Issue first       | `gh label create intent` if missing, `gh issue create -R <owner>/<pmRepo> --title "Intent: <title>" --label intent`            | None: `add-to-project` adds the card                                      |
| Bare intent       | Fill [../templates/intent.md](../templates/intent.md) (Request only), `gh api graphql --input commit.json`, `gh issue comment` | Frontmatter, GitHub recipes: Commit to main                               |
| Door              | Apply the `intent-interview` skill with the issue, `short` and `request`                                                       | Required sections                                                         |
| Review            | Read `intent.md` from `main`, `check.py --ready` (if Python), one question                                                     | Ready gate                                                                |
| Write local files | Build `intent.docx` from `main`, write `.intent.json` with `syncedSha`                                                         | Word conversion → Markdown to Word, GitHub recipes: Last commit of a file |
| Hand off          | `open` on macOS, `explorer` on Windows                                                                                         | None                                                                      |
