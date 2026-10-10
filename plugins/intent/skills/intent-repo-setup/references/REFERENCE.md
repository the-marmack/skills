# intent-repo-setup reference

`gh` only. `O=the-marmack`, `L=<github-login>`, `R=intent-$L`. Every check comes before its change, so a re-run on a
repo that's already right changes nothing.

## Step map

| Step         | Check                                                | Change (only when needed)                          |
| ------------ | ---------------------------------------------------- | -------------------------------------------------- |
| 1 Preflight  | `gh auth status`, `gh api users/$L`                  | None                                               |
| 2 Repository | `gh api repos/$O/$R` (404 = missing)                 | "Create the repository"                            |
| 3 Files      | "Template files": read each path on `main`           | One commit with `intent-bundle`'s "Commit to main" |
| 4 Labels     | `gh label list -R $O/$R`                             | `gh label create`                                  |
| 5 Secrets    | `gh secret list -R $O/$R` (names only)               | `gh secret set` from the admin's values            |
| 6 App access | `gh api orgs/$O/installations`                       | None here: the admin changes it in the UI          |
| 7 Access     | `gh api repos/$O/<repo>/collaborators/$L/permission` | `gh api -X PUT repos/$O/<repo>/collaborators/$L`   |

## Create the repository

```sh
gh api orgs/$O/repos -f name="$R" -F private=true -F auto_init=true \
  -f description="Intents authored by $L (managed by the intent plugin)."
```

`auto_init` gives `main` a first commit, so "Commit to main" has a head to build on.

## Template files

| Template in this skill          | Path in the PM repo                     | Notes                        |
| ------------------------------- | --------------------------------------- | ---------------------------- |
| `templates/README.md`           | `README.md`                             | Replace `{{login}}` with `L` |
| `templates/settings.json`       | `.claude/settings.json`                 |                              |
| `templates/add-to-project.yaml` | `.github/workflows/add-to-project.yaml` | Keep its SHA pin current     |
| `templates/gitkeep`             | `intents/.gitkeep`                      | Empty file                   |
| `templates/basic-path.md`       | `docs/basic-path.md`                    | The no-plugin guide          |

Read each one on `main` with `intent-bundle`'s "Read a file"; a 404 means missing. Compare after replacing `{{login}}`
and ignoring a trailing newline. Commit all the changes at once: "Commit to main" takes several `additions`.

## Labels

```sh
gh label create intent -R $O/$R --color 1D76DB --description "A PM intent" 2>/dev/null || true
gh label create locked -R $O/$R --color B60205 --description "Planning has locked this intent" 2>/dev/null || true
```

## Secrets

```sh
gh secret list -R $O/$R --json name -q '.[].name'     # names only; values can't be read back
gh secret set INTENT_LOCK_CLIENT_ID -R $O/$R --body "<client id>"
gh secret set INTENT_LOCK_PRIVATE_KEY -R $O/$R < "<path to the App's .pem>"
```

On Windows, `Get-Content <pem> -Raw | gh secret set INTENT_LOCK_PRIVATE_KEY -R $O/$R`. Never print the key, put it in a
command line or a file in the repo, or keep a copy.

## App access

```sh
gh api orgs/$O/installations -q '.installations[]|select(.app_slug=="the-marmack-intent-projects")|.repository_selection'
```

`all` means the App sees every repo. `selected` means the admin must add `$R` under the App's installation settings (Org
→ Settings → GitHub Apps → the-marmack-intent-projects → Configure → Repository access).

## Access

```sh
gh api repos/$O/$R/collaborators/$L/permission -q .permission          # admin, maintain, write, triage, read or none
gh api -X PUT repos/$O/$R/collaborators/$L -f permission=push           # write on their repo
gh api repos/$O/intents/collaborators/$L/permission -q .permission
gh api -X PUT repos/$O/intents/collaborators/$L -f permission=pull      # read on the-marmack/intents
```

Only add when the current level is lower. An org member gets the access directly; anyone else gets an invitation, which
the PM accepts on GitHub.
