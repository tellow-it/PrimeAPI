from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
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
    db_url=settings.DATABASE_URL,
    modules={"models": ["database.models.building",
                        "database.models.important",
                        "database.models.status",
                        "database.models.system",
                        "database.models.user",
                        "database.models.order"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
