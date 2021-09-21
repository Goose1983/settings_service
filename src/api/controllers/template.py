import asyncio
from typing import Any

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection

from src.api import injections
from src.api.schemas.template import TemplateRequest, TemplateResponse
from src.models.template import template

router = APIRouter()


@router.post("/insert_example", response_model=TemplateResponse)
async def template_post(request: TemplateRequest, db: Connection = Depends(injections.get_db),
                        logger=Depends(injections.get_logger)) -> TemplateResponse:
    logger.info("Start processing")
    try:
        with db as connection:
            connection.execute(template.insert(
                {
                    "ID": request.request_id,
                    "NAME": request.name,
                    "VALUE": request.value,
                    "VERSION": request.version
                }))

        response = TemplateResponse(request_id=request.request_id, result="success")
    except Exception as e:
        logger.info("Error caught")
        response = TemplateResponse(request_id=request.request_id, result="error", error_code=-1, error_message=str(e))

    logger.info("End processing")
    return response


@router.post("/import_example")
async def template_post(request: TemplateRequest) -> Any:
    # Импортируем модуль по полному имени
    # Для примера - синхронный HTTP-клиент "requests"
    requests = __import__("requests")
    result = requests.get("https://httpbin.org")
    return {"result_status_code": result.status_code}


@router.post("/gather_example")
async def template_gather(request: TemplateRequest) -> Any:
    # Тут используем асинхронный HTTP-клиент
    async with httpx.AsyncClient() as client:
        # coros - список корутин, завершения которых мы хотим дождаться
        coros = [client.get("https://httpbin.org") for _ in range(10)]
        results = await asyncio.gather(*coros)

    codes = [r.status_code for r in results]
    return {"result_status_codes": codes}
