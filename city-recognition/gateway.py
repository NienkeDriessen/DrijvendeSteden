from flask import Flask, request, render_template, redirect
from recognizer.recognizer import recognize_city
import os
import qrcode
import csv

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"
DATABASE_FILE = 'city_data.csv'

# Initialize the database file with headers if it doesn't exist
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['id', 'grid_data'])  # Add headers

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

    # Save the grid data to the local CSV file
    id = save_to_csv(grid)

    return id

def save_to_csv(grid):
    # Generate a unique ID (you can use a counter or UUID)
    id = generate_unique_id()

    with open(DATABASE_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([id, str(grid)])  # Save the grid data as a string

    return id

def generate_unique_id():
    # Simple counter-based ID generation (for demonstration purposes)
    # In a real application, consider using UUIDs or a more robust method
    if not os.path.exists('id_counter.txt'):
        with open('id_counter.txt', 'w') as f:
            f.write('0')

    with open('id_counter.txt', 'r') as f:
        count = int(f.read())

    count += 1

    with open('id_counter.txt', 'w') as f:
        f.write(str(count))

    return count

def create_link(id):
    link = f"https://singular-granita-604f65.netlify.app//?id={id}"

    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = "static/qr_code.png"
    if not os.path.exists("static"):
        os.makedirs("static")

    img.save(qr_path)

    return render_template('show_link.html', link=link, qr_path=qr_path)


if __name__ == '__main__':
    app.run(debug=False)