from moto import mock_dynamodb
import boto3
from table_update import update_dynamodb_item
import pytest
import os

@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture()
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.client("dynamodb", region_name="us-east-1")

@pytest.fixture()
def create_table(dynamodb):
    boto3.client("dynamodb").create_table(
        TableName="mock_table",
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'N'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
    )

# Decorate the test function with mock_dynamodb2 to activate the mock DynamoDB service
@mock_dynamodb
@pytest.mark.parametrize("item_id, updated_data, expected_name", [
    (1, {'name': 'Updated Example'}, 'Updated Example'),
    (2, {'name': 'Updated Example 2'}, 'Updated Example 2'),
    (3, {'name': 'Updated Example 3'}, 'Updated Example 3'),
    (4, {'name': 'Updated Example 4'}, 'Updated Example 4'),
    # Add more test cases as needed
])

def test_update_dynamodb_item(item_id, updated_data, expected_name, dynamodb, create_table):
    # Put an item in the mock table
    item = {'id': item_id, 'name': 'Example'}
    dynamodb.put_item(TableName="mock_table", Item=item)

    # Test the update function
    updated_item = update_dynamodb_item("mock_table", item_id, updated_data)

    # Assert that the item has been updated
    assert updated_item['name'] == expected_name