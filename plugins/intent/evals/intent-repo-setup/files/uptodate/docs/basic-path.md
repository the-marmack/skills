# Writing an intent without the plugin

You can write an intent with nothing but GitHub in your browser. No git, no Word, no plugin.

## 1. Open the issue

On this repo's **Issues** tab, click **New issue**. Title it `Intent: <a few words>`, add the label **intent**, and put
your idea in a sentence or two in the description. Create it and note its number, for example **#12**. The card appears
on the Intents board in **Create** by itself.

## 2. Create the file

On the **Code** tab, click **Add file → Create new file**. Name it `intents/<number>-<short-name>/intent.md`, for
example `intents/12-label-reprint/intent.md` (short name: lowercase words joined by `-`). Paste this and fill it in:

```markdown
---
door: hand
harness: github-web
---

# Intent: <title>

**Author:** <your name>

**Date:** <today, YYYY-MM-DD>

**Issue:** <link to the issue>

## Request

<your idea in your own words>

## Problem

## Proposed outcome

Success criteria:

- <something we can check>

## Affected users and systems

## Constraints

## Out of scope

- <something this won't do>

## Open questions
```

## 3. Fill in each section

Each section is good enough when:

| Section                    | Good enough when                                                    |
| -------------------------- | ------------------------------------------------------------------- |
| Problem                    | It names who hurts, what hurts, and either evidence or "we believe" |
| Proposed outcome           | It states the result, with at least one testable success criterion  |
| Affected users and systems | At least one concrete group or system is named                      |
| Constraints                | It lists hard limits or says "None known"                           |
| Out of scope               | At least one exclusion is listed, or "Nothing excluded yet"         |

Park anything you can't settle under **Open questions**. Add `(blocking)` to a question only if planning can't start
without its answer: planning refuses an intent that still has one.

## 4. Save it

Click **Commit changes…**, keep **Commit directly to the main branch**, and commit. You can edit the file the same way
as often as you like until planning starts.

## 5. Approve it

When it's ready, move its card to **Ready** on the Intents board. That's your approval. Once planning starts the intent
is locked for good. To change it after that, write a new intent the same way and add `supersedes: <the old issue's URL>`
to its frontmatter; to drop it, close its issue as not planned.
