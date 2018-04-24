import requests, PIL, pytesseract, sys
from flask import Flask, request, url_for, render_template, jsonify
from imgurpython import ImgurClient
from random import randint
from io import BytesIO

app = Flask(__name__)

@app.route('/meme_url')
def get_meme():
    client_id = 'c1c976ad7ab60e9'
    client_secret = '96fff59e1a078eb1d8080d838dba6f0892b17f3c'
    client = ImgurClient(client_id, client_secret)
    while True:
        page = randint(0, 1000)
        try:
            gallery = client.gallery_tag('memes', page = page, sort = 'time', window = 'all')
            break
        except:
            pass
    items = gallery.items
    while True:
        try:
            item_ind = randint(0, len(items))
            item = items[item_ind]
            break
        except IndexError:
            pass
    if hasattr(item, "images"):
        images = item.images
        while True:
            try:
                image_ind = randint(0, len(images))
                image = images[image_ind]
                break
            except IndexError:
                pass
        if not image["animated"]:
            return image["link"]
    else:
        if not item.animated:
            return item.link

def decode_meme(url):
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    response = requests.get(url)
    pil_img = PIL.Image.open(BytesIO(response.content))
    meme_text = pytesseract.image_to_string(pil_img)
    meme_rows = str(meme_text.count("\n") + 1)
    return meme_rows, meme_text

@app.route('/meme_text', methods = ["GET"])
def read_meme():
    url = request.args.get("url")
    #with open("/app/log", "a") as logstream:
    #    logstream.write(url + "\n")
    #    logstream.flush()
    meme_rows, meme_text = decode_meme(url)
    return jsonify({"meme_rows": meme_rows, "meme_text": meme_text})

@app.route('/')
def index():
    first_meme_url = get_meme()
    first_meme_rows, first_meme_text = decode_meme(first_meme_url)
    return render_template('index.html', first_meme_url = first_meme_url, first_meme_rows = first_meme_rows, first_meme_text = first_meme_text)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')