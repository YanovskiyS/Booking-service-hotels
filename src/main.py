import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.api.hotels import router as router_hotels  # noqa E402
from src.api.auth import router as router_auths  # noqa E402
from src.api.rooms import router as router_rooms  # noqa E402
from src.api.bookings import router as routers_bookings  # noqa E402
from src.api.facilities import router as routers_facilities  # noqa E402
from src.api.images import router as images_router  # noqa E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.init import redis_manager

    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPICache initialized")
    yield
    await redis_manager.close()


app = FastAPI(docs_url=None, lifespan=lifespan)

app.include_router(router_auths)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(routers_bookings)
app.include_router(routers_facilities)
app.include_router(images_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
