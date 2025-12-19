def calculate_gross_pnl(
    side: str,
    entry_price: float,
    exit_price: float,
    quantity: int,
) -> float:
    if side == "BUY":
        return (exit_price - entry_price) * quantity
    else:  # SELL
        return (entry_price - exit_price) * quantity


def calculate_charges(turnover: float) -> float:
    """
    Very basic model:
    0.03% of turnover (both sides combined)
    """
    return turnover * 0.0003


def calculate_net_pnl(
    side: str,
    entry_price: float,
    exit_price: float,
    quantity: int,
) -> float:
    if side == "BUY":
        gross = (exit_price - entry_price) * quantity
    else:
        gross = (entry_price - exit_price) * quantity

    turnover = (entry_price + exit_price) * quantity
    charges = turnover * 0.0003

    return gross - charges
