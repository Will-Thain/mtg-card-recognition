# Bootstrap: separate Git repository (Option C)

This directory is a **complete standalone Python package**. Use these steps to publish it as its own repo and consume it from EbayWorkflows via git/PyPI instead of a monorepo path.

## 1. Create the remote repository

```bash
# On GitHub: create empty repo `mtg-card-recognition` (no README)
cd packages/mtg-card-recognition
git init
git add .
git commit -m "Initial standalone mtg-card-recognition 0.2.0"
git branch -M main
git remote add origin git@github.com:YOUR_ORG/mtg-card-recognition.git
git push -u origin main
```

## 2. Tag releases

```bash
git tag v0.2.0
git push origin v0.2.0
```

Use [semantic versioning](https://semver.org/): breaking gate/API changes → major; new features → minor; fixes → patch.

## 3. Wire EbayWorkflows to the remote package

In **EbayWorkflows** `pyproject.toml`, replace the path dependency:

```toml
# Development (monorepo) — remove after split
"mtg-card-recognition @ file:./packages/mtg-card-recognition",

# Production (separate repo) — pick one:
"mtg-card-recognition @ git+https://github.com/YOUR_ORG/mtg-card-recognition@v0.2.0",
# "mtg-card-recognition>=0.2.0",   # after publishing to PyPI/private index
```

Then reinstall:

```powershell
pip install -e ".[dev]"
```

## 4. CI in this repo

GitHub Actions workflow: `.github/workflows/ci.yml`

- `ruff check src tests`
- `pytest` (no Postgres required for unit tests)

## 5. What stays in EbayWorkflows

| Concern | Repo |
|---------|------|
| Zone OCR, gate, FAISS core | **mtg-card-recognition** |
| Postgres models, Phase 5/6 workers, CLI, GUI | **EbayWorkflows** |
| Scryfall sync, Cardmarket, EV ranking | **EbayWorkflows** |
| `recognition_settings` adapter (`Settings` → `RecognitionSettings`) | **EbayWorkflows** |
| Match event log, proposal DB writes | **EbayWorkflows** |

## 6. Panel v2 work

Implement proposal review, veto layer, and gate hardening **in this repo first**, release a new tag, then bump the dependency in EbayWorkflows.

## 7. Optional: git submodule (alternative to pip git URL)

```bash
# In EbayWorkflows root
git submodule add git@github.com:YOUR_ORG/mtg-card-recognition.git vendor/mtg-card-recognition
pip install -e vendor/mtg-card-recognition
```

Submodules add friction; **pip git URL is preferred** for Option C.

## 8. Remove monorepo copy (after remote is live)

Once EbayWorkflows uses the git/PyPI dependency:

```powershell
Remove-Item -Recurse -Force packages/mtg-card-recognition
# Keep packages/README.md pointing to the external repo URL
```

Or retain `packages/` as a **git submodule** checkout of the external repo for local dev.
