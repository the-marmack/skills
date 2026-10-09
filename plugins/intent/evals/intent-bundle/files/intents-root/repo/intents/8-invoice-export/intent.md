# Intent: Export invoices as CSV

**Author:** Pat PM

**Date:** 2026-10-07

**Issue:** <https://github.com/the-marmack/intent-themarmack/issues/8>

## Request

Customers keep asking for a way to get their invoices into their accounting tools without retyping them.

## Problem

Finance admins at customer firms copy invoice data into their accounting tools by hand every month. Support tickets say
this takes about two hours each time.

## Proposed outcome

Finance admins can download their invoices as a CSV file from the billing page.

Success criteria:

- A finance admin can export one month of invoices as CSV in under 30 seconds.
- The CSV opens in Excel and Google Sheets without errors.

## Affected users and systems

Finance admins at customer firms, the billing page and the invoices API.

## Constraints

- An export must never include invoices from another customer's account.

## Out of scope

- PDF export
- Scheduled or emailed exports

## Open questions

- Should credit notes be part of the export? (owner: Pat PM)
