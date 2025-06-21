import json
from src.clients.cognito_client import authenticate_event
from src.utils.logging import log, setup_log

def login(event, context):
    setup_log(event, context)
    log('Request to /login')
    # Authenticate using Cognito JWT
    claims = authenticate_event(event)
    if not claims:
        log('Unauthorized: Invalid or missing token')
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Unauthorized'})
        }
    log(f"Authorized request to /login for sub={claims.get('sub')}")
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Login successful', 'claims': claims})
    }