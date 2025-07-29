from flask import Flask, request, render_template, redirect, jsonify, flash, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from recognizer.recognizer import recognize_city
import qrcode
import os
import json
from datetime import datetime
from functools import wraps
import ast
import threading
import time

# Main DB (long-term)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-to-a-random-value')
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'city_data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Viewer DB (latest 20)
VIEWER_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'city_viewer.db'))
viewer_engine = create_engine(f'sqlite:///{VIEWER_DB_PATH}')

# Create viewer table if not exists
with viewer_engine.connect() as conn:
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS ViewerCity (
            slot_id INTEGER PRIMARY KEY,
            main_id INTEGER,
            name TEXT,
            grid_data TEXT,
            upload_date DATETIME
        )
    '''))

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grid_data = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def save_to_database(grid, city_name):
    # save a JSON string, not repr(grid)
    payload = json.dumps(grid)
    print(payload)
    new_city = City(name=city_name, grid_data=payload)
    db.session.add(new_city)
    db.session.commit()
    # After saving to main DB, also update viewer DB
    update_viewer_db(new_city)
    return new_city.id

def update_viewer_db(city):
    slot_id = ((city.id - 1) % 20) + 1
    # debug log
    print(f"[ViewerDB] syncing main_id={city.id} → slot_id={slot_id}")

    # use a transactional begin() so we commit automatically
    with viewer_engine.begin() as conn:
        conn.execute(
            text('''
                INSERT INTO ViewerCity (slot_id, main_id, name, grid_data, upload_date)
                VALUES (:slot_id, :main_id, :name, :grid_data, :upload_date)
                ON CONFLICT(slot_id) DO UPDATE SET
                    main_id=:main_id,
                    name=:name,
                    grid_data=:grid_data,
                    upload_date=:upload_date
            '''), {
                'slot_id': slot_id,
                'main_id': city.id,
                'name': city.name,
                'grid_data': city.grid_data,
                'upload_date': city.upload_date.isoformat()
            }
        )

def sync_main_db_to_viewer_db():
    """
    On startup, ensure the viewer DB has the latest 20 cities from the main DB.
    """
    with app.app_context():
        latest = City.query.order_by(City.id.desc()).limit(20).all()[::-1]
        print(">>> syncing main IDs:", [c.id for c in latest])
        for c in latest:
            update_viewer_db(c)

def periodic_sync():
    while True:
        print("Running periodic sync...")
        sync_main_db_to_viewer_db()
        time.sleep(5 * 60)  # Perform database sync every 5 min

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

def create_link(id):
    # Update link to point to local viewer with a simple hash
    # Use the slot_id for the link, not the main_id
    slot_id = ((id - 1) % 20) + 1
    link = f"http://127.0.0.1:8000/#{slot_id}"  # e.g., http://127.0.0.1:8000/#1

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
    # only send id, name and upload_date
    return jsonify([
        {
            'id': c.id,
            'name': c.name,
            'upload_date': c.upload_date.isoformat(),
            'grid_data': json.loads(c.grid_data)
        }
        for c in cities
    ])

@app.route('/api/city/<int:city_id>')
@requires_auth
def api_city(city_id):
    city = City.query.get_or_404(city_id)
    # parse the grid_data string into a real JSON object
    try:
        grid = json.loads(city.grid_data)
    except json.JSONDecodeError:
        # If JSON decoding fails, attempt to parse as a Python literal
        try:
            grid = ast.literal_eval(city.grid_data)
        except (SyntaxError, ValueError):
            # If literal evaluation fails as well, return an empty dictionary
            grid = {}
    return jsonify({
        'id': city.id,
        'name': city.name,
        'upload_date': city.upload_date.isoformat(),
        'grid_data': json.loads(grid)
    })

@app.route('/api/viewer/ids')
@requires_auth
def api_viewer_ids():
    with viewer_engine.connect() as conn:
        rows = conn.execute(text('SELECT slot_id, main_id, name, upload_date, grid_data FROM ViewerCity ORDER BY slot_id')).fetchall()
    return jsonify([
        {
            'slot_id': r.slot_id,
            'main_id': r.main_id,
            'name': r.name,
            # upload_date is already stored as an ISO‐format string in the viewer DB,
            # so just return it directly instead of calling .isoformat()
            'upload_date': r.upload_date,
            'grid_data': json.loads(r.grid_data)
        }
        for r in rows
        if r.slot_id is not None
    ])

@app.route('/api/viewer/city/<int:slot_id>')
@requires_auth
def api_viewer_city(slot_id):
    with viewer_engine.connect() as conn:
        row = conn.execute(
            text('SELECT slot_id, main_id, name, grid_data, upload_date FROM ViewerCity WHERE slot_id = :s'),
            {'s': slot_id}
        ).first()
    if not row:
        return jsonify({}), 404

    return jsonify({
        'slot_id': row.slot_id,
        'main_id': row.main_id,
        'name': row.name,
        # same here: row.upload_date is already a string
        'upload_date': row.upload_date,
        'grid_data': json.loads(row.grid_data)
    })

@app.route('/api/viewer/debug')
@requires_auth
def api_viewer_debug():
    """
    Dump all rows in ViewerCity so you can verify the sync is happening.
    """
    with viewer_engine.connect() as conn:
        rows = conn.execute(
            text('SELECT slot_id, main_id, name, upload_date, grid_data FROM ViewerCity ORDER BY slot_id')
        ).fetchall()

    data = []
    for r in rows:
        try:
            gd = json.loads(r.grid_data)
        except:
            gd = r.grid_data
        data.append({
            'slot_id': r.slot_id,
            'main_id': r.main_id,
            'name': r.name,
            'upload_date': r.upload_date,
            'grid_data': json.loads(gd)
        })

    return jsonify(data)

# CORS headers for cross-origin requests
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    # Initial sync
    with app.app_context():
        sync_main_db_to_viewer_db()

    # Start the periodic sync in a background thread
    threading.Thread(target=periodic_sync, daemon=True).start()

    # Run on HTTP, no SSL context
    app.run(host='0.0.0.0', port=5050, debug=True)

    # From another machine just run:
    # curl -u youruser:yourpass http://SERVER_IP:5050/api/ids

    # From another machine just run:
    # curl -u youruser:yourpass http://SERVER_IP:5000/api/ids