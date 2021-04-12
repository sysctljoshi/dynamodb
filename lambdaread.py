import json
import boto3
client = boto3.client('apigateway')

def lambda_handler(event, context):
  dynamodb = boto3.resource('dynamodb')
  dbdetails = dynamodb.Table('rdsdetails')
  response = dbdetails.query(
  KeyConditionExpression=Key('dbendpoint').eq('')
)
print(response)