from flask import Flask, request, render_template, redirect
from recognizer.recognizer import recognize_city
from firebase import firebase
import os
import qrcode
from io import BytesIO

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"
firebase = firebase.FirebaseApplication('https://drijvendesteden-default-rtdb.europe-west1.firebasedatabase.app/', None)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            id = create_result(image)
            return create_link(id)
    return render_template("upload_image.html")


def create_result(image):
    if not os.path.exists("upload"):
        os.makedirs("upload")

    image.save(app.config["IMAGE_UPLOAD"])

    grid = recognize_city(app.config["IMAGE_UPLOAD"])

    result = firebase.post('/data', grid)
    return result['name']

def create_link(id):
    link = f"https://66b39d39708f9b1e02b6d9eb--singular-granita-604f65.netlify.app/?id={id}"

    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = "static/qr_code.png"
    if not os.path.exists("static"):
        os.makedirs("static")

    img.save(qr_path)

    return render_template('show_link.html', link=link, qr_path=qr_path)
    