from flask import Flask, request, render_template, redirect, jsonify, flash, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from recognizer.recognizer import recognize_city
import os
import qrcode
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# 1) enable sessions/flashing
app.secret_key = os.getenv('SECRET_KEY', 'change-this-to-a-random-value')

app.config["IMAGE_UPLOAD"] = "upload/img.png"

# SQLite database configuration
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'city_data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grid_data = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Create database and tables
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files.get("image")
        city_name = request.form.get("city_name")

        if not image:
            flash('No image uploaded!', 'error')
            return render_template("upload_image.html")

        if not city_name:
            flash('City name is required!', 'error')
            return render_template("upload_image.html")

        # Check for duplicate city name
        existing_city = City.query.filter_by(name=city_name).first()
        if existing_city:
            flash('City name already exists. Please choose a different name.', 'error')
            return render_template("upload_image.html")

        # Save & get new ID
        id = create_result(image, city_name)

        # 2) PRG: redirect to a GET route instead of rendering directly
        return redirect(url_for('show_link', city_id=id))

    return render_template("upload_image.html")

# 3) new GET‐only endpoint to display the link/QR
@app.route("/link/<int:city_id>")
def show_link(city_id):
    return create_link(city_id)

def create_result(image, city_name):
    if not os.path.exists("upload"):
        os.makedirs("upload")

    image.save(os.path.join("upload", "img.png"))  # Save with a fixed name

    grid = recognize_city("upload/img.png")

    # Save the grid data to the SQLite database
    id = save_to_database(grid, city_name)

    return id

def save_to_database(grid, city_name):
    # Create new city record
    new_city = City(name=city_name, grid_data=str(grid))
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

    return render_template('show_link.html', link=link)

# Basic-Auth credentials via env-vars
API_USER = os.getenv('API_USER', 'admin')
API_PASS = os.getenv('API_PASS', 'secret')

def check_auth(username, password):
    return username == API_USER and password == API_PASS

def authenticate():
    return Response(
        '\n Authentication required!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'
    })

def requires_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return wrapped

# API endpoints for the viewer app
@app.route('/api/ids')
@requires_auth
def api_ids():
    cities = City.query.order_by(City.id).all()
    data = [
        {
            'id': city.id,
            'name': city.name,
            'upload_date': city.upload_date.isoformat()
        }
        for city in cities
    ]
    return jsonify(data)

@app.route('/api/city/<int:city_id>')
@requires_auth
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
        'name': city.name,
        'grid_data': grid_data,
        'upload_date': city.upload_date.isoformat()
    })

# CORS headers for cross-origin requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    # bind to 0.0.0.0 so other machines can curl in
    app.run(host='0.0.0.0', port=5050, debug=True)

    # From another machine just run:
    # curl -u youruser:yourpass http://SERVER_IP:5000/api/ids