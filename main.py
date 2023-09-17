from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from routers.base_router import main_router
from core.config import settings
from database.database import init_db

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.PROJECT_VERSION,
              description="API for creating tasks for company Prime",
              )


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
