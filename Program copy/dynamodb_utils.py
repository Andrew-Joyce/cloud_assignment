import boto3
from botocore.exceptions import ClientError
import logging

# Initialize DynamoDB resource
def get_dynamodb_resource(region_name='ap-southeast-2'):
    return boto3.resource('dynamodb', region_name=region_name)

# Get the DynamoDB table
def get_table(table_name='Clients', dynamodb=None):
    if dynamodb is None:
        dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)

# Check if an email is already registered
def check_if_email_exists(email, table):
    try:
        response = table.get_item(Key={'email': email})
        return 'Item' in response
    except ClientError as e:
        logging.error("Failed to query DynamoDB", exc_info=True)
        raise e  # Re-raise exception after logging it

# Register a new user
def insert_user(user_data, table):
    try:
        response = table.put_item(Item=user_data)
        return True  # Return True if insertion is successful
    except ClientError as e:
        logging.error("Failed to insert data into DynamoDB", exc_info=True)
        return False  # Return False if insertion fails

# Check user credentials
def check_credentials(email, password, table):
    try:
        response = table.get_item(Key={'email': email})
        if 'Item' in response and response['Item']['password'] == password:
            return True
        return False
    except ClientError as e:
        logging.error("Failed to fetch user data", exc_info=True)
        raise e  # Re-raise exception after logging it

# Get user details
def get_user(email, table):
    try:
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return response['Item']
        else:
            return None  # No user found
    except ClientError as e:
        logging.error("Failed to fetch user details from DynamoDB", exc_info=True)
        raise e  # Re-raise exception after logging it
