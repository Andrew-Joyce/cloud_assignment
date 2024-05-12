from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import boto3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'andrew_joyce'  # Ensure this is a secure key in production

    if not app.debug:
        file_handler = RotatingFileHandler('errorlog.txt', maxBytes=1024 * 1024 * 100, backupCount=20)
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

    try:
        table = dynamodb.Table('Clients')
        table.load()  
        logging.info("DynamoDB table accessed successfully.")
    except boto3.exceptions.ResourceNotFoundException:
        logging.error("DynamoDB table not found.")

    from Program.routes import configure_routes
    configure_routes(app, table)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=True)
