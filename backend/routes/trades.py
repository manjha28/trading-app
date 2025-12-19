from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from routes.auth import get_current_user
from database import SessionLocal
from models import Trade, User
from schemas import TradeCreate, TradeResponse, TradeClose
from utils.pnl import calculate_gross_pnl, calculate_charges, calculate_net_pnl
from datetime import datetime
from fastapi import HTTPException


router = APIRouter(prefix="/api/trades", tags=["Trades"])

# --------------------
# DB Dependency
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------
# Routes
# --------------------
@router.post("/", response_model=TradeResponse)
@router.post("/", response_model=TradeResponse)
def add_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pnl = None

    if trade.exit_price is not None:
        pnl = calculate_net_pnl(
            trade.side,
            trade.entry_price,
            trade.exit_price,
            trade.quantity,
        )

    new_trade = Trade(
        user_id=current_user.id,
        symbol=trade.symbol,
        instrument_type=trade.instrument_type,
        side=trade.side,
        quantity=trade.quantity,
        entry_price=trade.entry_price,
        exit_price=trade.exit_price,
        entry_time=trade.entry_time,
        exit_time=trade.exit_time,
        pnl=pnl,
        fees=0.0,
        notes=trade.notes,
    )

    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade

@router.get("/open", response_model=list[TradeResponse])
def open_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.exit_time.is_(None),
        )
        .order_by(Trade.entry_time.desc())
        .all()
    )





@router.get("/", response_model=list[TradeResponse])
def list_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Trade)
        .filter(Trade.user_id == current_user.id)
        .order_by(Trade.trade_date.desc())
        .all()
    )



@router.get("/closed", response_model=list[TradeResponse])
def closed_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.exit_time.isnot(None),
        )
        .order_by(Trade.exit_time.desc())
        .all()
    )


@router.post("/{trade_id}/close", response_model=TradeResponse)
def close_trade(
    trade_id: int,
    data: TradeClose,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trade = (
        db.query(Trade)
        .filter(
            Trade.id == trade_id,
            Trade.user_id == current_user.id,
        )
        .first()
    )

    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    if trade.exit_time is not None:
        raise HTTPException(status_code=400, detail="Trade already closed")

    trade.exit_price = data.exit_price
    trade.exit_time = datetime.utcnow()
    trade.pnl = calculate_net_pnl(
        trade.side,
        trade.entry_price,
        trade.exit_price,
        trade.quantity,
    )

    db.commit()
    db.refresh(trade)

    return trade
