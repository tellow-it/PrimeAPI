from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from routers.base_router import main_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              description="API for creating tasks for company Prime",
              )

app.include_router(prefix='/prime', router=main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
register_tortoise(
    app,
    db_url=settings.DATABASE_URL_R,
    modules={"models": ["database.models.building",
                        "database.models.important",
                        "database.models.status",
                        "database.models.system",
                        "database.models.user",
                        "database.models.order"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=jsonable_encoder({"detail_error": str(exc)}))
