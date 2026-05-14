"""
Задание 10: Генерация регулярного выражения

Промпт в Claude Code:
    "Сгенерируй регулярное выражение для валидации номера банковского счёта.
     Формат: 2 заглавные латинские буквы (код страны) + 18 цифр.
     Пример валидного: RU123456789012345678
     Пример невалидного: ru123456789012345678 (строчные буквы)
     Также сгенерируй скрипт тестирования на 5 валидных и 5 невалидных примерах."
"""

import re

# Паттерн: 2 заглавные буквы A-Z, затем ровно 18 цифр
ACCOUNT_NUMBER_PATTERN = re.compile(r"^[A-Z]{2}\d{18}$")


def is_valid_account_number(value: str) -> bool:
    """Проверить, соответствует ли строка формату номера счёта."""
    return bool(ACCOUNT_NUMBER_PATTERN.match(value))


# ============================================================
# Тестирование
# ============================================================

VALID_EXAMPLES = [
    "RU123456789012345678",   # стандартный российский формат
    "US000000000000000001",   # американский, нули допустимы
    "DE999999999999999999",   # максимальные цифры
    "GB000000000000000000",   # все нули
    "AA111111111111111111",   # буквы из начала алфавита
]

INVALID_EXAMPLES = [
    "ru123456789012345678",   # строчные буквы
    "R1123456789012345678",   # цифра вместо второй буквы
    "RU12345678901234567",    # 17 цифр (мало)
    "RU1234567890123456789",  # 19 цифр (много)
    "RU12345678901234567X",   # буква в конце
]


def run_tests() -> None:
    print("=== Валидные номера счётов ===")
    for number in VALID_EXAMPLES:
        result = is_valid_account_number(number)
        status = "OK" if result else "FAIL"
        print(f"  [{status}] {number!r}")

    print("\n=== Невалидные номера счётов ===")
    for number in INVALID_EXAMPLES:
        result = is_valid_account_number(number)
        status = "OK" if not result else "FAIL"
        print(f"  [{status}] {number!r}")

    all_valid = all(is_valid_account_number(n) for n in VALID_EXAMPLES)
    all_invalid = all(not is_valid_account_number(n) for n in INVALID_EXAMPLES)

    print(f"\nРезультат: {'все тесты пройдены' if all_valid and all_invalid else 'ЕСТЬ ОШИБКИ'}")


if __name__ == "__main__":
    run_tests()
