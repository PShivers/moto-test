import boto3

def update_dynamodb_item(table_name, item_id, updated_data):
    """
    Update an item in a DynamoDB table.

    Parameters:
    - table_name (str): Name of the DynamoDB table.
    - item_id (int): ID of the item to be updated.
    - updated_data (dict): Dictionary containing updated attributes.

    Returns:
    - dict: Updated item.
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)

    # Update the item
    response = table.update_item(
        Key={'id': item_id},
        UpdateExpression='SET #name = :name',
        ExpressionAttributeNames={'#name': 'name'},
        ExpressionAttributeValues={':name': updated_data['name']},
        ReturnValues='ALL_NEW'  # Return the updated item
    )

    return response.get('Attributes', {})


# import boto3
# from moto import mock_dynamodb
# import pytest

# # Decorate the test function with mock_dynamodb2 to activate the mock DynamoDB service
# @mock_dynamodb
# def test_update_item():
#     # Create a mock DynamoDB table
#     table_name = 'test_table'
#     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
#     table = dynamodb.create_table(
#         TableName=table_name,
#         KeySchema=[
#             {'AttributeName': 'id', 'KeyType': 'HASH'},
#         ],
#         AttributeDefinitions=[
#             {'AttributeName': 'id', 'AttributeType': 'N'},
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5,
#         },
#     )

#     # Put an item in the table
#     item = {'id': 1, 'name': 'example'}
#     table.put_item(Item=item)

#     # Update the item
#     updated_data = {'name': 'updated_example'}
#     client = boto3.client('dynamodb', region_name='us-east-1')
#     client.update_item(
#         TableName=table_name,
#         Key={'id': {'N': '1'}},
#         UpdateExpression='SET #name = :name',
#         ExpressionAttributeNames={'#name': 'name'},
#         ExpressionAttributeValues={':name': {'S': updated_data['name']}},
#     )

#     # Retrieve the updated item from the table
#     response = table.get_item(Key={'id': 1})
#     updated_item = response['Item']
#     print(updated_item)
#     # Assert that the item has been updated
#     assert updated_item['name'] == updated_data['name']

# # Run the test
# if __name__ == '__main__':
#     pytest.main([__file__])