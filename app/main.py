from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.middlewares import RequestProcessTimeMiddleware
from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.posts import router as posts_router
from app.routers.tags import router as tags_router
from app.routers.users import router as users_router

app = FastAPI()

# Add middlewares
app.add_middleware(RequestProcessTimeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(tags_router, prefix="/tags", tags=["Tags"])
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
