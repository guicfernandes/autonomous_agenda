"""Main module to run the application."""

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# from app.main import app
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
