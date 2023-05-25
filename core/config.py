from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_NAME: str = 'PRIME'
    PROJECT_VERSION: str = '1.0.0'

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    POSTGRES_USER_R: str = os.getenv("POSTGRES_USER_R")
    POSTGRES_PASSWORD_R = os.getenv("POSTGRES_PASSWORD_R")
    POSTGRES_SERVER_R: str = os.getenv("POSTGRES_SERVER_R")
    POSTGRES_PORT_R: str = os.getenv("POSTGRES_PORT_R")
    POSTGRES_DB_R: str = os.getenv("POSTGRES_DB_R")
    DATABASE_URL_R: str = f"postgres://{POSTGRES_USER_R}:{POSTGRES_PASSWORD_R}" \
                          f"@{POSTGRES_SERVER_R}/{POSTGRES_DB_R}"

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")


settings = Settings()
