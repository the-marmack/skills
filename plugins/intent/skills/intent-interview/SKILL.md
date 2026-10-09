---
name: intent-interview
description: Fills in a PM's intent by chat — drafts every required section (problem, proposed outcome with testable success criteria, affected users and systems, constraints, out of scope) from the PM's own words, then asks only about the gaps, in at most three batched rounds with a recommended answer for each question, and parks anything unsettled under Open questions. It is the default door of intent-create; on its own it fills the gaps in an existing unlocked intent, rewrites its intent.docx and publishes it with intent-sync. Use when a PM wants to fill in, complete, flesh out or continue an intent by answering questions. Not for starting a new intent (intent-create), publishing Word edits (intent-sync), checking an intent without changing it (intent-bundle), promoting or revoking (intent-lock) or planning (plan-create).
license: MIT
---

# Interview for an intent

The default door of the `intent-create` skill. It turns the PM's words into content for every required section. The
user is a product manager who doesn't know git, so speak in plain language. The section rules and Word conversion are
in the `intent-bundle` skill. The interview rules and the step map are in
[references/REFERENCE.md](references/REFERENCE.md).

## Input

- **From `intent-create`:** `request`, the PM's raw words.
- **On its own:** a short name, an issue number or `<issue>-<short>` of an existing intent. With none, list the
  unlocked intents the way the `intent-sync` skill does, and ask which one.

## Step 1 — Read

- **In:** the input.
- **Out:** the current content of every section.

- **From `intent-create`:** start from `request`. Nothing else exists yet.
- **On its own:** read `.config.json` and the intent's `.intent.json`, and pull `repoDir`, as described in the
  `intent-bundle` skill. Run "Lock check" in the `intent-bundle` skill, which reads `main` on GitHub, not the local
  clone. If it's locked, stop and tell the PM: "*(intent title)* is being planned and is locked. Run
  `/intent-revoke <short>` first if it needs changes." If it's unknown, stop and say the lock couldn't be confirmed.
  Otherwise read `intent.docx` into sections, following "Word conversion → Word to markdown" in the `intent-bundle`
  skill.

## Step 2 — Draft

- **In:** the current content.
- **Out:** a draft for every required section.

Draft each empty or weak section from what the PM has already said. Keep the PM's words. Never rewrite the Request.

## Step 3 — Interview

- **In:** the draft.
- **Out:** a filled answer for every required section, with leftovers moved to Open questions.

1. Check each required section against "Required sections" in the `intent-bundle` skill.
2. Ask about the gaps only, following "Interview rules" in [references/REFERENCE.md](references/REFERENCE.md).

## Step 4 — Hand back

- **From `intent-create`:** hand the sections back and stop. `intent-create` writes and publishes the files.
- **On its own:** rewrite `~/Documents/intents/<issue>-<short>/intent.docx` from the updated sections, following
  "Word conversion → Markdown to Word" in the `intent-bundle` skill, and keep the title, author, date and issue lines as
  they were. Then apply the `intent-sync` skill for this intent with door `interview`, so the published frontmatter
  says `door: interview` (see "Frontmatter" in the `intent-bundle` skill), and list any Open questions that are still unanswered.
