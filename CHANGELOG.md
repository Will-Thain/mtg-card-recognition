# Changelog

## 0.2.0 (2026-06-06)

- Standalone repository layout under `packages/mtg-card-recognition/`
- Extract FAISS index build/search into `mtg_card_recognition.embeddings.faiss_index`
- Add `PrintingRecord` catalog type for framework-agnostic indexing
- Labeled crop fixtures and regression tests included in package
- See `REPO_BOOTSTRAP.md` for publishing as a separate Git repository

## 0.1.0

- Initial monorepo extraction: zones, OCR, evidence gate, OpenCLIP embeddings
