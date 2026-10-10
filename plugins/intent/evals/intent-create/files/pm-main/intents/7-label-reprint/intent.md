---
door: interview
harness: claude-code
---

# Intent: One-click label reprint

**Author:** Pat PM

**Date:** 2026-10-07

**Issue:** <https://github.com/the-marmack/intent-themarmack/issues/7>

## Request

Warehouse staff waste about 20 minutes a shift re-printing shipping labels because the printer queue drops jobs. I want
reprints to be one click from the order screen.

## Problem

Warehouse staff lose about 20 minutes a shift re-printing shipping labels, because the printer queue drops jobs.

## Proposed outcome

Staff can reprint any shipping label from the order screen with one click.

Success criteria:

- A reprint takes one click from the order screen.
- A reprinted label reaches the printer in under 5 seconds.

## Affected users and systems

- Warehouse staff
- The order screen
- The label print service

## Constraints

- Must reuse the existing label print service.

## Out of scope

- Replacing the printers or the printer queue.

## Open questions

- Should reprints be logged for audit? (owner: Pat PM)
