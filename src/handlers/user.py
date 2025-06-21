# Handler for user endpoint
import json
from logging import log, setup_log

def login(event, context):
    setup_log(event, context)
    log('Request to /login')
    # Authenticate using Cognito JWT (handled by API Gateway)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Login successful'})
    }
