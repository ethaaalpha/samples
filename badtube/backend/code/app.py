import logging
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from controllers.dao.sys.engine import clear_db, init_db
from objects.user import User
from routes import comments, movies, stream
from routes.tools.dependencies import get_context_user

# logger configuration
logging.basicConfig(format="(%(levelname)s)[%(filename)s]: %(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)

# database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # clear_db()
    init_db()
    yield

# fast api
app = FastAPI(debug=True, lifespan=lifespan)
app.include_router(movies.router)
app.include_router(comments.router)
app.include_router(stream.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/auth")
def test(user: Annotated[User, Depends(get_context_user)]) -> User:
    return user
