aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/484907526888/product-purchase-queue --message-body file://message-body-1.json 

# Basic test
curl -X POST https://4u5kyy3y7f.execute-api.us-east-1.amazonaws.com/Prod/purchase \
-H "Content-Type: application/json" \
-d @tests/message-body-1.json

# With verbose output
curl -v -X POST https://4u5kyy3y7f.execute-api.us-east-1.amazonaws.com/Prod/purchase \
-H "Content-Type: application/json" \
-d @test/payload.json