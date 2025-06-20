from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from recognizer.recognizer import recognize_city
import os
import qrcode
import json

app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "upload/img.png"

# SQLite database configuration
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'city_data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid_data = db.Column(db.Text, nullable=False)

# Create database and tables
with app.app_context():
    db.create_all()

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

    # Save the grid data to the SQLite database
    id = save_to_database(grid)

    return id

def save_to_database(grid):
    # Create new city record
    new_city = City(grid_data=str(grid))
    db.session.add(new_city)
    db.session.commit()
    
    return new_city.id

def create_link(id):
    # Update link to point to local viewer
    link = f"http://127.0.0.1:8000/#?id={id}"  # Assuming viewer runs on port 8000

    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = "city-recognition/static/qr_code.png"
    if not os.path.exists("city-recognition/static"):
        os.makedirs("city-recognition/static")

    img.save(qr_path)

    return render_template('show_link.html', link=link, qr_path=qr_path)

# API endpoints for the viewer app
@app.route('/api/ids')
def api_ids():
    cities = City.query.order_by(City.id).all()
    ids = [str(city.id) for city in cities]
    return jsonify(ids)

@app.route('/api/city/<int:city_id>')
def api_city(city_id):
    city = City.query.get_or_404(city_id)
    # Parse the grid data string into a JSON object
    try:
        grid_data = json.loads(city.grid_data.replace("'", '"'))
    except json.JSONDecodeError:
        # Fallback if the data isn't properly formatted
        grid_data = {}
    
    return jsonify({
        'id': str(city.id),
        'grid_data': grid_data
    })

# CORS headers for cross-origin requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)