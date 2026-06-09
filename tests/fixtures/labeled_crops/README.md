# Labeled crop fixtures

Golden crop images for regression-testing card recognition (Phase 5/6 strict gate) and **data-grounded architecture review**.

## Layout

| File | Purpose |
|------|---------|
| `manifest.json` | Schema-valid entries for CI (`verify_expect`: `pass` \| `fail`) |
| `manifest.schema.json` | JSON Schema for manifest rows |
| `cases.json` | Rich metadata: signals, FAISS top-5, production evidence, asset paths |
| `examples/{case_id}/` | Copied JPGs: `region.jpg`, optional `listing.jpg`, zone crops |
| `manifest.example.json` | Minimal schema example |

## Curated set (48 cases)

Generated from production Postgres + `.cache/images/`:

```powershell
.\.venv\Scripts\python.exe scripts\curate_labeled_crops.py
```

| Category | Count | Notes |
|----------|-------|-------|
| `verified_production` | 3 | DB `image_verified=true`; visual audit → **all fail** gate (false symbol match) |
| `high_proposal_listing` | 12 | 30–66 candidates; tests proposal caps |
| `title_match_single` | 8 | Title-only path |
| `has-bottom-zone` / `has-symbol-zone` / `bulk-multi-region` / `rich-zones` | 25 | Filesystem samples |

See `docs/adr/0003-eval-brief.md` and `docs/adr/0003-expert-review-v3.md`.

## Manifest row fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Stable fixture id |
| `path` | yes | Relative path under this directory |
| `expected_set` | no | Expected Scryfall set code (visual or title ground truth) |
| `expected_collector` | no | Expected collector number |
| `expected_name` | no | Expected card name substring |
| `verify_expect` | yes | `pass` or `fail` — whether strict gate **should** verify |
| `notes` | no | Operator / visual audit context |

**Note:** `verify_expect` reflects **ground truth from visual audit**, not necessarily current DB `image_verified` flags.

## Example cases

| Id | Lesson |
|----|--------|
| `verified-01-prm` | Goblin Tinkerer mis-verified as Flooded Strand (symbol false positive) |
| `fs-has-bottom-zone-001` | Magnigoth Treefolk (INV 201) — good set+collector target |
| `title-single-01` | Card stack edges detected as region — should skip |
| `proposal-heavy-001` | Yu-Gi-Oh! photo in MTG lot search |
