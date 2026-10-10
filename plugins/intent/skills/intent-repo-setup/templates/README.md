# intent-{{login}}

Intents written by **{{login}}**. You never need git here: the `intent` plugin does the GitHub work for you through the
`gh` command, which is all you need installed (`gh auth login` once).

| Command           | What it does                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `/intent-create`  | Opens an issue here, interviews you section by section, and gives you a Word file to edit.  |
| `/intent-sync`    | Publishes your Word edits. It warns you first if the intent changed on GitHub since.        |
| `/intent-refresh` | Rebuilds your Word file from GitHub, keeping the old one as a backup.                       |
| `/intent-promote` | Publishes your last Word edits and moves the card to **Ready**: your approval for planning. |
| `/intent-revoke`  | Takes an intent back to **Create**, and removes its lock if planning had already started.   |

## What's true

`intents/<issue>-<short-name>/intent.md` on `main` is the intent. Your Word file in
`~/Documents/intents/<issue>-<short-name>/` is one way to edit it, the interview is another, and you can also edit
`intent.md` on GitHub directly.

## Approving and the lock

Moving an intent's card to **Ready** on the board (or running `/intent-promote`) is your approval. When engineering
starts planning it, the intent is locked in [the-marmack/intents](https://github.com/the-marmack/intents) and can't be
changed here any more; `/intent-revoke` takes it back if you need to.

_This repo was set up by `/intent-repo-setup`; re-running it brings these files up to date._
