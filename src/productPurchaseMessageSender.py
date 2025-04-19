import json
import boto3
import logging
import os
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Determine HTTP method
        http_method = event['httpMethod']
        
        if http_method == 'POST':
            body['action'] = 'create'  # Add an action field to indicate a creation
        
        elif http_method == 'PUT':
            if 'ProductPurchaseId' not in body:
                logger.error("Missing 'ProductPurchaseId' field for update operation")
                # Raise a ClientError for missing ProductPurchaseId
                raise ClientError(
                    error_response={
                        'Error': {
                            'Code': 'ValidationException',
                            'Message': "Missing 'ProductPurchaseId' field for update operation"
                        }
                    },
                    operation_name='PutProductPurchase'
                )
            body['action'] = 'update'  # Add an action field to indicate an update
            
        else:
            # Handle unsupported methods
            logger.error(f"Method {http_method} not allowed")
            # Raise a ClientError for unsupported methods
            raise ClientError(
                error_response = {
                    'Error': {
                        'Code': 'NotImplementedException',
                        'Message': f"Method {http_method} not allowed"
                    }
                },
                operation_name = 'UnsupportedMethod'
            )   
        
        # Send message to SQS queue
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body)
        )
        
        logger.info('Message sent to queue', extra={
            'message_id': response['MessageId'],
            'payload': body
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Message sent successfully',
                'messageId': response['MessageId']
            })
        }
        
    except ClientError as e:
        logger.error(f"Error sending message: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(e)
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }