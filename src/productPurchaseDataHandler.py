import json
import boto3
import logging
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

database = boto3.resource('dynamodb')
table = database.Table('ProductPurchase')

def lambda_handler(event, context):
    
    try:
        for record in event["Records"]:
            
            payload = json.loads(record["body"])
            if payload['action'] == 'create':
                payload['ProductPurchaseId'] = str(uuid.uuid4())
            payload['CreatedAt'] = datetime.now().isoformat()
            
            logger.info('Processing record', extra={
                'payload': payload,
                'message_id': record.get('messageId'),
                'event_source': record.get('eventSource')
            })
            
            table.put_item(Item=payload)
        
        logger.info('Successfully inserted items into DynamoDB')
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully inserted data!"
            })
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