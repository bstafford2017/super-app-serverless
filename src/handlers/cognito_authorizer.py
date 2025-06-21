# Handler for Cognito authorizer
import json
from cognito_client import verify_jwt_token

def lambda_handler(event, context):
    token = event.get('authorizationToken')
    method_arn = event.get('methodArn')
    if not token or not token.startswith('Bearer '):
        return generate_policy('user', 'Deny', method_arn)
    jwt_token = token.split(' ')[1]
    claims = verify_jwt_token(jwt_token)
    if claims:
        return generate_policy(claims.get('sub', 'user'), 'Allow', method_arn)
    else:
        return generate_policy('user', 'Deny', method_arn)

def generate_policy(principal_id, effect, resource):
    auth_response = {'principalId': principal_id}
    if effect and resource:
        auth_response['policyDocument'] = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    return auth_response
