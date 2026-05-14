from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class AccountCreate(BaseModel):
    owner_name: str = Field(..., min_length=2, max_length=100, examples=["Иван Иванов"])
    account_number: str = Field(..., pattern=r"^[A-Z]{2}\d{18}$", examples=["RU123456789012345678"])
    balance: float = Field(default=0.0, ge=0.0)
    currency: Literal["RUB", "USD", "EUR"] = "RUB"
    account_type: Literal["checking", "savings"] = "checking"

    @field_validator("owner_name")
    @classmethod
    def owner_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("owner_name не может быть пустым")
        return v.strip()


class AccountUpdate(BaseModel):
    owner_name: Optional[str] = Field(None, min_length=2, max_length=100)
    balance: Optional[float] = Field(None, ge=0.0)
    currency: Optional[Literal["RUB", "USD", "EUR"]] = None
    account_type: Optional[Literal["checking", "savings"]] = None
    is_active: Optional[bool] = None


class AccountResponse(BaseModel):
    id: int
    owner_name: str
    account_number: str
    balance: float
    currency: str
    account_type: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
