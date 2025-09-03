from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """
    Schema for validating user registration input.
    """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    role: Optional[str] = "staff"
