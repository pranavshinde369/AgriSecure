import pytesseract
from PIL import Image

# Explicit path to Tesseract executable (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image):
    """
    Extract text from screenshot image using OCR
    """
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text
