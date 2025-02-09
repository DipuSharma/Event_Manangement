from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from fastapi import status


class ResponseModel(BaseModel):
    """
    Base Response Model
    """

    data: Any = {}
    status_code: int = status.HTTP_200_OK
    success: bool = True
    message: str = "Request handled successfully"


class ErrorResponseModel(BaseModel):
    """
    Base Error Model
    """

    error: Any = {}
    status_code: int = status.HTTP_400_BAD_REQUEST
    success: bool = False
    message: str = "Request could not be processed"
