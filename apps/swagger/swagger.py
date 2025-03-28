# /apps/swagger/swagger.py
from flask import Flask
from flask_restx import Api

a = 2
app = Flask(__name__)  # Create the Flask app here
api = Api(app, version='1.0', title='Swagger', description='Swagger API', doc='/swagger')

def initialize_swagger():
    return app

if __name__ == '__main__':
    initialize_swagger()