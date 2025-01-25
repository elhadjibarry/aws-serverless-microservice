import json
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    try:
        dynamodb_client.put_item(
            TableName='ProductPurchase',
            Item={
                'ProductPurchaseId': {'S': '1'},
                'Name': {'S': 'Laptop'},
                'Price': {'N': '1000'}
            }
        )
        
        logger.info('Successfully inserted item into DynamoDB')
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully inserted data!"
            }),
        }
        
    except ClientError as e:
        logger.error(f"Error inserting item into DynamoDB: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Error inserting data",
                "error": str(e)
            }),
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            }),
        }