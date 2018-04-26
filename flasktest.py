import os
from datetime import datetime

import pytesseract
from PIL import Image
from flask import Flask, render_template, json, request

app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def ana_sayfa():
    dosya = os.path.join(BASE_DIR, 'static/test.jpg')
    return render_template('result.html', dosya=dosya)


@app.route('/result', strict_slashes=False)
def ocr():
    startTime = datetime.now()

    img = request.args.get("img", False)
    if not img:
        dosya = Image.open(os.path.join(BASE_DIR, 'static/test.jpg'))
    else:
        import requests
        dosya = requests.get(img)

    ocr_content = pytesseract.image_to_string(Image.open(dosya), lang='tur').replace('\n\n', '\n')

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
