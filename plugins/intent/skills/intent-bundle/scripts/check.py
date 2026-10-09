#!/usr/bin/env python3
"""Check the structure of an intent.md and, with --ready, the structural part of the ready gate.

Usage: python3 check.py [--ready] < intent.md

Prints one JSON object and exits 0 when the check passes, 1 when it fails, 2 on a usage error. Judging whether a
section is good enough stays with the agent; this only checks what can be checked mechanically. Standard library only,
no prompts. The copy in the plan plugin's plan-create skill must stay byte-identical (make lint checks it).
"""

from __future__ import annotations

import json
import re
import sys

REQUIRED = [
    "Problem",
    "Proposed outcome",
    "Affected users and systems",
    "Constraints",
    "Out of scope",
]
USAGE = "usage: check.py [--ready] < intent.md"


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, str, list[str]]:
    """Return (frontmatter or None, body, errors). Frontmatter is simple `key: value` lines between `---` fences."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, []
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text, ["frontmatter has no closing '---'"]
    meta: dict[str, str] = {}
    errors: list[str] = []
    for raw in lines[1:end]:
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or not key.strip() or key != key.strip():
            errors.append(f"frontmatter line is not 'key: value': {raw.strip()}")
            continue
        meta[key.strip()] = value.strip()
    return meta, "\n".join(lines[end + 1 :]), errors


def sections(body: str) -> dict[str, list[str]]:
    """Map each `## Heading` to the lines under it (headings may repeat; repeats are reported)."""
    found: dict[str, list[str]] = {}
    current = None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1)
            found.setdefault(current, [])
            found[current].append("\x00")  # marks a heading occurrence
            continue
        if current is not None:
            found[current].append(line)
    return found


def check(text: str, ready: bool) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    meta, body, fm_errors = split_frontmatter(text)
    errors += fm_errors
    if meta is None and not fm_errors:
        errors.append("no frontmatter: intent.md must start with '---' (door, harness)")
    elif meta is not None:
        for key in ("door", "harness"):
            if not meta.get(key):
                errors.append(f"frontmatter has no '{key}'")

    title = next((ln for ln in body.splitlines() if ln.strip()), "")
    if not title.startswith("# Intent:"):
        errors.append("the title must start with '# Intent:'")

    found = sections(body)
    report: dict[str, dict[str, bool]] = {}
    for name in REQUIRED:
        lines = found.get(name)
        present = lines is not None
        content = [ln for ln in (lines or []) if ln != "\x00" and ln.strip()]
        report[name] = {"present": present, "empty": present and not content}
        if not present:
            errors.append(f"missing section: ## {name}")
            continue
        if lines.count("\x00") > 1:
            errors.append(f"section appears more than once: ## {name}")
        if not content:
            errors.append(f"empty section: ## {name}")

    outcome = [ln for ln in found.get("Proposed outcome", []) if ln != "\x00"]
    after = None
    for i, ln in enumerate(outcome):
        if re.match(r"^\s*\**\s*success criteria\b", ln, re.IGNORECASE):
            after = outcome[i + 1 :]
            break
    if "Proposed outcome" in found and not (after and any(re.match(r"^\s*[-*]\s+\S", ln) for ln in after)):
        errors.append(
            "Proposed outcome has no success criterion: add a 'Success criteria:' line followed by '- ' bullets"
        )

    blocking = [ln.strip() for ln in found.get("Open questions", []) if ln != "\x00" and "(blocking)" in ln.lower()]
    if "Open questions" not in found:
        warnings.append("no '## Open questions' section")
    if blocking and not ready:
        warnings.append(f"{len(blocking)} open question(s) marked (blocking); the ready gate will fail")

    if ready:
        errors += [f"blocking open question: {q}" for q in blocking]
    return {
        "ok": not errors,
        "ready": (not errors) if ready else None,
        "errors": errors,
        "warnings": warnings,
        "frontmatter": meta or {},
        "sections": report,
    }


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args not in ([], ["--ready"]):
        print(USAGE, file=sys.stderr)
        return 2
    if sys.stdin.isatty():
        print(USAGE, file=sys.stderr)
        return 2
    result = check(sys.stdin.read(), ready=bool(args))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
