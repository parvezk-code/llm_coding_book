
# pip install pdfplumber

import pdfplumber

def extract_text_pdfplumber(file_path: str) -> str:
    text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text)


# text = extract_text_pdfplumber("sample.pdf")