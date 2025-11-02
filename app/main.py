import time

from fastapi import FastAPI, Request, Response
from loguru import logger
from typing_extensions import Callable

from app.routers.comments import router as comments_router
from app.routers.posts import router as posts_router
from app.routers.tags import router as tags_router

app = FastAPI()


@app.middleware("http")
async def add_requests_process_time(request: Request, call_next: Callable) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.debug(f"Request processed in {process_time:.1f}s")
    return response


app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(tags_router, prefix="/tags", tags=["Tags"])
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
