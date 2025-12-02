from functools import cache
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.jose import JsonWebKey, KeySet, JWTClaims, JoseError, jwt
from settings import get_settings
import requests

@cache
def get_keys():
    settings = get_settings()

    rq = requests.get(f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs")
    rq.raise_for_status()

    return JsonWebKey.import_key_set(rq.json())

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/token?client_id=web",
    authorizationUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/auth?client_id=web&response_type=code&scope=email",
    refreshUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/token",
)

def validate_token(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    key_set: Annotated[KeySet, Depends(get_keys)],
) -> JWTClaims:
    if not access_token:
        raise HTTPException(401, detail="No access_token provided")
    try:
        claims = jwt.decode(access_token, key_set)
        claims.validate()
        return claims
    except (JoseError, ValueError):
        raise HTTPException(401, detail="Invalid access token")
