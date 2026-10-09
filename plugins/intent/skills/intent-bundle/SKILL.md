---
name: intent-bundle
description: Defines what a PM intent is and holds the recipes the intent skills share — the ~/Documents/intents layout and .config.json, the intent-<user> repo clone, the intent.md sections and when each is good enough, the board statuses Create, Ready, Plan, In progress, Test and Done, the intent.lock that the repo's intent-lock workflow writes, and Word conversion. Checks one intent and reports which required sections are good enough, weak or missing, without changing it. Use when someone asks whether an intent is complete or ready to promote, what an intent holds, where its files live or how its lock works. Not for creating (intent-create), filling in (intent-interview), syncing (intent-sync), promoting or revoking (intent-lock) or planning (plan-create) an intent.
license: MIT
---

# Intent bundle

The contract for an intent, and the recipes the other intent skills share. It is not a door: it never creates, edits
or publishes an intent. The recipes are in [references/REFERENCE.md](references/REFERENCE.md).

## Bundle

- **Local folder:** `~/Documents/intents/<issue>-<short>/` holds only `intent.docx`, the PM's source of truth, and
  `.intent.json`.
- **Repo folder:** `intents/<issue>-<short>/` on `main` of `<owner>/<pmRepo>` holds `intent.md`, generated from the
  Word file, and `intent.lock` while the intent is being planned or built.
- **Sections:** `intent.md` has Request, Problem, Proposed outcome, Affected users and systems, Constraints, Out of scope
  and Open questions. It holds no status.
- **Complete:** every required section is good enough, as defined in "Required sections".
- **Status** lives on the board: Create → Ready → Plan → In progress → Test → Done. Promoting moves Create to Ready,
  planning moves Ready to Plan, and the build moves it on from there.
- **Locked:** exactly when the Status is Plan or later (In progress, Test, Done). `intent.lock` records it, and only the
  PM repo's `intent-lock` workflow writes or removes it.

## Shared recipes

| Recipe                          | Used by                                      |
| ------------------------------- | -------------------------------------------- |
| Local layout and `.config.json` | every intent skill                           |
| Repo location                   | every intent skill                           |
| Required sections               | intent-create, intent-interview, intent-sync |
| Git identity                    | intent-create, intent-sync, intent-lock      |
| Board                           | intent-create, intent-lock                   |
| Lock check                      | intent-sync, intent-interview, intent-lock   |
| Sync the lock, Lock file        | intent-lock                                  |
| Word conversion                 | intent-create, intent-interview, intent-sync |

## Check an intent

- **In:** a short name, an issue number or `<issue>-<short>`.
- **Out:** a one-line verdict per required section. Nothing is changed.

1. Read `~/Documents/intents/.config.json`, resolve `repoDir` following "Repo location", and read the intent's
   `.intent.json`.
2. Read `<repoDir>/<repoPath>/intent.md`. It is the last synced version, so say that Word edits not yet synced aren't
   checked.
3. Rate each required section as **good enough**, **weak** or **missing** against "Required sections", with a short
   reason for anything that isn't good enough. Then report the lock state from "Lock check": it asks GitHub's `main`,
   never the local clone.
4. Change nothing. For gaps, suggest the `intent-interview` skill, or editing `intent.docx` and running `/intent-sync`.
