from flask import Flask, request, render_template, redirect
from recognizer import recognize_city
from firebase import firebase
import os

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"
firebase = firebase.FirebaseApplication('https://drijvendesteden-default-rtdb.europe-west1.firebasedatabase.app/', None)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            id = create_result(image)
            return id
    return render_template("upload_image.html")


def create_result(image):
    if not os.path.exists("upload"):
        os.makedirs("upload")

    image.save(app.config["IMAGE_UPLOAD"])

    grid = recognize_city(app.config["IMAGE_UPLOAD"])

    result = firebase.post('/data', grid)
    return result['name']