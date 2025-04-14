# Send message to SQS queue directly
# This is useful for testing the SQS queue directly without going through the API Gateway
# Make sure to replace the queue URL with your own
# You can use the AWS CLI to send a message to the SQS queue
aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/484907526888/product-purchase-queue --message-body file://message-body-1.json 

# Basic test
# This is a basic test to send a message to the API Gateway
# Make sure to replace the URL with your own
curl -X POST https://4u5kyy3y7f.execute-api.us-east-1.amazonaws.com/Prod/product-purchase \
-H "Content-Type: application/json" \
-d @tests/message-body-1.json

# With verbose output
curl -v -X POST https://rgd3o8kko2.execute-api.us-east-1.amazonaws.com/Prod/product-purchase \
-H "Content-Type: application/json" \
-d @tests/message-body-1.json

# With custom domain
# This is a test to send a message to the API Gateway with a custom domain
# Make sure to replace the URL with your own
curl -X POST https://api.visiotechno.net/product-purchase/ \                                                
-H "Content-Type: application/json" \
-d @tests/message-body-1.json