import datetime
from typing import Optional, Any, List

from pydantic import BaseModel


class BaseTemplate(BaseModel):
    pass


class GetListSettingsRequest(BaseTemplate):
    parameters: List[str]


class GetListSettingsResponse(BaseTemplate):
    settings: Optional[Any]
    time_last_maintained: Optional[datetime.datetime]
    error_message: Optional[str]
