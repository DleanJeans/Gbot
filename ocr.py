from PIL import Image
import pytesseract
import requests
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def read_image(img, lang='vie', config='--psm 6'):
	text = pytesseract.image_to_string(img, lang, config=config)
	return text

def read_history(folder, image):
	image = Image.open('G:/Python/Confetti/history/%s/%s.png' % (folder, image))
	return read_image(image)