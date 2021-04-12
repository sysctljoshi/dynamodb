import boto3

def delete_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('rdsdetails')
    table.delete()
delete_table()

def create_table(dynamodb=None):
    if not dynamodb:
      dynamodb = boto3.resource('dynamodb")

    table = dynamodb.create_table(
        TableName='rdsdetails',
        KeySchema=[
            {
                'AttributeName': 'dbendpoint',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'instancetype',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'dbendpoint',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'instancetype',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

available_regions = boto3.Session().get_available_regions('rds')
for region in available_regions:
    rds = boto3.client('rds', region_name=region)
    paginator = rds.get_paginator('describe_db_instances').paginate()
    for page in paginator:
        for dbinstance in page['DBInstances']:
            dynamodb = boto3.resource('dynamodb')
            dynamodb.put_item(TableName='rdsdetails', Item={'dbendpoint':{'S':'DBInstanceIdentifier'},'instancetype':{'S':'DBInstanceClass'}})