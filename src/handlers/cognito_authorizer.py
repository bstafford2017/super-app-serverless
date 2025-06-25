# Handler for Cognito authorizer
import requests
from jose import jwt
import json

COGNITO_REGION = 'us-east-2'  # Update as needed
USER_POOL_ID = 'us-east-1_UsOf5uctI'  # Replace with your Cognito User Pool ID
CLIENT_ID = 'bf8cdaqjoqh3o5fu7fd3brc20'    # Replace with your Cognito App Client ID

def get_cognito_jwks():
    jwks_url = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
    print(f"Fetching JWKS from: {jwks_url}")
    response = requests.get(jwks_url)
    print(f"JWKS fetch status: {response.status_code}")
    return response.json()

def verify_jwt_token(token: str):
    print(f"Verifying JWT token: {token[:20]}... (truncated)")
    jwks = get_cognito_jwks()
    try:
        claims = jwt.decode(
            token,
            jwks,
            algorithms=['RS256'],
            audience=CLIENT_ID,
            issuer=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}'
        )
        print(f"JWT claims: {json.dumps(claims)}")
        return claims
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

def authenticate_event(event):
    print(f"Authenticating event: {json.dumps(event)}")
    auth_header = event.get('headers', {}).get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        print("No Bearer token found in Authorization header.")
        return None
    token = auth_header.split(' ')[1]
    return verify_jwt_token(token)

def lambda_handler(event, context):
    print(f"Lambda event: {json.dumps(event)}")
    token = event.get('authorizationToken')
    method_arn = event.get('methodArn')
    print(f"Token: {token}, Method ARN: {method_arn}")
    if not token or not token.startswith('Bearer '):
        print("No valid Bearer token provided.")
        return generate_policy('user', 'Deny', method_arn)
    jwt_token = token.split(' ')[1]
    claims = verify_jwt_token(jwt_token)
    if claims:
        print("Token valid, generating Allow policy.")
        return generate_policy(claims.get('sub', 'user'), 'Allow', method_arn)
    else:
        print("Token invalid, generating Deny policy.")
        return generate_policy('user', 'Deny', method_arn)

def generate_policy(principal_id, effect, resource):
    print(f"Generating policy: principal_id={principal_id}, effect={effect}, resource={resource}")
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
    print(f"Auth response: {json.dumps(auth_response)}")
    return auth_response
