from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routers.base_router import main_router
from core.config import settings
from database.database import init_db
import sentry_sdk

sentry_sdk.init(
    dsn="https://157f9b059e579c9dc7e9635b0a0ebadd@o4505918971576320.ingest.sentry.io/4505918977212416",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              description="API for creating tasks for company Prime",
              )


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


@app.on_event("startup")
async def start_up():
    init_db(app)


app.include_router(prefix='/api', router=main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#
# @app.exception_handler(Exception)
# async def internal_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(status_code=500, content=jsonable_encoder({"detail_error": str(exc)}))
