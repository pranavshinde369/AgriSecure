import pytesseract
from PIL import Image

def extract_text_from_image(image):
    try:
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text
    except Exception:
        return ""
