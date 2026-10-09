"""Tests for intent-bundle/scripts/check.py, run as a subprocess the way the skills call it."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"
SCRIPT = HERE.parents[1] / "skills" / "intent-bundle" / "scripts" / "check.py"
PLAN_COPY = HERE.parents[2] / "plan" / "skills" / "plan-create" / "scripts" / "check.py"


def run(fixture: str | None, *args: str, text: str | None = None) -> tuple[int, dict | None, str]:
    stdin = text if text is not None else (FIXTURES / fixture).read_text() if fixture else ""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True, check=False
    )
    out = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc.returncode, out, proc.stderr


def test_complete_intent_passes_and_is_ready() -> None:
    code, out, _ = run("complete.md", "--ready")
    assert code == 0
    assert out["ok"] is True and out["ready"] is True and out["errors"] == []
    assert out["frontmatter"]["door"] == "interview"
    assert all(s["present"] and not s["empty"] for s in out["sections"].values())


def test_ready_is_null_without_the_flag() -> None:
    code, out, _ = run("complete.md")
    assert code == 0 and out["ready"] is None


@pytest.mark.parametrize(
    ("fixture", "message"),
    [
        ("missing-section.md", "missing section: ## Constraints"),
        ("empty-section.md", "empty section: ## Affected users and systems"),
        ("no-success-criterion.md", "no success criterion"),
        ("no-frontmatter.md", "no frontmatter"),
        ("bad-title.md", "# Intent:"),
        ("duplicate-section.md", "more than once: ## Out of scope"),
    ],
)
def test_structural_failures(fixture: str, message: str) -> None:
    code, out, _ = run(fixture)
    assert code == 1
    assert out["ok"] is False
    assert any(message in e for e in out["errors"]), out["errors"]


def test_blocking_question_only_fails_the_ready_gate() -> None:
    code, out, _ = run("blocking-question.md")
    assert code == 0 and out["ok"] is True
    assert any("(blocking)" in w for w in out["warnings"])

    code, out, _ = run("blocking-question.md", "--ready")
    assert code == 1
    assert out["ready"] is False
    assert any(e.startswith("blocking open question:") for e in out["errors"])


def test_frontmatter_needs_door_and_harness() -> None:
    text = (FIXTURES / "complete.md").read_text().replace("harness: claude-code\n", "")
    code, out, _ = run(None, text=text)
    assert code == 1 and "frontmatter has no 'harness'" in out["errors"]


def test_unclosed_frontmatter_is_an_error() -> None:
    text = "---\ndoor: interview\n# Intent: x\n"
    code, out, _ = run(None, text=text)
    assert code == 1 and any("no closing" in e for e in out["errors"])


def test_frontmatter_keeps_extra_keys_and_ignores_comments() -> None:
    text = (
        (FIXTURES / "complete.md")
        .read_text()
        .replace(
            "harness: claude-code\n", "harness: claude-code # the tool\nsupersedes: https://example.test/issues/5\n"
        )
    )
    code, out, _ = run(None, text=text)
    assert code == 0
    assert out["frontmatter"]["harness"] == "claude-code"
    assert out["frontmatter"]["supersedes"] == "https://example.test/issues/5"


@pytest.mark.parametrize("args", [["--nope"], ["--ready", "extra"]])
def test_bad_usage_exits_2(args: list[str]) -> None:
    code, out, err = run("complete.md", *args)
    assert code == 2 and out is None and "usage" in err


def test_plan_create_copy_is_identical() -> None:
    assert PLAN_COPY.read_bytes() == SCRIPT.read_bytes()
