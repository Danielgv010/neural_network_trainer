# /apps/main/main.py
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from apps.swagger.swagger import app, api

if __name__ == '__main__':
    app.run(debug=True)