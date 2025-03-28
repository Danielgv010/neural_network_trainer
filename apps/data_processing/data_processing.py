# /apps/data_processing/data_processing.py

from flask import request
from flask_restx import Namespace, Resource, fields
import csv
import io
import pandas as pd
import os

# Create a Namespace
api = Namespace('data', description='Data Processing operations')

error_model = api.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

##############################################################
########################  Upload CSV  ########################
##############################################################

# Define the expected input (request) data
upload_parser = api.parser()
upload_parser.add_argument('project_name', type=str, required=True, help='The name of the project', location='form')
upload_parser.add_argument('file', type='file', required=True, help='The CSV file to upload', location='files')

# Define the response model
upload_response_model = api.model('UploadResponse', {
    'status': fields.String(description='Status of the upload'),
    'message': fields.String(description='Message indicating the result'),
    'file_path': fields.String(description='Path to the saved file')
})

@api.route('/upload_csv')
@api.expect(upload_parser)
@api.response(200, 'Success', upload_response_model)
@api.response(400, 'Bad Request', error_model)
@api.response(500, 'Internal Server Error', error_model)
class UploadCSV(Resource):
    def post(self):
        '''
        Uploads a CSV file for processing.
        '''
        try:
            # Get the project name from the request
            project_name = request.form.get('project_name')

            if not project_name:
                return {'error': 'Project name is required'}, 400

            # Check if a file was uploaded
            if 'file' not in request.files:
                return {'error': 'No file part'}, 400

            file = request.files['file']

            # Check if the file is empty
            if file.filename == '':
                return {'error': 'No selected file'}, 400

            # Ensure the file is a CSV file
            if not file.filename.endswith('.csv'):
                return {'error': 'Invalid file type. Only CSV files are allowed.'}, 400

            # Create the directory if it doesn't exist
            upload_dir = os.path.join('data', 'raw', project_name)
            os.makedirs(upload_dir, exist_ok=True)

            # Read and Save the CSV data
            try:
                df = pd.read_csv(file)
                file_path = os.path.join(upload_dir, file.filename)
                df.to_csv(file_path, index=False)

            except Exception as e:
                return {'error': f'Error saving CSV: {str(e)}'}, 500

            # Prepare the Response
            response_data = {
                'status': 'success',
                'message': 'CSV file processed and saved successfully',
                'file_path': file_path
            }

            return response_data, 200

        except Exception as e:
            return {'error': f'An unexpected error occurred: {str(e)}'}, 500