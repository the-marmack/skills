---
description:
    Plan a promoted intent — run the ready gate, lock it with lock.yaml in the-marmack/intents, break it into technical
    tasks an AI agent can pick up, choose (or name) the repo in the the-marmack org where the work happens, and write
    the plan under plans/.
argument-hint: [intent issue URL | intent-<user>#<issue>]
---

# Plan an intent

Apply the `plan-create` skill.

Which intent to plan (empty means list the Ready and Plan intents on the board and ask): $ARGUMENTS

Follow the skill's steps in order: preflight, select intent, lock, read intent, choose repo, survey repo, break down,
review, write plan.
