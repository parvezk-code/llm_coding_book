from __future__ import annotations

from io import BytesIO
from dataclasses import dataclass
from pathlib import Path
from typing import List, TypeAlias, TypedDict, Union


PathLike: TypeAlias = Union[str, Path]


class PDFExtractionError(Exception):
    """Raised when PDF text extraction cannot be completed."""


@dataclass
class PDFPageText:
    page_number: int
    text: str


class PDFExtractionResult(TypedDict):
    path: str
    text: str
    error: str | None


def _extract_page_texts(reader, *, strip: bool, skip_empty: bool) -> List[PDFPageText]:
    pages: List[PDFPageText] = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            raise PDFExtractionError(
                f"Failed to extract text from page {page_number}."
            ) from exc
        if strip:
            text = text.strip()
        if skip_empty and not text:
            continue
        pages.append(PDFPageText(page_number=page_number, text=text))

    return pages


def _get_pdf_reader(pdf_path: PathLike):
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path}")

    PdfReader = _get_pdf_reader_class()

    try:
        return PdfReader(str(path))
    except Exception as exc:
        raise PDFExtractionError(f"Failed to read PDF: {path}") from exc


def _get_pdf_reader_class():
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ImportError as second_exc:
            raise PDFExtractionError(
                "No supported PDF library found. Install 'pypdf' (recommended) "
                "or 'PyPDF2' to enable extraction."
            ) from second_exc
    return PdfReader


def extract_text_by_page(
    pdf_path: PathLike,
    *,
    strip: bool = True,
    skip_empty: bool = False,
) -> List[PDFPageText]:
    """
    Extract text from each page of a PDF.

    Returns a list of PDFPageText objects with 1-based page numbers.
    """
    reader = _get_pdf_reader(pdf_path)
    return _extract_page_texts(reader, strip=strip, skip_empty=skip_empty)


def extract_text(
    pdf_path: PathLike,
    *,
    page_separator: str = "\n\n",
    strip: bool = True,
    skip_empty: bool = False,
) -> str:
    """
    Extract combined text from all pages in a PDF.
    """
    page_items = extract_text_by_page(pdf_path, strip=strip, skip_empty=skip_empty)
    return page_separator.join(item.text for item in page_items)


def extract_text_from_many_pdfs(
    pdf_paths: List[PathLike],
    *,
    page_separator: str = "\n\n",
    strip: bool = True,
    skip_empty: bool = False,
    continue_on_error: bool = False,
) -> List[PDFExtractionResult]:
    """
    Extract text from multiple PDFs.

    Returns items in the form:
    {
        "path": "<pdf path>",
        "text": "<combined extracted text>",
        "error": "<error message or None>"
    }
    """
    results: List[PDFExtractionResult] = []

    for pdf_path in pdf_paths:
        path_str = str(pdf_path)
        try:
            text = extract_text(
                pdf_path,
                page_separator=page_separator,
                strip=strip,
                skip_empty=skip_empty,
            )
            results.append({"path": path_str, "text": text, "error": None})
        except Exception as exc:
            if not continue_on_error:
                raise
            results.append({"path": path_str, "text": "", "error": str(exc)})

    return results


def extract_text_from_pdf_bytes(
    pdf_bytes: bytes,
    *,
    page_separator: str = "\n\n",
    strip: bool = True,
    skip_empty: bool = False,
) -> str:
    """
    Extract combined text from raw PDF bytes.
    """
    PdfReader = _get_pdf_reader_class()

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as exc:
        raise PDFExtractionError("Failed to read PDF from bytes.") from exc

    page_items = _extract_page_texts(reader, strip=strip, skip_empty=skip_empty)
    return page_separator.join(item.text for item in page_items)
