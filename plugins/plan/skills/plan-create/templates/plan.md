# Plan: {{title}}

**Intent:** [{{pmRepo}}#{{issue}}]({{url}}) · `{{intentPath}}` at `{{lockCommit}}`

**Target repo:** [{{targetRepo}}](https://github.com/{{targetRepo}})
{{"— new, created by Task 1" when newRepo is true; otherwise leave out}}

**Planned by:** {{author}} on {{date}}

## Summary

{{one paragraph: what will be built and how it meets the proposed outcome}}

## Approach

{{the design in a few bullets: where the change lives, key decisions, the stack for a new repo, other repos involved}}

## Tasks

### Task 1 — {{title}}

- **Repo:** {{targetRepo}}
- **Depends on:** none
- **Goal:** {{one sentence}}
- **Changes:** {{files and modules, with real paths}}
- **Approach:**
    - {{step}}
- **Acceptance:**
    - [ ] {{testable check}} ({{SC1 | C1}})
- **Verify:** `{{exact command}}`

<!-- Repeat the task block for each task, numbered in runnable order. -->

## Traceability

| Intent item                | Covered by |
| -------------------------- | ---------- |
| SC1: {{success criterion}} | Task {{n}} |
| C1: {{constraint}}         | Task {{n}} |

## Out of scope

Copied from the intent. No task may do these:

- {{item}}

## Open questions

- {{question}} — blocks Task {{n}}

## Follow-up

- {{post-launch measurement or check, with who owns it}}
