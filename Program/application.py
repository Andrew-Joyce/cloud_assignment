from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import boto3

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    # Configure Flask application
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'andrew_joyce'  # Ensure this is a secure key in production

    # Configure logging
    if not app.debug:
        file_handler = RotatingFileHandler('errorlog.txt', maxBytes=1024 * 1024 * 100, backupCount=20)
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

    # Check DynamoDB table existence
    try:
        table = dynamodb.Table('Clients')
        table.load()  # Attempt to load the table to ensure it exists
        logging.info("DynamoDB table accessed successfully.")
    except boto3.exceptions.ResourceNotFoundException:
        logging.error("DynamoDB table not found.")

    # Import routes
    from Program.routes import configure_routes
    configure_routes(app, table)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=True)
