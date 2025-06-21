import requests
from jose import jwt

COGNITO_REGION = 'us-east-2'  # Update as needed
USER_POOL_ID = 'your_user_pool_id'  # Replace with your Cognito User Pool ID
CLIENT_ID = 'your_app_client_id'    # Replace with your Cognito App Client ID

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
