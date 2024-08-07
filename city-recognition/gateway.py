from flask import Flask, request, render_template, redirect
from recognizer import recognize_city
from firebase import firebase
import uuid
import os

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"
firebase = firebase.FirebaseApplication('https://drijvendesteden-default-rtdb.europe-west1.firebasedatabase.app/', None)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            store_image(image)
            grid = recognize_city(app.config["IMAGE_UPLOAD"])
            id = store_result(grid)
            return id
    return render_template("upload_image.html")

def store_image(image):
    if not os.path.exists("upload"):
        os.makedirs("upload")

    image.save(app.config["IMAGE_UPLOAD"])

def store_result(grid):
    id = generate_id()
    new_city = {str(id) : grid}
    result = firebase.post('/data', new_city)
    print(result)
    return id

def generate_id():
    id = str(uuid.uuid4())
    result = firebase.get(f'/data/{id}', None)
    if result == None:
        return id
    else:
        return generate_id()