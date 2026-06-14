# Agent instructions (greenfield program)

This program is built by **concurrent Cursor agents** under a **Supervisor**. Human operators intervene on escalation only.

## Law

1. **`conformance/manifest.yaml`** in `mtg-ebay-docs` is authoritative over informal chat.
2. **No checkpoint PASS** without green proof in `conformance-report.json`.
3. **Secrets never** in git — see `08-accounts-and-secrets.md` in planning docs.
4. **Library boundary:** only `recognition/` + `adapters/` import `mtg_card_recognition`.
5. **Pipeline runs local;** Vercel receives **publish snapshots only** after success.

## Repos (multi-root workspace)

| Folder | Repo |
|--------|------|
| `docs` | `mtg-ebay-docs` — Fumadocs, manifest, Vercel API |
| `workflows` | `mtg-ebay-workflows` — CLI, Postgres, local UI |
| `recognition` | `mtg-card-recognition` — CV library |

## Agents

| Invoke | Role |
|--------|------|
| `@supervisor` | Pass/fail checkpoints, assign work, run proofs |
| `@agent-docs-platform` | MDX, manifest, schemas |
| `@agent-python-workflows` | Consumer pipeline |
| `@agent-python-recognition` | Cascade library |
| `@agent-vercel` | Next.js API, Blob, deploy |

## Cursor rules

Project rules live in `.cursor/rules/` (installed via `new_project_docs/scripts/bootstrap-cursor-rules.ps1` from [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) + `mtg-*.mdc` templates). See planning doc `11-cursor-rules-bootstrap.md`.

## Before you code

1. Read criterion `doc_ref` in manifest for your task.
2. Confirm file ownership in `06-cursor-agent-orchestration.md`.
3. Implement minimal diff for that criterion only.

## Before you claim done

1. Run proof command from manifest entry.
2. Notify `@supervisor` with criterion IDs and command output.

## Planning docs source

Bootstrap pack: `Desktop/new_project_docs/` (copy into repos as needed).
