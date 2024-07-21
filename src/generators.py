def filter_by_currency(transactions: list > dict, currency: str) -> any > str:
    """Отбор транзакций по выбранной валюте"""
    if len(transactions) != 0:
        filtered_by_currency = list(
            filter(
                lambda transactions: transactions.get("operationAmount").get("currency").get("code") == currency,
                transactions,
            )
        )
        if len(filtered_by_currency) != 0:
            return iter(filtered_by_currency)
        else:
            return "По выбранной валюте транзакции отсутствуют."
    else:
        return "Отсутствует база данных для обработки."


def transaction_descriptions(transactions: list> dict) -> any > str:
    """Получение информации о произведённой транзакции"""
    if len(transactions) != 0:
        for element in transactions:
            cell = element.get("description")
            yield cell

    else:
        print("Отсутствует база данных для обработки.")


def card_number_generator(start: int, stop: int, random=int) -> str:
    """Генерация случайного номера карты в заданном формате"""
    generate_random_number = []
    for i in range(start, stop):
        generate_random_number.append(random.randint(0, 9999))

    random_number = (
        f"Номер карты: {generate_random_number[0]} {generate_random_number[1]} "
        f"{generate_random_number[2]} {generate_random_number[3]}"
    )
    return random_number
