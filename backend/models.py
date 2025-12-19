from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    instrument_type = Column(String, nullable=False)  # EQUITY | OPTION | FUTURE
    symbol = Column(String, nullable=False)

    side = Column(String, nullable=False)  # BUY | SELL
    quantity = Column(Integer, nullable=False)

    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)

    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)

    option_type = Column(String, nullable=True)  # CE | PE
    strike_price = Column(Float, nullable=True)
    expiry_date = Column(Date, nullable=True)

    lot_size = Column(Integer, nullable=True)

    pnl = Column(Float, nullable=True)
    fees = Column(Float, default=0.0)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship("User")
