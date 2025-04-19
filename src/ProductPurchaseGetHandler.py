import boto3
import os
import logging
import json  # Import JSON for serialization

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

database = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = database.Table(table_name)

def lambda_handler(event, context):
    try:
        # Retrieve all items from the DynamoDB table
        response = table.scan()
        logger.info(f"Retrieved data: {response['Items']}")
        
        # Return a properly formatted response
        return {
            "statusCode": 200,
            "body": json.dumps(response['Items']),  # Serialize the body as a JSON string
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error retrieving data: {str(e)}"}),  # Serialize error message
            "headers": {
                "Content-Type": "application/json"
            }
        }