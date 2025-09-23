# from typing import List, Optional
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    status:str = Field(default="Success", description="Response Status")

class ErrorResponse(BaseModel):
    error:str = Field(..., description="Error Details")
    status:str = Field(default="error", description="Error Message")


