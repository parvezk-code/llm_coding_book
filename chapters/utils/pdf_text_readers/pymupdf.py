
# pip install pymupdf

import fitz

def extract_text_pymupdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = []

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text.append(page_text)

    doc.close()
    return "\n".join(text)


# text = extract_text_pymupdf("sample.pdf")

