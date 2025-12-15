from fastapi import FastAPI , HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI() 

class UserCreate(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)
    email: str = Field(..., min_length=5, max_length=50)
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)

    @validator('email')
    def validate_email(cls, v):
        if len(v)<=5:
            raise ValueError('email must be more than 5')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v)<=5:
            raise ValueError('Username must be more than 5')
        return v
class UserResponse(BaseModel):
    username: str
    email: str
    age: int


@app.post("/register", response_model=UserResponse)
def register_user(data: UserCreate):
    # Example: check username logic
    if data.username.lower() == "admin":
        raise HTTPException(status_code=400, detail="Invalid username")

    # Mock response — normally save to database
    return UserResponse(
        username=data.username,
        email=data.email,
        age=data.age,
    )