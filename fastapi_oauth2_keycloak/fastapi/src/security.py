from typing import Annotated
from fastapi import Depends, HTTPException
from authlib.jose import jwt, JWTClaims, JoseError, KeySet
from db.config import SessionConnector
from db.models.User import User
from keycloak import get_key_set, oauth2_scheme

async def validate_token(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    key_set: Annotated[KeySet, Depends(get_key_set)],
) -> JWTClaims:
    if not access_token:
        raise HTTPException(401, detail="No access_token provided")
    try:
        claims = jwt.decode(access_token, key_set)
        claims.validate()
        return claims
    except (JoseError, ValueError):
        raise HTTPException(401, detail="Invalid access token")

async def get_context_user(claims: Annotated[JWTClaims, Depends(validate_token)], session: SessionConnector):
    id = claims.get("sub")
    user = session.get(User, id)

    if not user:
        print(f"ici {id}")
        print("Utilisateur non existant")
        user = User(id=id)
        session.add(User(id=id))
        session.commit()
    else:
        print("Utilisateur existant")
    return user

ContextUser = Annotated[User, Depends(get_context_user)]