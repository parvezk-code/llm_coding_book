

# pip install pytesseract pdf2image\
# sudo apt install tesseract-ocr poppler-utils

from pdf2image import convert_from_path
import pytesseract

def extract_text_ocr(file_path: str) -> str:
    images = convert_from_path(file_path)
    text = []

    for img in images:
        page_text = pytesseract.image_to_string(img)
        if page_text:
            text.append(page_text)

    return "\n".join(text)


# text = extract_text_ocr("scanned.pdf")