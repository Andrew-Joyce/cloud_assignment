import boto3
from botocore.exceptions import ClientError
import logging

# Initialize DynamoDB client with the specified region
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-2')

# Get the DynamoDB table
def get_table(table_name='Clients'):
    # Returns a DynamoDB Table resource object for the specified table
    return boto3.resource('dynamodb', region_name='ap-southeast-2').Table(table_name)

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

def check_credentials(email, password, table):
    # Use the provided table object to retrieve the item
    response = table.get_item(Key={'email': email})

    # Check if the item exists and if the password matches
    if 'Item' in response:
        item = response['Item']
        if item['password'] == password:
            return True
    return False

# Get user details
def get_user(email, table):
    # This function retrieves user details by email from the specified DynamoDB table
    try:
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return response['Item']
        else:
            return None  # No user found
    except ClientError as e:
        logging.error("Failed to fetch user details from DynamoDB", exc_info=True)
        raise e  # Re-raise exception after logging it

# Example usage to list tables
response = dynamodb.list_tables()
print(response)
