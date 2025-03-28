# /apps/swagger/swagger.py
from flask import Flask
from flask_restx import Api

app = Flask(__name__)  # Create the Flask app here
api = Api(app, version='1.0', title='Swagger', description='Swagger API', doc='/swagger')

if __name__ == '__main__':
    app.run(debug=True)