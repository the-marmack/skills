# intent-bundle reference

## Local layout

All intent-plugin skills use the same layout under `~/Documents/intents/` (on Windows,
`%USERPROFILE%\Documents\intents\`).

```text
~/Documents/intents/
  .config.json            # plugin settings, written on first run
  <issue>-<short-name>/
    intent.docx           # the PM's Word copy of intent.md on main; a door, not the truth
    intent.<YYYYMMDD-HHMM>.docx  # backups kept by "Refresh the Word file"
    .intent.json          # {"issue", "url", "title", "itemId", "repoPath", "syncedSha"}
```

The local intent folder holds only the Word file (and its backups) and `.intent.json`. The markdown lives in the PM
repo, at `intents/<issue>-<short-name>/intent.md` on `main`, and **that is the truth**: Word is one door into it, the
interview is another, and someone may edit it on GitHub by hand. `syncedSha` is the commit of `intent.md` that this
machine last wrote or refreshed from; "Changed on GitHub" compares it with `main`.

`.config.json`:

```json
{
    "owner": "the-marmack",
    "pmRepo": "intent-<github-login>",
    "project": { "owner": "the-marmack", "number": 2, "title": "Intents (test)" },
    "statuses": { "create": "Create", "ready": "Ready", "plan": "Plan" }
}
```

The first run creates this file:

- `owner` defaults to `the-marmack`.
- `pmRepo` defaults to `intent-$(gh api user -q .login)`. Check the repo exists with `gh repo view`. If it doesn't, stop
  and ask an admin to create it. Never create the repo yourself.
- For `project`, list the projects with `gh project list --owner <owner> --format json`. If exactly one title starts
  with `Intents`, use it without asking. Otherwise ask the PM which one to use.

## GitHub recipes

Every intent skill talks to GitHub through `gh` alone: no clone, no git, no shell script. A PM machine needs only the
`gh` CLI, logged in (`gh auth login`). If an old `.config.json` still has `repoDir`, ignore it and leave that folder
alone. `O` is `owner`, `R` is `pmRepo`, and `P` is the intent's `repoPath`.

**Working files:** write drafts (`intent.md`, the commit request) to the OS temp folder (`$TMPDIR` on macOS, `$env:TEMP`
on Windows), never into `~/Documents/intents/<issue>-<short>/`, which holds only the Word file, its backups and
`.intent.json`.

| Recipe                | `gh` (macOS and Windows alike)                                                                | GitHub MCP tool                                            |
| --------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Who am I              | `gh api user -q '{login: .login, name: .name}'`                                               | `get_me`                                                   |
| Read a file           | `gh api "repos/$O/$R/contents/$P/intent.md?ref=main" -H "Accept: application/vnd.github.raw"` | `get_file_contents`                                        |
| List a folder         | `gh api "repos/$O/$R/contents/intents?ref=main" -q '.[].name'`                                | `get_file_contents` (a folder)                             |
| Last commit of a file | `gh api "repos/$O/$R/commits?path=$P/intent.md&sha=main&per_page=1" -q '.[0].sha'`            | `list_commits` (with `path`)                               |
| Head of `main`        | `gh api "repos/$O/$R/git/ref/heads/main" -q .object.sha`                                      | `list_branches`                                            |
| Commit files          | "Commit to main" below                                                                        | `push_files` (several) or `create_or_update_file` (one)    |
| Create the issue      | `gh issue create -R $O/$R --title … --label intent --body-file <file>`                        | `create_issue`                                             |
| Comment               | `gh issue comment <n> -R $O/$R --body-file <file>`                                            | `add_issue_comment`                                        |
| Add or remove a label | `gh issue edit <n> -R $O/$R --add-label <l>` / `--remove-label <l>`                           | `update_issue`                                             |
| Board (Projects)      | "Board" below                                                                                 | none: use `gh`                                             |
| Lock check            | "Lock check" below                                                                            | `get_file_contents` on `intents/` in `the-marmack/intents` |

The MCP names are from github/github-mcp-server; check your server's tool list.

### Commit to main

One GraphQL call commits any number of files to `main` at once. GitHub signs the commit and authors it as the `gh`
login, so no git identity is needed. It is refused if `main` moved since you read it:

1. Read the head of `main` (`HEAD`) before you build the new content. For each later commit in the same run, use the
   commit SHA the previous one returned as `HEAD`: reading the branch right after a commit can still return the old head
   for a few seconds.
2. Base64-encode each file: `base64 < intent.md | tr -d '\n'` on macOS, or
   `[Convert]::ToBase64String([IO.File]::ReadAllBytes("intent.md"))` in PowerShell.
3. Write `commit.json` in the temp folder:

    ```json
    {
        "query": "mutation($i: CreateCommitOnBranchInput!) { createCommitOnBranch(input: $i) { commit { oid } } }",
        "variables": {
            "i": {
                "branch": { "repositoryNameWithOwner": "<owner>/<pmRepo>", "branchName": "main" },
                "expectedHeadOid": "<HEAD>",
                "message": { "headline": "intent(<issue>): <verb> <short>" },
                "fileChanges": { "additions": [{ "path": "<repoPath>/intent.md", "contents": "<base64>" }] }
            }
        }
    }
    ```

    Deletions go in `"deletions": [{ "path": "…" }]` next to `additions`.

4. `gh api graphql --input commit.json -q .data.createCommitOnBranch.commit.oid` prints the new commit's SHA.
5. If GitHub answers "Expected branch to point to …", `main` moved: wait a few seconds, then read the head and the file
   again. If the file hasn't changed, retry once with the new `HEAD`; if it has, stop and tell the PM someone else
   changed the intent.

## Required sections

These sections must have real content. Interview the PM about any that are missing or weak.

| Section                    | Good enough when                                                    |
| -------------------------- | ------------------------------------------------------------------- |
| Problem                    | It names who hurts, what hurts, and either evidence or "we believe" |
| Proposed outcome           | It states the result, with at least one testable success criterion  |
| Affected users and systems | At least one concrete group or system is named                      |
| Constraints                | It lists hard limits or says "None known"                           |
| Out of scope               | At least one exclusion is listed, or "Nothing excluded yet"         |

The **Request** is the PM's raw words, so never interview the PM about it. **Open questions** is where anything that
can't be settled now is parked.

An intent is **complete** when every required section is good enough. The published `intent.md` must also keep these
headings: `## Problem`, `## Proposed outcome`, `## Affected users and systems`, `## Constraints`, `## Out of scope`.

## Frontmatter

`intent.md` starts with YAML frontmatter. It records who wrote this version, never a status:

```yaml
---
door: interview # free text: interview, word, hand, …
harness: claude-code # free text: the tool that wrote this version (claude-code, codex, github-web, …)
supersedes: https://github.com/the-marmack/intent-<login>/issues/<n> # optional: the locked intent this replaces
---
```

- Each door sets `door` and `harness` when it writes `intent.md`: `intent-create` and `intent-interview` set
  `door: interview`, and `intent-sync` sets `door: word` (or the door its caller passes).
- Keep `supersedes` and any other key that is already there. Never drop the frontmatter.
- Word can't hold frontmatter, so it never goes into `intent.docx`. A Word sync takes it from the published `intent.md`
  (see "Word to markdown").

## Ready gate

An intent is **ready** to be planned when all of these hold:

1. It's complete: every required section is good enough (the table above, judged by the agent).
2. No line under `## Open questions` contains `(blocking)`. Mark a question `(blocking)` when planning can't start until
   it's answered.
3. The folder holds only allowed files. For now that's `intent.md` alone; `sources.md` and `design/` come later.

`plan-create` runs the gate before it locks an intent and refuses one that fails.

### Gate script

`scripts/check.py` in this skill checks the structural part. It's Python standard library only and never prompts:

```sh
python3 <skill dir>/scripts/check.py --ready < intent.md
```

**On a PM's machine it's optional**, because a PM needs only `gh`. Run it only when a real Python is already there, and
never start one that would prompt an install:

- **macOS:** `/usr/bin/python3` is a stub that pops up the Xcode Command Line Tools install. Run the script only if
  `xcode-select -p` succeeds or `command -v python3` is something other than `/usr/bin/python3`.
- **Windows:** `python` may be a Microsoft Store alias that opens the Store. Run the script only if `py -3 --version`
  succeeds, and call it as `py -3 <skill dir>/scripts/check.py`.

Without Python, apply the same structural rules yourself (the list below), and say the script didn't run. Planner
machines (the `plan` plugin's `plan-create`) always run their copy.

It prints one JSON object (`ok`, `ready`, `errors`, `warnings`, `frontmatter`, `sections`) and exits `0` when the check
passes, `1` when it fails and `2` on a usage error. It checks:

- the frontmatter has `door` and `harness`;
- the title starts with `# Intent:`;
- each required heading appears exactly once and isn't empty;
- `## Proposed outcome` has a `Success criteria:` line followed by `-` bullets;
- with `--ready`, no open question is marked `(blocking)`.

Without `--ready`, a blocking question is only a warning. Whether each section is _good enough_ stays the agent's
judgement: run the script first, then rate the sections against "Required sections".

## Board

The board is `project` in `.config.json`. Its Status options are `statuses.create`, `statuses.ready` and
`statuses.plan`, followed by `In progress`, `Test` and `Done`. **Locked statuses** are `statuses.plan` and every status
after it: planning has started. The lock itself is "Lock check", not the column. If `.config.json` has no
`statuses.plan`, use `Plan`. Use `gh`'s built-in `-q` for JSON queries rather than `jq`, which isn't installed by
default.

### Resolve IDs

```sh
P=<project.number>; O=<project.owner>
PID=$(gh project view "$P" --owner "$O" --format json -q .id)
Q='.fields[]|select(.name=="Status")'
FID=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.id")
CREATE=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.create>\").id")
READY=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.ready>\").id")
PLAN=$(gh project field-list "$P" --owner "$O" --format json -q "$Q.options[]|select(.name==\"<statuses.plan>\").id")
```

### Add the issue

```sh
ITEM=$(gh project item-add "$P" --owner "$O" --url "$URL" --format json -q .id)
```

### Find the item

The item ID is `itemId` in `.intent.json`. If that is missing or stale, look it up by the issue URL:

```sh
ITEM=$(gh project item-list "$P" --owner "$O" --limit 1000 --format json \
  -q ".items[]|select(.content.url==\"$URL\").id")
```

If the item is still missing, add it as in "Add the issue".

The current Status:

```sh
STATUS=$(gh project item-list "$P" --owner "$O" --limit 1000 --format json \
  -q ".items[]|select(.id==\"$ITEM\").status")
```

### Set status

```sh
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$FID" --single-select-option-id "$CREATE"
```

Use `$READY` or `$PLAN` for the other statuses. If `gh` reports a missing `project` scope, tell the PM to run
`gh auth refresh -s project` and then retry.

## Lock check

An intent is **locked** when `the-marmack/intents` has `intents/<login>-<issue>-<short>/lock.yaml` on `main`, written by
`plan-create` (`<login>` is `pmRepo` without `intent-`). Nothing in the PM repo records the lock.

Always ask GitHub. Never look in a local clone: it can be stale, and a lock can land after the last pull. One call reads
the whole `main` tree of `the-marmack/intents`:

```sh
O=<owner>; R=<pmRepo>; L=${R#intent-}; I=<issue>
Q='if .truncated then error("tree truncated") else .tree[].path end'
if C=$(gh api "repos/$O/intents/git/trees/main?recursive=1" -q "$Q" 2>&1)
then
  if printf '%s\n' "$C" | grep -Eq "^intents/$L-$I-[^/]+/lock\.yaml$"
  then STATE=locked; else STATE=unlocked; fi
else
  STATE=unknown   # no network, no access: $C holds the error
fi
```

To list every locked intent at once (for example to offer only unlocked ones), keep the `$C` list and match each intent
against it.

- **locked:** a lock exists. Block: don't change, sync or interview the intent.
- **unlocked:** the tree was read and has no lock for it.
- **unknown:** GitHub couldn't be read. Block as well, and tell the PM the lock couldn't be confirmed and to try again
  once `gh auth status` works. Never treat an error as unlocked. A PM needs read access to `the-marmack/intents`;
  without it every check is unknown, so ask an admin for it.

On Windows, run the same `gh api` call in PowerShell. A non-zero exit means unknown.

The lock only means anything to the intent skills, which refuse to change a locked intent. Nothing stops a plain
`git push` to the PM repo. Stronger enforcement is tracked in the-marmack/intents#1.

## Remove the central lock

Revoking deletes the central `lock.yaml`. That needs push access to `the-marmack/intents`; on 403 or 404, stop and tell
the PM to ask a planner to revoke it:

```sh
F=intents/<folder>/lock.yaml
BLOB=$(gh api "repos/the-marmack/intents/contents/$F" -q .sha)
gh api -X DELETE "repos/the-marmack/intents/contents/$F" -f message="unlock(<login>#<issue>): <short>" \
  -f sha="$BLOB" -f branch=main
```

## Changed on GitHub

Before a Word sync or an interview overwrites `intent.md`, check whether `main` moved since this machine last wrote or
refreshed it. Ask GitHub, never the local clone:

```sh
HEAD=$(gh api "repos/<owner>/<pmRepo>/commits?path=<repoPath>/intent.md&sha=main&per_page=1" -q '.[0].sha')
```

- `HEAD` equals `syncedSha` in `.intent.json`: nothing changed on GitHub; go ahead.
- They differ, or `syncedSha` is missing (an intent from before this field): `intent.md` changed on GitHub, through the
  interview, by hand or from another machine. Don't overwrite it silently. Warn the PM and offer **Refresh my Word
  file** (recommended) or **Overwrite anyway**.
- `gh` fails: say the check couldn't be done and stop. Never assume nothing changed.

## Refresh the Word file

Rebuild `intent.docx` from `intent.md` on `main`, so the PM edits the current version:

1. Rename the existing `intent.docx` to `intent.<YYYYMMDD-HHMM>.docx` (local time) in the same folder, so no Word edit
   is lost.
2. Read `intent.md` at `HEAD` from GitHub
   (`gh api "repos/<owner>/<pmRepo>/contents/<repoPath>/intent.md?ref=$HEAD" -H "Accept: application/vnd.github.raw"`).
3. Build the new `intent.docx` from it with "Markdown to Word" (the frontmatter stays out of Word).
4. Set `syncedSha` in `.intent.json` to `HEAD`.
5. Tell the PM the Word file now matches GitHub, and where the backup is.

## Word conversion

The conversion uses only what ships with the OS: `textutil` on macOS, and Word (via PowerShell) plus `tar` on Windows.
The output doesn't need to be byte-identical between runs. What matters is the intent's content.

### Markdown to Word (create)

Write the filled template as simple HTML in `<issue>-<short>/intent.html`, inside the local intent folder. Leave the
frontmatter out: Word can't hold it, and it stays in `intent.md`. Use only `h1`, `h2`, `p`, `ul`/`li`, `strong`, `em`
and `a`, and start the file with `<html><head><meta charset="utf-8"></head>`. Without the charset, dashes, accents and
curly quotes turn into garbage such as `â€”` in Word. Then convert it and delete the HTML file:

```sh
# macOS
textutil -convert docx -inputencoding UTF-8 intent.html -output intent.docx && rm intent.html
```

```powershell
# Windows (16 = wdFormatDocumentDefault)
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$d = $w.Documents.Open((Resolve-Path intent.html).Path)
$d.SaveAs2((Join-Path $PWD 'intent.docx'), 16); $d.Close(); $w.Quit(); Remove-Item intent.html
```

### Word to markdown (sync)

Extract the text with its structure, then write `intent.md` yourself to a working file (see "GitHub recipes"). Never
write an `intent.md` into the local intent folder:

```sh
# macOS: Word -> HTML on stdout
textutil -convert html -stdout intent.docx
```

```powershell
# Windows: a .docx is a zip; read the document body XML (tar ships with Windows 10+)
$t = New-Item -ItemType Directory (Join-Path $env:TEMP ([guid]::NewGuid()))
tar -xf intent.docx -C $t word/document.xml; Get-Content (Join-Path $t 'word/document.xml') -Raw
```

Map the structure onto the template's shape:

- The title becomes `# Intent: …` and each section becomes a level-2 (`##`) heading. Lists become `-` bullets.
- macOS `textutil` HTML has no heading tags. Headings come back as short bold paragraphs and bullets as `•`, so match
  them against the template's section names.
- In Windows XML, the `w:pStyle` values `Heading1` and `Heading2` mark headings, and `w:numPr` marks list items.
- Keep the PM's words. Don't summarize, reorder or "improve" them.
- Start the file with the frontmatter of the currently published `intent.md`. Keep every key, set `door` to `word` (or
  the door the caller passed) and `harness` to the running tool. If the published file has no frontmatter, add one.
