# ============================================================
# ЗАДАНИЕ 3: Рефакторинг плохого кода
# Тема: расчёт комиссии за банковский перевод
# ============================================================


# ===== ИСХОДНЫЙ «ПЛОХОЙ» КОД (намеренно написан плохо) =====

def f(a, b, c, d):
    # считаем комиссию
    x = 0
    if c == "RUB":
        if a == "checking":
            if b > 0 and b <= 1000:
                x = b * 0.01
                if x < 10:
                    x = 10
            if b > 1000 and b <= 50000:
                x = b * 0.015
                if x < 10:
                    x = 10
            if b > 50000 and b <= 500000:
                x = b * 0.02
                if x < 10:
                    x = 10
            if b > 500000:
                x = b * 0.025
                if x < 10:
                    x = 10
        if a == "savings":
            if b > 0 and b <= 1000:
                x = b * 0.005
                if x < 5:
                    x = 5
            if b > 1000 and b <= 50000:
                x = b * 0.008
                if x < 5:
                    x = 5
            if b > 50000 and b <= 500000:
                x = b * 0.01
                if x < 5:
                    x = 5
            if b > 500000:
                x = b * 0.015
                if x < 5:
                    x = 5
    if c == "USD" or c == "EUR":
        x = b * 0.03
        if a == "savings":
            x = b * 0.02
        if x < 15:
            x = 15
    if d == True:
        x = x * 0.9
    if b <= 0:
        x = -1
    return x


# ============================================================
# ПРОБЛЕМЫ В КОДЕ (выявленные при ревью):
#
# 1. Имя функции `f` — полностью неинформативное.
# 2. Параметры `a`, `b`, `c`, `d` — нет понимания что это.
# 3. Переменная `x` — непонятное имя для результата.
# 4. Магические числа: 0.01, 0.015, 10, 5, 50000, 500000 — нет констант.
# 5. Дублирование кода: блок `if x < MIN: x = MIN` повторяется 8 раз.
# 6. Длина функции > 40 строк, делает сразу всё.
# 7. Нет обработки ошибок — возврат -1 вместо исключения.
# 8. `if d == True` — антипаттерн, нужно просто `if d`.
# 9. Нет разделения логики: тип счёта, валюта, скидка — всё в одной функции.
# ============================================================


# ===== РЕФАКТОРИРОВАННЫЙ КОД =====

from dataclasses import dataclass
from typing import Literal

AccountType = Literal["checking", "savings"]
Currency = Literal["RUB", "USD", "EUR"]

# Минимальные комиссии по типу счёта
MIN_FEE_RUB: dict[AccountType, float] = {
    "checking": 10.0,
    "savings": 5.0,
}
MIN_FEE_FOREIGN = 15.0

# Ставки комиссии для RUB: (порог суммы, ставка)
RATES_RUB: dict[AccountType, list[tuple[float, float]]] = {
    "checking": [
        (1_000.0,   0.010),
        (50_000.0,  0.015),
        (500_000.0, 0.020),
        (float("inf"), 0.025),
    ],
    "savings": [
        (1_000.0,   0.005),
        (50_000.0,  0.008),
        (500_000.0, 0.010),
        (float("inf"), 0.015),
    ],
}

RATES_FOREIGN: dict[AccountType, float] = {
    "checking": 0.03,
    "savings": 0.02,
}

PREMIUM_DISCOUNT = 0.9


def _get_rub_fee(amount: float, account_type: AccountType) -> float:
    for threshold, rate in RATES_RUB[account_type]:
        if amount <= threshold:
            return max(amount * rate, MIN_FEE_RUB[account_type])
    return max(amount * RATES_RUB[account_type][-1][1], MIN_FEE_RUB[account_type])


def _get_foreign_fee(amount: float, account_type: AccountType) -> float:
    return max(amount * RATES_FOREIGN[account_type], MIN_FEE_FOREIGN)


def calculate_transfer_fee(
    amount: float,
    account_type: AccountType,
    currency: Currency,
    is_premium: bool = False,
) -> float:
    """
    Рассчитать комиссию за банковский перевод.

    Args:
        amount: сумма перевода (должна быть > 0)
        account_type: тип счёта ('checking' или 'savings')
        currency: валюта перевода
        is_premium: премиум-клиент получает скидку 10%

    Returns:
        Размер комиссии в той же валюте

    Raises:
        ValueError: если amount <= 0
    """
    if amount <= 0:
        raise ValueError(f"Сумма перевода должна быть положительной, получено: {amount}")

    if currency == "RUB":
        fee = _get_rub_fee(amount, account_type)
    else:
        fee = _get_foreign_fee(amount, account_type)

    if is_premium:
        fee *= PREMIUM_DISCOUNT

    return round(fee, 2)


# ============================================================
# ИТОГ РЕФАКТОРИНГА:
#
# ✅ Имя функции `calculate_transfer_fee` — описывает назначение.
# ✅ Параметры именованы: amount, account_type, currency, is_premium.
# ✅ Константы вынесены: MIN_FEE_RUB, RATES_RUB и т.д.
# ✅ Дублирование устранено: логика минимальной комиссии — в одном месте.
# ✅ Функция разбита на три: основная + две вспомогательные.
# ✅ Обработка ошибок через ValueError вместо возврата -1.
# ✅ `if is_premium` вместо `if d == True`.
# ✅ Добавлена документация (docstring).
# ============================================================
