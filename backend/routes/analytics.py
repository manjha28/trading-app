from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from database import SessionLocal
from models import Trade, User
from routes.auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/overview")
def analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
        )
        .all()
    )

    total_trades = len(trades)

    if total_trades == 0:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_win": 0,
            "avg_loss": 0,
        }

    wins = [t.pnl for t in trades if t.pnl > 0]
    losses = [t.pnl for t in trades if t.pnl < 0]

    total_pnl = sum(t.pnl for t in trades)
    win_rate = (len(wins) / total_trades) * 100

    return {
        "total_trades": total_trades,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "avg_win": round(sum(wins) / len(wins), 2) if wins else 0,
        "avg_loss": round(sum(losses) / len(losses), 2) if losses else 0,
    }

@router.get("/daily")
def daily_pnl(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            func.date(Trade.entry_time).label("date"),
            func.sum(Trade.pnl).label("pnl"),
        )
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
        )
        .group_by(func.date(Trade.entry_time))
        .order_by(func.date(Trade.entry_time))
        .all()
    )

    return [
        {"date": r.date, "pnl": round(r.pnl, 2)}
        for r in results
    ]

@router.get("/equity-curve")
def equity_curve(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
            Trade.exit_time.isnot(None),
        )
        .order_by(Trade.exit_time)
        .all()
    )

    equity = 0
    curve = []

    for t in trades:
        equity += t.pnl
        curve.append({
            "date": t.exit_time.date(),
            "equity": round(equity, 2),
        })

    return curve

@router.get("/max-drawdown")
def max_drawdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
            Trade.exit_time.isnot(None),
        )
        .order_by(Trade.exit_time)
        .all()
    )

    equity = 0
    peak = 0
    max_dd = 0  # negative number

    for t in trades:
        equity += t.pnl

        if equity > peak:
            peak = equity

        drawdown = equity - peak
        if drawdown < max_dd:
            max_dd = drawdown

    return {
        "max_drawdown": round(max_dd, 2)
    }

@router.get("/streaks")
def win_loss_streaks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
            Trade.exit_time.isnot(None),
        )
        .order_by(Trade.exit_time)
        .all()
    )

    max_win_streak = 0
    max_loss_streak = 0
    current_win = 0
    current_loss = 0

    for t in trades:
        if t.pnl > 0:
            current_win += 1
            current_loss = 0
        elif t.pnl < 0:
            current_loss += 1
            current_win = 0
        else:
            current_win = 0
            current_loss = 0

        max_win_streak = max(max_win_streak, current_win)
        max_loss_streak = max(max_loss_streak, current_loss)

    return {
        "max_win_streak": max_win_streak,
        "max_loss_streak": max_loss_streak,
    }


@router.get("/best-worst-trade")
def best_worst_trade(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
        )
        .all()
    )

    if not trades:
        return {
            "best_trade": None,
            "worst_trade": None,
        }

    best = max(trades, key=lambda t: t.pnl)
    worst = min(trades, key=lambda t: t.pnl)

    return {
        "best_trade": {
            "id": best.id,
            "symbol": best.symbol,
            "pnl": round(best.pnl, 2),
        },
        "worst_trade": {
            "id": worst.id,
            "symbol": worst.symbol,
            "pnl": round(worst.pnl, 2),
        },
    }


@router.get("/best-worst-day")
def best_worst_day(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            func.date(Trade.exit_time).label("date"),
            func.sum(Trade.pnl).label("pnl"),
        )
        .filter(
            Trade.user_id == current_user.id,
            Trade.pnl.isnot(None),
            Trade.exit_time.isnot(None),
        )
        .group_by(func.date(Trade.exit_time))
        .all()
    )

    if not results:
        return {
            "best_day": None,
            "worst_day": None,
        }

    best = max(results, key=lambda r: r.pnl)
    worst = min(results, key=lambda r: r.pnl)

    return {
        "best_day": {
            "date": best.date,
            "pnl": round(best.pnl, 2),
        },
        "worst_day": {
            "date": worst.date,
            "pnl": round(worst.pnl, 2),
        },
    }
