# intent-pat-pm

Intents written by **pat-pm**. You never need git here: the `intent` plugin does the GitHub work for you through the
`gh` command, which is all you need installed (`gh auth login` once).

| Command           | What it does                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `/intent-create`  | Opens an issue here, interviews you section by section, and gives you a Word file to edit.  |
| `/intent-sync`    | Publishes your Word edits. It warns you first if the intent changed on GitHub since.        |
| `/intent-refresh` | Rebuilds your Word file from GitHub, keeping the old one as a backup.                       |
| `/intent-promote` | Publishes your last Word edits and moves the card to **Ready**: your approval for planning. |

## What's true

`intents/<issue>-<short-name>/intent.md` on `main` is the intent. Your Word file in
`~/Documents/intents/<issue>-<short-name>/` is one way to edit it, the interview is another, and you can also edit
`intent.md` on GitHub directly. No plugin? [docs/basic-path.md](docs/basic-path.md) shows how to write an intent in the
browser.

## Approving and the lock

Moving an intent's card to **Ready** on the board (or running `/intent-promote`) is your approval. When engineering
starts planning it, the intent is locked in [the-marmack/intents](https://github.com/the-marmack/intents) for good. To
change it after that, start a new intent that replaces it: `/intent-create … supersedes <the old issue's URL>`. To drop
an intent, close its issue as not planned.

New to this? Start with the
[getting-started guides](https://github.com/the-marmack/intents/tree/main/docs/getting-started).

_This repo was set up by `/intent-repo-setup`; re-running it brings these files up to date._
