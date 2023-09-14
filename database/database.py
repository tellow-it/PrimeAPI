from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

from core.config import settings


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["database.models.building",
                            "database.models.important",
                            "database.models.status",
                            "database.models.system",
                            "database.models.user",
                            "database.models.order",
                            "aerich.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["database.models.building",
                       "database.models.important",
                       "database.models.status",
                       "database.models.system",
                       "database.models.user",
                       "database.models.order",
                       "aerich.models"],
            "default_connection": "default",
        },
    },
}
