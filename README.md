# mtg-card-recognition (greenfield)

CV library cascade Tiers 0–8. MVP-4 delivers a minimal installable package with a deterministic cascade stub and a sample FAISS index build script.

## Install

```powershell
cd c:\dev\mtg-card-recognition
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Proof commands (CHK-M4-01, CHK-M4-05)

```powershell
pytest -q
python scripts/build_faiss_index.py
```

Expected:

- `pytest -q` exits `0` with all cascade tests passing.
- `python scripts/build_faiss_index.py` exits `0` and writes `.cache/faiss/index.bin` plus `.cache/faiss/index.bin.meta.json` from `tests/fixtures/faiss/cards.json`.

## API (MVP-4 stub)

```python
from mtg_card_recognition import run_cascade

proposals = run_cascade("path/to/image.png", candidates=[{"printing_id": "...", "name": "..."}])
# Each proposal includes gate_status and gate_fail_reason (deterministic stub).
```

Planning: `new_project_docs/05-greenfield-repository-plan.md`
