# intent-create reference

## Local layout

All intent-plugin skills use the same layout under `~/Documents/intents/` (on Windows,
`%USERPROFILE%\Documents\intents\`).

```text
~/Documents/intents/
  .config.json            # plugin settings, written on first run
  .repo/                  # clone of the PM's intent-<user> repo; managed by the plugin, never edited by hand
  <short-name>/
    intent.docx           # the file the PM edits in Word; this is the source of truth
    intent.md             # generated from intent.docx; never edit by hand
    .intent.json          # {"issue", "url", "title", "itemId", "repoPath"}
```

`.config.json`:

```json
{
    "owner": "the-marmack",
    "pmRepo": "intent-<github-login>",
    "project": { "owner": "the-marmack", "number": 2, "title": "Intents (test)" },
    "statuses": { "create": "Create", "ready": "Ready" }
}
```

The first run creates this file:

- `owner` defaults to `the-marmack`.
- `pmRepo` defaults to `intent-$(gh api user -q .login)`. Check the repo exists with `gh repo view`. If it doesn't, stop
  and ask an admin to create it. Never create the repo yourself.
- For `project`, list the projects with `gh project list --owner <owner> --format json`. If exactly one title starts
  with `Intents`, use it without asking. Otherwise ask the PM which one to use.

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

## Interview rules (lighter than aidd-intent's capture-intent grill)

- Ask in **rounds**. Put every open question that doesn't depend on another answer into one batch. Use the interactive
  question UI when it exists; otherwise use a numbered list.
- Every question gets a **recommended answer** drawn from what the PM has already said. The PM can reply "yes" to accept
  it.
- Don't ask the PM what you can look up yourself, such as the repo contents or earlier intents in `.repo/intents/`.
- Use at most **three rounds**. After that, move whatever is still open into Open questions as `(owner: <author>)` and
  continue.
- Plain language. The PM doesn't know git, and never needs to.

## Git identity

Set it only inside `.repo/`, never with `--global`. Use the PM's GitHub noreply address:

```sh
R=~/Documents/intents/.repo
git -C "$R" config user.name "$(gh api user -q '.name // .login')"
git -C "$R" config user.email "$(gh api user -q .id)+$(gh api user -q .login)@users.noreply.github.com"
```

## GitHub project recipes

```sh
P=<project number>; O=<project owner>
PID=$(gh project view "$P" --owner "$O" --format json -q .id)
ITEM=$(gh project item-add "$P" --owner "$O" --url "$ISSUE_URL" --format json -q .id)
FID=$(gh project field-list "$P" --owner "$O" --format json -q '.fields[]|select(.name=="Status").id')
OID=$(gh project field-list "$P" --owner "$O" --format json \
  -q '.fields[]|select(.name=="Status").options[]|select(.name=="Create").id')
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$FID" --single-select-option-id "$OID"
```

If `gh` reports a missing `project` scope, tell the PM to run `gh auth refresh -s project` and then retry.

Use `gh`'s built-in `-q` for JSON queries rather than `jq`, which isn't installed by default.

## Word conversion

The conversion uses only what ships with the OS: `textutil` on macOS, and Word (via PowerShell) plus `tar` on Windows.
The output doesn't need to be byte-identical between runs. What matters is the intent's content.

### Markdown to Word (create)

Write the filled template as simple HTML in `<short>/intent.html`. Use only `h1`, `h2`, `p`, `ul`/`li`, `strong`, `em`
and `a`. Then convert it and delete the HTML file:

```sh
# macOS
textutil -convert docx intent.html -output intent.docx && rm intent.html
```

```powershell
# Windows (16 = wdFormatDocumentDefault)
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$d = $w.Documents.Open((Resolve-Path intent.html).Path)
$d.SaveAs2((Join-Path $PWD 'intent.docx'), 16); $d.Close(); $w.Quit(); Remove-Item intent.html
```

### Word to markdown (sync)

Extract the text with its structure, then write `intent.md` yourself:

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
