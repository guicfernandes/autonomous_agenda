"""Main module to run the application."""

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# from app.main import app
from app import create_app

app = create_app()

# print("FLASK_ENV:", os.getenv("FLASK_ENV"))
# print("FLASK_DEBUG:", os.getenv("FLASK_DEBUG"))
# print("FLASK_APP:", os.getenv("FLASK_APP"))
# print("Debug mode:", app.debug)

if __name__ == "__main__":
    app.run(debug=True)
