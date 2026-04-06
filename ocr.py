from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    
    text = ""
    for img in images:
        page_text = pytesseract.image_to_string(img)
        text += page_text + "\n"
    
    return text