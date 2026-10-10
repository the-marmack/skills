# Plan: One-click label reprint

**Intent:** [intent-themarmack#7](https://github.com/the-marmack/intent-themarmack/issues/7) ·
`intents/7-label-reprint/intent.md` at `abc1234`

**Target repo:** [the-marmack/label-reprint](https://github.com/the-marmack/label-reprint) — new, created by Task 1

## Summary

A reprint button on the order screen sends the existing label to the label print service again.

## Tasks

### Task 1 — Create the-marmack/label-reprint

- **Depends on:** none
- **Goal:** a repo that lints, tests and builds in CI.
- **Acceptance:**
    - [ ] CI passes on a first PR.
- **Verify:** `make lint && make test`

### Task 2 — Label print service client

- **Depends on:** 1
- **Goal:** reprint an existing label through the existing label print service.
- **Acceptance:**
    - [ ] Uses only the existing service's reprint call. (C1)
- **Verify:** `make test`

### Task 3 — Reprint endpoint with a 5-second budget

- **Depends on:** 2
- **Goal:** `POST /orders/:id/label/reprint` reaches the printer in under 5 seconds.
- **Acceptance:**
    - [ ] The printer accepts the job in under 5 seconds. (SC2)
- **Verify:** `make test`

### Task 4 — One-click button on the order screen

- **Depends on:** 3
- **Goal:** one click on the order screen calls the reprint endpoint.
- **Acceptance:**
    - [ ] A reprint takes one click. (SC1)
- **Verify:** `make test`

## Traceability

| Intent item                                 | Covered by |
| ------------------------------------------- | ---------- |
| SC1: one click from the order screen        | Task 4     |
| SC2: reaches the printer in under 5 seconds | Task 3     |
| C1: reuse the existing label print service  | Task 2     |

## Out of scope

- Replacing the printers or the printer queue.

## Open questions

- None.
