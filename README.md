# the-marmack skills

> Forked from [`bitwise-media-group/skills`](https://github.com/bitwise-media-group/skills) (MIT).

Agent skills and plugins from the-marmack, packaged as a marketplace for **Claude Code**, **OpenAI Codex CLI**, **Google
Antigravity**, and **OpenCode**.

Skills follow the [Agent Skills](https://agentskills.io) open standard (`SKILL.md` with portable frontmatter), live once
under `plugins/<plugin>/skills/`, and are delivered to each tool through its native mechanism — no duplicated content.

## Plugins

### golang

Modern, stdlib-first Go development conventions.

| Skill        | What it does                                                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `go-style`   | House style for Go: `%w` error wrapping, sentinels, `log/slog`, context threading, consumer interfaces, stdlib `net/http`, cobra + viper CLIs.    |
| `go-docs`    | Doc comments on every exported identifier, package comments in `doc.go`, and LLM-ready CLI reference generation for cobra tools.                  |
| `go-testing` | Table-driven tests with subtests, stdlib assertions, hand-written fakes, `httptest`, and native fuzz targets with seed corpora.                   |
| `go-project` | Scaffolds the canonical layout: `cmd/` + `internal/`, a pinned tools module (`go tool -modfile=tools/go.mod`), and a Makefile with the `pr` gate. |
| `go-release` | GoReleaser v2 with version ldflags, SBOMs, multi-arch images, SHA-pinned CI (`-race`, `govulncheck`), and Renovate coverage.                      |

### terraform

Conventions and workflows for authoring reusable Terraform modules.

| Skill                | What it does                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `terraform-style`    | House style for HCL: collection types, resource naming, `name_prefix`, `for_each` toggles, variable/output grouping, null defaults, file layout.  |
| `terraform-module`   | Scaffolds a new module with the canonical layout (`terraform.tf`, `main.tf`, `variables.tf`, `outputs.tf`, `README.md`) from commented templates. |
| `terraform-validate` | The fmt → init/validate → tflint loop, with a bundled provider-agnostic `tflint.hcl`.                                                             |

### python

Modern Python on the Astral toolchain (`uv`, `ruff`, `ty`/`pyright`).

| Skill            | What it does                                                                                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python-project` | Scaffolds the `src/` layout with `uv`: `pyproject.toml` on the `uv_build` backend, dev tools in a dependency group, and a Makefile `pr` gate.       |
| `python-style`   | House style enforced by `ruff format` + `ruff check`: the opinionated lint select set, `pathlib`, `logging`, and exception idioms.                  |
| `python-typing`  | Type every public API and gate it with `ty` or `pyright`: `[tool.ty]`/`[tool.pyright]` config, `X \| None`, PEP 695 generics, `Protocol` over ABCs. |
| `python-testing` | `pytest` with `@pytest.mark.parametrize`, fixtures, fakes over mocks, and Hypothesis property tests as the fuzzing analogue.                        |
| `python-docs`    | Google-style docstrings enforced via ruff `D` rules, and LLM-ready CLI reference generation for Typer/Click tools.                                  |
| `python-release` | `uv build` + `uv publish` via PyPI Trusted Publishing, SHA-pinned CI (`ruff`/`ty`/`pytest`), tag-driven releases, and Renovate coverage.            |

### intent

New here? The getting-started guides (software, building an intent, building and reviewing a plan, the whole workflow)
are in [the-marmack/intents/docs/getting-started](https://github.com/the-marmack/intents/tree/main/docs/getting-started)
(private: PMs and planners have access).

Intent authoring for product managers who don't use git. Intents live in each PM's private
`the-marmack/intent-<github-username>` repo. Each PM edits a Word file under
`~/Documents/intents/<issue>-<short-name>/`, and the plugin handles Word conversion (built-in OS tools only), git, the
issue and the project board. `intent.md` on `main` is the truth, and Word is one door into it. A PM needs only `gh`: the
skills talk to GitHub through its API, with no clone and no git. An intent is locked when planning has written its
`lock.yaml` to `the-marmack/intents`, so every PM needs read access to that repository; the skills check the lock on
GitHub, never in a clone.

| Skill               | What it does                                                                                                                                                                                                                                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `intent-create`     | Opens a tracking issue labelled `intent` (the repo's `add-to-project` workflow puts it on the board in Create), commits a bare `intents/<issue>-<short-name>/intent.md`, and hands over to a door, by default `intent-interview`. Then reviews the result and the ready gate with the PM, writes `intent.docx`, and tells them to move the card to Ready when it's done. |
| `intent-interview`  | The default door: works on `intent.md` on `main`, one section at a time, with a recommended answer for each question, and commits each accepted section straight away. On its own it continues any unlocked intent from its short name, issue number or issue URL.                                                                                                       |
| `intent-bundle`     | The contract every intent skill shares: the local and repo layout, the frontmatter, the required sections, the ready gate (with the `scripts/check.py` gate script), the board and the lock, and Word conversion. Checks an intent without changing it.                                                                                                                  |
| `intent-sync`       | Converts one intent's `intent.docx` to markdown and pushes it straight to `main`, after warning if `intent.md` changed on GitHub since the last sync (`intent.md` on `main` is the truth; Word is a door). `/intent-refresh` rebuilds the Word file from GitHub. With no name, lists the unlocked intents to pick from. Refuses locked intents.                          |
| `intent-promote`    | Publishes the last Word edits and moves the issue to **Ready**: the PM's approval. Once planning locks an intent it stays locked; a change is a new intent that supersedes it.                                                                                                                                                                                           |
| `intent-repo-setup` | **Admins:** creates or updates a PM's `intent-<login>` repo with `gh`: the private repo, its standard files (README, plugin settings, the `add-to-project` workflow), labels, the board App's secrets, App access, and the PM's access (write on their repo, read on `the-marmack/intents`). Safe to re-run.                                                             |

The plugin also ships the Claude Code commands `/intent-create`, `/intent-sync`, `/intent-refresh`, `/intent-promote`
and, for admins, `/intent-repo-setup` as thin entry points to these skills.

### plan

Planning for promoted intents, run from a clone of `the-marmack/intents`. The intent's format and lock are defined by
the intent plugin's `intent-bundle` skill.

| Skill         | What it does                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan-create` | Checks a **Ready** intent against the ready gate, locks it with `lock.yaml` in `the-marmack/intents` (pinned to the intent's commit) and moves it to **Plan**. Then picks the `the-marmack` repo where the work belongs and breaks the intent into small ordered tasks for AI agents, with acceptance criteria traced to the intent, as `plan.md` and `plan.json` next to the lock in `intents/<login>-<issue>-<short-name>/`, published as a draft pull request (revisions add `plan_rev1.md` and so on). |
| `plan-review` | Read-only companion for reviewing a draft plan PR: loads the plan, its lock, the intent at the locked commit, the target repo and the review guide, answers questions and checks the plan for gaps. It never edits: reviewers make each change as its own commit.                                                                                                                                                                                                                                          |

The plugin also ships the Claude Code commands `/plan-create` and `/plan-review` as thin entry points to the skills.

### workflow

Developer-workflow commands and skills, layered on the global Conventional-Commits and `commit.sh` conventions.

| Skill                      | What it does                                                                                                                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow-commit`          | Conventional Commit messages with a sandbox-safe `commit.sh` handoff: commit unsigned inside a worktree and re-sign via the script, or generate the `git add`/`git commit` script in the main checkout. |
| `workflow-security-report` | Triage a code-scanning (CodeQL) finding fetched via `gh`: an immutable report and index row with SHA-pinned permalinks, recommending remediation or dismissal.                                          |
| `workflow-skill-evals`     | Generate an evolve evaluation suite for an agent skill: Tier 1 triggers and Tier 2 behavioral evals under `evals/<skill>/`, deterministic-first, tracking the upstream evolve guide and JSON Schemas.   |

The plugin also ships matching Claude Code commands — `/commit` and `/security-report` — as thin entry points to these
skills.

## Installation

### Claude Code

```text
/plugin marketplace add the-marmack/skills
/plugin install terraform@the-marmack
```

### Codex CLI

```sh
codex plugin marketplace add the-marmack/skills
codex plugin add terraform@the-marmack
```

### OpenCode and Antigravity

Both read `.agents/skills/` natively. Clone this repo and symlink the skills in:

```sh
./install.sh                  # project scope: ./.agents/skills/ in the current directory
./install.sh --global         # user scope: ~/.agents/skills + ~/.gemini/skills
./install.sh --global --claude  # also link ~/.claude/skills
./install.sh --copy ...       # copy instead of symlink
```

Symlinked installs update on `git pull`. Alternatively,
[`npx skills add the-marmack/skills`](https://github.com/vercel-labs/skills) works as a zero-clone installer;
`install.sh` is the supported path.

## Evals

Each skill ships with evals under `plugins/<plugin>/evals/<skill>/`, run through the
[evolve](https://github.com/bitwise-media-group/evolve) CLI (`go tool evolve`, pinned in `tools/go.mod`):

- **Tier 0 — static lint** (run inside `make lint`): frontmatter, manifests, version sync. Runs in CI on every push.
- **Tier 1 — trigger accuracy** (`make triggers`): does the skill activate for the right prompts and stay quiet for
  near-misses? Real headless `claude -p` sessions.
- **Tier 2 — behavioral** (`make evals`): does following the skill produce correct artifacts? Graded deterministically
  (`terraform validate`, `tflint`, file/regex checks) with an optional LLM judge for subjective assertions.

Tiers 1–2 run per provider model (evolve's `--models anthropic|openai|google|all`, or specific model ids; default from
`.evolve.json`) and record token usage per eval via the provider token-counting APIs. Results land in each skill's
committed `results.json`; `make report` (`evolve report`) renders them into [`EVALUATION.md`](EVALUATION.md) +
`EVALUATION.json` (plugin-level rollup) and `plugins/<plugin>/EVALUATION.md` (per-eval detail).

Tiers 1–2 cost tokens and run via the manual `evals` GitHub workflow or locally.

## Contributing

See [AGENTS.md](AGENTS.md) for repository conventions: layout, dual Claude/Codex manifests, frontmatter policy, and the
eval requirements for new skills.

## License

[MIT](LICENSE)
