# llm_coding

## PDF text extraction utilities

This repository now includes `pdf_text_extractor.py` with reusable functions for
RAG preprocessing workflows:

- `extract_text_by_page(pdf_path)` for page-level extraction
- `extract_text(pdf_path)` for full-document extraction
- `extract_text_from_many_pdfs(pdf_paths)` for batch extraction
- `extract_text_from_pdf_bytes(pdf_bytes)` for in-memory extraction

Install a PDF parser first (recommended):

```bash
pip install pypdf
```
