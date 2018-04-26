import os
from datetime import datetime

import pytesseract
from PIL import Image
from flask import Flask, render_template, json

app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def ana_sayfa():
    dosya = os.path.join(BASE_DIR, 'static/test.jpg')
    return render_template('result.html', dosya=dosya)


@app.route('/result/<img>', strict_slashes=False)
def ocr(img):
    startTime = datetime.now()
    if not img:
        img = Image.open(os.path.join(BASE_DIR, 'static/test.jpg'))
    ocr_content = pytesseract.image_to_string(img, lang='tur').replace('\n\n', '\n')

    # JSON Response
    json_response = {
        "status": True,
        "content": ocr_content,
        "length": len(ocr_content),
        "runtime": str(datetime.now() - startTime),
        "linelenght": str(len(ocr_content.split('\n'))),
        "wordslenght": str(len(ocr_content.split(' '))),
    }

    # json_response_ordered = json.dumps(OrderedDict(
    #     status=True,
    #     content=ocr_content,
    #     length=len(ocr_content),
    #     runtime=str(datetime.now() - startTime),
    #     linelenght=str(len(ocr_content.split('\n'))),
    #     wordslenght=str(len(ocr_content.split(' '))),
    # ))

    result = json.dumps(json_response)
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
