from LSBSteg import LSBSteg
import cv2

from flask import Flask, render_template, request, redirect, session, Response, abort

import json
import numpy


# Initialize the app
app = Flask(__name__, instance_relative_config=True)


# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# Load the views
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/api/encode',methods = ['POST'])
def encode():
	if request.method == 'POST':
		file = request.files['file_gambar']
		text = request.form['text']
		img  = numpy.fromstring(file.read(), numpy.uint8)
		steg = LSBSteg(cv2.imdecode(img, cv2.IMREAD_UNCHANGED))
		img_encoded = steg.encode_text(text)
		cv2.imwrite("my_new_image.png", img_encoded)
		return render_template("index.html", pesan="berhasil menyisipkan")

@app.route('/api/decode',methods = ['POST'])
def decode():
	file = request.files['file_gambar']
	img  = numpy.fromstring(file.read(), numpy.uint8)
	im = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
	steg = LSBSteg(im)
	pesan = unicode(steg.decode_text(), "utf8")
	print(pesan)
	return render_template("index.html",pesan=pesan)

if __name__ == '__main__':
    app.run()
