import json
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.data_source import engine
from src.api.routers import api_router


app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup():
    # В этом месте нужно еще затянуть все конфиги из БД и выполнить инициализацию моделей
    pass


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(format='%(asctime)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        filename='MATRIX_settings.log',
                        level=settings.LOGGING_LEVEL)
    logging.info('запуск сервиса получения настроек матрицы предложений')

    uvicorn.run(app)
