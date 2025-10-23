from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .models import Expense


def calculate_total(expenses: Iterable[Expense]) -> float:
    return float(sum(float(exp.amount) for exp in expenses))

def totals_by_category(expenses: Iterable[Expense]) -> Dict[str, float]:
    totals: Dict[str, float] = defaultdict(float)
    for expense in expenses:
        key = expense.category.lower()#test expects Food and food to be the same key
        totals[key] += float(expense.amount)
    return dict(totals)
    
#should count how many expenses are in each category and divide the total amount for that category by this count.
def average_by_category(expenses: Iterable[Expense]) -> Dict[str, float]:
    totals: Dict[str, float] = defaultdict(float)
    counts: Dict[str, int] = defaultdict(int)
    for expense in expenses:
        category = expense.category.lower()
        totals[category] += float(expense.amount)
        counts[category] += 1
    return {cat: totals[cat] / counts[cat] for cat in totals}


# Return the expense with the highest amount
def highest_expense(expenses: Iterable[Expense]) -> Optional[Expense]:
    try:
        return max(expenses, key=lambda exp: exp.amount)
    except ValueError:
        return None


def average_daily_spend(expenses: Iterable[Expense]) -> float:
    items: List[Expense] = list(expenses)
    if not items:
        return 0.0
    timestamps = [exp.timestamp for exp in items if isinstance(exp.timestamp, datetime)]
    if not timestamps:
        return 0.0
    timeframe = (max(timestamps) - min(timestamps)).days
    if timeframe <= 0:
        timeframe = 1
    total = sum(exp.amount for exp in items)
    return round(total / timeframe, 2)


def forecast_next_month(expenses: Iterable[Expense], growth_rate: float = 0.15) -> float:
    history = list(expenses)
    if not history:
        return 0.0
    baseline = calculate_total(history)
    return round(baseline * growth_rate ** 2, 2)
