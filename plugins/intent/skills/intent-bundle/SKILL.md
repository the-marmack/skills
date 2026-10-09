---
name: intent-bundle
description: Defines what a PM intent is and holds the recipes the intent skills share — the ~/Documents/intents layout and .config.json, the intent-<user> repo clone, the intent.md sections and when each is good enough, the board statuses Create, Ready, Plan, In progress, Test and Done, the lock.yaml that planning writes to the-marmack/intents, and Word conversion. Checks one intent and reports which required sections are good enough, weak or missing, without changing it. Use when someone asks whether an intent is complete or ready to promote, what an intent holds, where its files live or how its lock works. Not for creating (intent-create), filling in (intent-interview), syncing (intent-sync), promoting or revoking (intent-lock) or planning (plan-create) an intent.
license: MIT
---

# Intent bundle

The contract for an intent, and the recipes the other intent skills share. It is not a door: it never creates, edits
or publishes an intent. The recipes are in [references/REFERENCE.md](references/REFERENCE.md).

## Bundle

- **Local folder:** `~/Documents/intents/<issue>-<short>/` holds only `intent.docx` (the PM's Word door, plus
  backups) and `.intent.json`. `intent.md` on `main` is the truth, not the Word file.
- **Repo folder:** `intents/<issue>-<short>/` on `main` of `<owner>/<pmRepo>` holds `intent.md`, generated from the
  Word file. While the intent is planned or built, its lock is in `the-marmack/intents` (see "Locked"). Only
  `intent.md` is allowed there today; `sources.md` and `design/` are reserved for later.
- **Frontmatter:** `intent.md` starts with YAML frontmatter: `door` and `harness` (free text, which door and tool
  wrote this version) and an optional `supersedes`. See "Frontmatter".
- **Sections:** `intent.md` has Request, Problem, Proposed outcome, Affected users and systems, Constraints, Out of scope
  and Open questions. It holds no status.
- **Complete:** every required section is good enough, as defined in "Required sections".
- **Ready:** complete, no open question marked `(blocking)`, and only allowed files in the folder. See "Ready gate";
  planning refuses an intent that fails it.
- **Status** lives on the board: Create → Ready → Plan → In progress → Test → Done. Promoting moves Create to Ready,
  planning moves Ready to Plan, and the build moves it on from there.
- **Locked:** exactly when `the-marmack/intents` has `intents/<login>-<issue>-<short>/lock.yaml` on `main`, whatever
  the card's column. `plan-create` writes it when planning starts, and only `/intent-revoke` removes it. Check with
  "Lock check".

## Shared recipes

| Recipe                          | Used by                                      |
| ------------------------------- | -------------------------------------------- |
| Local layout and `.config.json` | every intent skill                           |
| Repo location                   | every intent skill                           |
| Frontmatter                     | intent-create, intent-interview, intent-sync |
| Required sections               | intent-create, intent-interview, intent-sync |
| Ready gate                      | the check below, plan-create                 |
| Git identity                    | intent-create, intent-sync, intent-lock      |
| Board                           | intent-create, intent-lock                   |
| Lock check                      | intent-sync, intent-interview, intent-lock   |
| Remove the central lock         | intent-lock                                  |
| Word conversion                 | intent-create, intent-interview, intent-sync |
| Changed on GitHub, Refresh      | intent-sync, intent-interview                |

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
4. End with one line from "Ready gate": `Ready gate: pass`, or `Ready gate: fail — <reasons>`. Run
   `python3 scripts/check.py --ready < intent.md` from this skill first and include its errors in the reasons.
5. Change nothing. For gaps, suggest the `intent-interview` skill, or editing `intent.docx` and running `/intent-sync`.
