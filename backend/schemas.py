from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class TradeCreate(BaseModel):
    instrument_type: str
    symbol: str
    side: str
    quantity: int

    entry_price: float
    exit_price: Optional[float] = None

    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None

    option_type: Optional[str] = None
    strike_price: Optional[float] = None
    expiry_date: Optional[date] = None

    lot_size: Optional[int] = None
    fees: Optional[float] = 0.0
    notes: Optional[str] = None


class TradeResponse(TradeCreate):
    id: int
    pnl: Optional[float]

    class Config:
        from_attributes = True        


class TradeClose(BaseModel):
    exit_price: float