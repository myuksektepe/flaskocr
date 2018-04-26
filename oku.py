import os

import pytesseract
from PIL import Image
from flask import Flask

app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

dosya = Image.open(os.path.join(BASE_DIR, 'static/test.jpg'))

ocr_content = pytesseract.image_to_string(dosya, lang='tur').replace('\n\n', '\n')

print(ocr_content)
