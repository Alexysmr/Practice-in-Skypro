import logging
from pathlib import Path

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
main_path = Path(__file__).resolve().parents[1]
file_handler = logging.FileHandler(f'{main_path}/logs/masks.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(numbers) -> str:
    """Функция получения номера банковской карты и вывода в заданном формате"""
    logger.info('Старт')
    logger.info(f'Получаем номер карты от пользователя: {numbers}')
    card_numbers = []
    logger.info('Обрабатываем полученные данные')
    try:
        for num in numbers:
            if num.isdigit():  # Даём возможность проявится ошибке
                card_numbers.append(int(num))
        if len(card_numbers) == 16:
            first_group = "".join(str(item) for item in card_numbers[0:4])
            second_group = "".join(str(item) for item in card_numbers[4:6])
            last_group = "".join(str(item) for item in card_numbers[-4:])
            mask_number = f"{first_group} {second_group}** **** {last_group}"
            logger.info(f'Программа выполнена и завершена: {mask_number}')
            return mask_number
        else:
            logger.info('Ошибка ввода! Функция завершена.')
            return 'Введён некорректный номер карты'
    except Exception as ex:
        logger.error(f"Ошибка {ex}")
        return 'Введён некорректный номер карты'


def get_mask_account(bank_account) -> str:
    """Функция получения банковского счёта и вывода в заданном формате"""
    logger.info('Старт')
    logger.info(f'Получаем номер счёта от пользователя: {bank_account}')
    account_numbers = []
    logger.info('Обрабатываем полученные данные')
    try:
        for num in bank_account:
            if num.isdigit():  # Даём возможность проявится ошибке
                account_numbers.append(int(num))
        if len(account_numbers) == 20:
            mask = "".join(str(item) for item in account_numbers[0:])
            mask_account = f"**{mask[-4:]}"
            logger.info(f'Функция выполнена и завершена: {mask_account}')
            return mask_account
        else:
            logger.info('Ошибка ввода! Функция завершена.')
            return "Введён некорректный номер счёта"
    except Exception as ex:
        logger.error(f"Ошибка {ex}. Функция завершена.")
        return "Введён некорректный номер счёта"
