# Agent instructions (greenfield program)

This program is built by **concurrent Cursor agents** under a **Supervisor**. Human operators intervene on escalation only.

## Single entry point

**Address only `@supervisor`** in the Agents Window. The Supervisor routes work to stack agents via `/multitask` or Task subagents, then runs proofs.

Do **not** task `@agent-docs-platform`, `@agent-python-workflows`, `@agent-python-recognition`, or `@agent-vercel` directly.

Delegation blocks: **`MULTITASK.md`** in this folder.

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
| `@supervisor` | **Only operator entry point** — plan, delegate, prove, PASS/FAIL |
| `@agent-docs-platform` | MDX, manifest, schemas (supervisor-assigned) |
| `@agent-python-workflows` | Consumer pipeline (supervisor-assigned) |
| `@agent-python-recognition` | Cascade library (supervisor-assigned) |
| `@agent-vercel` | Next.js API, Blob, deploy (supervisor-assigned) |

## Cursor rules

Project rules live in `.cursor/rules/` including **`mtg-supervisor-hub.mdc`** (always on). See planning doc `11-cursor-rules-bootstrap.md`.

## Stack agents: before you claim done

1. Run proof command from manifest entry for your criterion IDs.
2. Report back to **`@supervisor`** with criterion IDs and command output — not to the human directly.

## Planning docs source

Bootstrap pack: `Desktop/new_project_docs/` (copy into repos as needed).
