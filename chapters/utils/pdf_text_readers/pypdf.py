# pip install pypdf
# pypdf is successor and continuation of PyPDF2

from pypdf import PdfReader

def extract_text_pypdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


# text = extract_text_pypdf("sample.pdf")