from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
import base64
from .config import settings
import jwt
import httpx
from jose import jwt, JWTError

security = HTTPBearer()

def get_privy_headers():
    auth_header = base64.b64encode(
        f'{settings.PRIVY_APP_ID}:{settings.PRIVY_APP_SECRET}'.encode()
    ).decode()
    return {
        'Authorization': f'Basic {auth_header}',
        'privy-app-id': settings.PRIVY_APP_ID
    }

appId = settings.PRIVY_APP_ID

# verify privy authentication
async def verify_token(token: str = Security(security)):
    print('verifying token')
    try:
        # Fetch the JWKS from the endpoint
        jwks_url = settings.PRIVY_JWKS_URL
        async with httpx.AsyncClient() as client:
            jwks_response = await client.get(jwks_url)
            jwks_data = jwks_response.json()

        key_id = jwt.get_unverified_header(token.credentials)['kid']
        public_key = next(key for key in jwks_data['keys'] if key['kid'] == key_id)

        decoded = jwt.decode(token.credentials, public_key, issuer='privy.io', audience=appId)
        print(decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Error verifying token: {e}")
        raise HTTPException(status_code=401)