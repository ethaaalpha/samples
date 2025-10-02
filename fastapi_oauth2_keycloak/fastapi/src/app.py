from typing import Annotated
from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from db.config import create_db_and_tables
from db.models.User import User
from starlette.middleware.sessions import SessionMiddleware
from keycloak import oauth2
from security import ContextUser

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("httpx")
logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="dumb_secret")

@app.get("/login")
async def login(request: Request):
    return await oauth2.keycloak.authorize_redirect(
        request,
        redirect_uri="http://localhost:8080/auth/callback"
    )

@app.get("/auth/callback")
async def callback(request: Request):
    token = await oauth2.keycloak.authorize_access_token(request)
    
    return { "token": token }

# you can test this endpoint easily by doing using curl (access_token retrieved on /login)
# curl -X GET http://localhost:8080/me \
#  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
@app.get("/me")
async def me(user: ContextUser):
    return user
