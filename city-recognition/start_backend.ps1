# start_backend.ps1

# Navigate to the backend directory
Set-Location "C:\Users\sup-ndriessen\Documents\floating_cities\DrijvendeSteden\city-recognition"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Set Flask app and start the server on port 5050
$env:FLASK_APP = "gateway.py"
$env:FLASK_ENV = "development"

flask run --host=0.0.0.0 --port=5050
