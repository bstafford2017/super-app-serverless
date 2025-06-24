# Handler for Cognito authorizer
import requests
from jose import jwt

COGNITO_REGION = 'us-east-2'  # Update as needed
USER_POOL_ID = 'us-east-1_UsOf5uctI'  # Replace with your Cognito User Pool ID
CLIENT_ID = 'bf8cdaqjoqh3o5fu7fd3brc20'    # Replace with your Cognito App Client ID

def get_cognito_jwks():
    jwks_url = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    return response.json()

def verify_jwt_token(token: str):
    jwks = get_cognito_jwks()
    try:
        claims = jwt.decode(
            token,
            jwks,
            algorithms=['RS256'],
            audience=CLIENT_ID,
            issuer=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}'
        )
        return claims
    except Exception as e:
        # Replace with your logging if needed
        print(f"Token verification failed: {e}")
        return None

def authenticate_event(event):
    auth_header = event.get('headers', {}).get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    return verify_jwt_token(token)

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
