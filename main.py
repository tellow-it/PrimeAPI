from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers.base_router import main_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              description="API for creating tasks for company Prime",
              )
app.include_router(prefix='/prime', router=main_router)
register_tortoise(
    app,
    db_url=settings.DATABASE_URL_R,
    modules={"models": ["database.models.building",
                        "database.models.important",
                        "database.models.role",
                        "database.models.status",
                        "database.models.system",
                        "database.models.user",
                        "database.models.order"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
