from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_NAME: str = 'PRIME'
    PROJECT_VERSION: str = '1.0.0'

    POSTGRES_USER: str = os.getenv("DB_USER")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("DB_SERVER")
    POSTGRES_PORT: str = os.getenv("DB_PORT")
    POSTGRES_DB: str = os.getenv("DB_NAME")
    DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    JWT_ACCESS_SECRET_KEY: str = os.getenv("JWT_ACCESS_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

    ADMIN_TELEPHONE: str = os.getenv("ADMIN_TELEPHONE")


settings = Settings()

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
