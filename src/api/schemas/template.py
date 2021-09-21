from typing import Optional

from pydantic import BaseModel


class BaseTemplate(BaseModel):
    request_id: str


class TemplateRequest(BaseTemplate):
    name: str
    value: str
    version: Optional[int]


class TemplateResponse(BaseTemplate):
    result: str
    error_code: Optional[int]
    error_message: Optional[str]
