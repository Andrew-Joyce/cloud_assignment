import boto3
from botocore.exceptions import ClientError
import logging

dynamodb = boto3.client('dynamodb', region_name='ap-southeast-2')

def get_table(table_name='Clients'):
    return boto3.resource('dynamodb', region_name='ap-southeast-2').Table(table_name)

def check_if_email_exists(email, table):
    try:
        response = table.get_item(Key={'email': email})
        return 'Item' in response
    except ClientError as e:
        logging.error("Failed to query DynamoDB", exc_info=True)
        raise e  
def insert_user(user_data, table):
    try:
        response = table.put_item(Item=user_data)
        return True  
    except ClientError as e:
        logging.error("Failed to insert data into DynamoDB", exc_info=True)
        return False  

def check_credentials(email, password, table):
    response = table.get_item(Key={'email': email})

    if 'Item' in response:
        item = response['Item']
        if item['password'] == password:
            return True
    return False

def get_user(email, table):
    try:
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return response['Item']
        else:
            return None  
    except ClientError as e:
        logging.error("Failed to fetch user details from DynamoDB", exc_info=True)
        raise e  

response = dynamodb.list_tables()
print(response)
