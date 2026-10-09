# intent-interview reference

## Interview rules (lighter than aidd-intent's capture-intent grill)

- Ask in **rounds**. Put every open question that doesn't depend on another answer into one batch. Use the interactive
  question UI when it exists; otherwise use a numbered list.
- Every question gets a **recommended answer** drawn from what the PM has already said. The PM can reply "yes" to accept
  it.
- Don't ask the PM what you can look up yourself, such as the repo contents or earlier intents in `intents/` on GitHub.
- Use at most **three rounds**. After that, move whatever is still open into Open questions as `(owner: <author>)` and
  continue.
- Plain language. The PM doesn't know git, and never needs to.

## Step map

Which command each step runs, and which recipe it follows. The recipes are in the `intent-bundle` skill.

| Step      | Command                                                                      | `intent-bundle` recipe                                      |
| --------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Read      | Lock check, then read `intent.md` and the head of `main` from GitHub         | Local layout, GitHub recipes, Lock check                    |
| Draft     | None                                                                         | Required sections                                           |
| Interview | Per accepted section: `check.py` (if Python), `gh api graphql --input …`     | Required sections, Frontmatter, Gate script, Commit to main |
| Finish    | `check.py --ready` (if Python); refresh `intent.docx` if this machine has it | Ready gate, Refresh the Word file                           |
