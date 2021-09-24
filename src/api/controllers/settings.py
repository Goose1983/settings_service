from fastapi import APIRouter, Depends

from src.api import injections
from src.api.schemas.settings import GetListSettingsResponse, GetListSettingsRequest
from src.settings_fabric.settings_creator import SettingsCreator

router = APIRouter()


@router.get("/", response_model=GetListSettingsResponse)
async def ksup_cacher_get(request: GetListSettingsRequest,
                          logger=Depends(injections.get_logger)) -> GetListSettingsResponse:
    """Функция получения настроек кэшера КСУП"""
    logger.info("Запрос настроек кэшера")
    try:
        settings_creator = SettingsCreator(request.parameters)
        return GetListSettingsResponse(
            settings=settings_creator.get_settings(),
            time_last_maintained=settings_creator.get_time_last_maintained()
        )
    except Exception as e:
        return GetListSettingsResponse(
            error_message=str(e)
        )



