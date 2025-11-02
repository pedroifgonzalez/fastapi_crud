from fastapi import FastAPI

from app.routers.posts import router as posts_router
from app.routers.tags import router as tags_router

app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(tags_router, prefix="/tags", tags=["Tags"])
