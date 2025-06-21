# Handler for user endpoint
import json
from src.clients.cognito_client import insert_user, lookup_user
from src.utils.logging import log, setup_log
from src.models.user import User

def login(event, context):
    setup_log(event, context)
    log('Request to /login')
    # Authenticate using Cognito JWT (handled by API Gateway)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Login successful'})
    }
