import boto3
from botocore.exceptions import ClientError
import random

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')  # Sydney region

def create_table():
    try:
        table = dynamodb.create_table(
            TableName='Clients',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        table.wait_until_exists()  # Wait until the table is created
        print("Table created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            raise

def populate_table():
    table = dynamodb.Table('Clients')
    suburbs = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra"]
    states = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT"]
    initial_password = 12345  # Initial password for the first customer
    for i in range(1, 16):
        name = f"Andrew Joyce {i}"
        email = f"andrewjoyce{i}@gmail.com"
        phone = f"+61 4{random.randint(10000000, 99999999)}"
        address = f"{random.randint(1, 100)} Example St"
        suburb = random.choice(suburbs)
        state = random.choice(states)
        postcode = random.randint(2000, 7999)
        password = f"{initial_password + i - 1}"  # Increment password by 1 for each customer
        try:
            table.put_item(
                Item={
                    'email': email,
                    'name': name,
                    'phone': phone,
                    'address': address,
                    'suburb': suburb,
                    'state': state,
                    'postcode': str(postcode),
                    'password': password
                }
            )
            print(f"Inserted customer: {name}")
        except ClientError as e:
            print(e.response['Error']['Message'])

def main():
    create_table()
    populate_table()

if __name__ == '__main__':
    main()
