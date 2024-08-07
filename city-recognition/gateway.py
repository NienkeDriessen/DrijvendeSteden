from flask import Flask, request, render_template, redirect
from recognizer import recognize_city
import os

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            store_image(image)
            grid = recognize_city(app.config["IMAGE_UPLOAD"])
            return grid
    return render_template("upload_image.html")

def store_image(image):
    if not os.path.exists("upload"):
        os.makedirs("upload")

    image.save(app.config["IMAGE_UPLOAD"])