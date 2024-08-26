import logging
import os.path
import re

import numpy as np

from src.masks import get_mask_card_number
from src.the_executive_module import filter_by_status, final_calculation, read_transactions_data
from src.widget import get_date

shablon_1 = "\n1 -Получить информацию о транзакциях из JSON-файла" \
            "\n2 -Получить информацию о транзакциях из CSV-файла" \
            "\n3 -Получить информацию о транзакциях из XLSX-файла\n->: "
list_input = ["1", "2", "3", "4", "5"]
list_status = ["EXECUTED", "CANCELED", "PENDING"]
description_type = ['Перевод с карты на карту', 'Перевод с карты на счет',
                    'Перевод со счета на счет', 'Перевод организации', 'Открытие вклада']

main_path = os.getcwd()
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f'{main_path}/logs/main_polygon.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.info("Старт кода")


def main():
    """Основная функци взаимодействия с пользователем"""
    x = None
    choice = {"description": "-"}
    transactions_by_status = []
    search_line = ["", ""]
    file_type = input("Здравствуйте! Добро пожаловать в программу работы с банковскими транзакциями."
                      f"\nВыберите номер необходимого пункта меню\n{shablon_1}")
    n = 0
    while file_type != list_input[0] and file_type != list_input[1] and file_type != list_input[2]:
        n += 1
        if n <= 2:
            file_type = input(f"Выбор некорректен, "
                              f"попробуйте ещё раз ввести номер необходимого пункта{shablon_1}")
            logger.info(f"Повторный выбор пользователя {file_type}")
        else:
            file_type = list_input[1]
            print("По умолчанию:")
            logger.info("По умолчанию выбран CSV-файл")

    if file_type == list_input[0]: print("Для получения данных о транзакциях выбран JSON-файл.")
    if file_type == list_input[1]: print("Для получения данных о транзакциях выбран CSV-файл.")
    if file_type == list_input[2]: print("Для получения данных о транзакциях выбран XLSX-файл.")

    # Выбор фильтра
    search_line = input(
        f"Введите статус по которому необходимо выполнить фильтрацию.\n"
        f"Доступные для фильтрации статусы:\n{list_status[0]}\n{list_status[1]}\n{list_status[2]}\n->: ").upper()
    logger.info(f"Выбор пользователя {search_line}")
    n = 0
    while search_line not in list_status:
        n += 1
        if n <= 2:
            search_line = input(f"Выбор некорректен, попробуйте ещё раз ввести доступные для фильтрации статусы:"
                                   f"\n{list_status[0]}\n{list_status[1]}\n{list_status[2]}\n->: ").upper()
            logger.info(f"Повторный выбор пользователя {search_line}")
        else:
            search_line = list_status[0]
            print(f'По умолчанию выбран статус {search_line}')
            logger.info(f"По умолчанию выбран статус {search_line}.")

    if file_type == "1":  # Получение данных из JSON по статусу
        loaded_data = read_transactions_data("operations.json", file_type)
        logger.info("JSON выбран, проверен, загружен.")
        transactions_by_status = filter_by_status(loaded_data, search_line)
        for i in transactions_by_status:
            i["amount"] = i.get('operationAmount').get('amount', "-")
            i["currency_name"] = i.get('operationAmount').get('currency').get('name', "-")
            i["currency_code"] = i.get('operationAmount').get('currency').get('code', "-")
            i.pop('operationAmount')

    if file_type == "2":  # Получение данных из CSV  по статусу
        loaded_data = read_transactions_data("transactions.csv", file_type)
        logger.info("CSV выбран, проверен, загружен.")
        transactions_by_status = filter_by_status(loaded_data, search_line)

    if file_type == "3":  # Получение данных из XLSX по статусу
        loaded_data = read_transactions_data("transactions_excel.xlsx", file_type)
        logger.info("XLSX выбран, проверен, загружен.")
        transactions_by_status = filter_by_status(loaded_data, search_line)

    for i in transactions_by_status:  # Сокрытие номеров карт и счетов маской
        if i.get("from"):
            if i["from"] is not np.nan and i["from"] is not float or type(i["from"]) is not None \
                    or i["from"] != "" or i["from"] != " ":
                bank_cell_from = i["from"]
                try:
                    if re.search("Счет", bank_cell_from, flags=0):
                        bank_account_from = "".join(str(item) for item in bank_cell_from[-4:])
                        result_from = re.sub(r'\b\d{20}\b', f"**{bank_account_from}", bank_cell_from)
                        i["from"] = result_from
                    else:
                        numbers = "".join(str(item) for item in bank_cell_from[-16:])
                        result_from = re.sub(r'\b\d{16}\b', get_mask_card_number(numbers), bank_cell_from)
                        i["from"] = result_from
                except Exception as ex:
                    print("Ошибка from")
                    logger.error(f"{i["id"]} Ошибка {ex}. Продолжаем")
                    continue
            else:
                i["from"] = "-"
        if i.get("to"):
            if type(i.get("to")) is not np.nan and i.get("to") is not float or i.get("to") != "" \
                    or i.get("to") != " ":
                bank_cell_to = i["to"]
                try:
                    if re.search("Счет", bank_cell_to, flags=0):
                        bank_account_to = "".join(str(item) for item in bank_cell_to[-4:])
                        result_to = re.sub(r'\b\d{20}\b', f"**{bank_account_to}", bank_cell_to)
                        i["to"] = result_to
                    else:
                        numbers = "".join(str(item) for item in bank_cell_to[-16:])
                        result_to = re.sub(r'\b\d{16}\b', get_mask_card_number(numbers), bank_cell_to)
                        i["to"] = result_to
                except Exception as ex:
                    print("Ошибка to")
                    logger.error(f"Ошибка {ex}. Продолжаем")
                    continue
            else:
                i["to"] = "-"
    logger.info("Сокрытие номеров карт и счетов выполнено через модуль masks")

    answer_by_date = input(  # Упорядочивание по дате
        "Упорядочить транзакции по дате?(да - упорядочить, иное - нет) ->: ").lower()
    if answer_by_date == "да" or answer_by_date == "lf":
        answer_vector_by_date = input("Упорядочить по дате по возрастанию/убыванию? ->: ").lower()
        if answer_vector_by_date == "убыванию" or answer_vector_by_date == "e,sdfyb.":
            reverse_parametr = True
            print("Упорядочиваем по дате по убыванию")
            logger.info("Упорядочиваем по дате по убыванию")
        else:
            reverse_parametr = False
            print("Упорядочиваем по дате по возрастанию")
        transactions_by_status = sorted(transactions_by_status, key=lambda z: z['date'], reverse=reverse_parametr)
        logger.info("Упорядочили по дате по возрастанию")
    else:
        logger.info("Выбор пользователя - без упорядочивания по дате.")

    for i in transactions_by_status:  # Преобразование даты в заданный формат
        full_date_time = i.get("date", "")
        correct_date = get_date(full_date_time)
        i["date"] = correct_date
    logger.info("Выполнено преобразование даты в заданный формат")

    # Фильтрация рублевых транзакций - да/нет
    answer_filtered_rub = input("Выводить только рублевые транзакции? (да - выводить, иное - нет) ->: ").lower()
    if answer_filtered_rub == "lf" or answer_filtered_rub == "да": choice["currency_code"] = "RUB"
    logger.info(f"Выбор пользователя по выводу только рублевых транзакций {answer_filtered_rub}")

    # Фильтрация транзакций по типу операций
    answer_description = input("Произвести подсчёт транзакций по типу операции?\n"
                               "(да - фильтровать, иное -нет) ->: ").lower()
    if answer_description == "lf" or answer_filtered_rub == "да":
        logger.info(f"Выбор пользователя фильтрации по типу операции {answer_description}")
        number_choice = input(f"Введите номер типа операции по которому необходимо выполнить фильтрацию.\n"
                              f"Доступные типы операций для фильтрации:\n1 -{description_type[0]}"
                              f"\n2 -{description_type[1]}\n3 -{description_type[2]}\n4 -{description_type[3]}"
                              f"\n5 -{description_type[4]}\n ->: ").lower()
        n = 0
        while number_choice not in list_input:
            n += 1
            if n <= 2:
                number_choice = input(f"Выбор некорректен, попробуйте ещё раз ввести доступный тип операции для"
                                      f" фильтрации:\n1 -{description_type[0]}\n2 -{description_type[1]}"
                                      f"\n3 -{description_type[2]}\n4 -{description_type[3]}"
                                      f"\n5 -{description_type[4]}\n ->: ").lower()
                logger.info(f"Повторный выбор пользователя {number_choice}")
            else:
                number_choice = list_status[0]
                print(f'По умолчанию выбран статус {number_choice}')
                logger.info(f"По умолчанию выбран статус {number_choice}.")
        if number_choice == "1": choice["description"] = description_type[0]
        if number_choice == "2": choice["description"] = description_type[1]
        if number_choice == "3": choice["description"] = description_type[2]
        if number_choice == "4": choice["description"] = description_type[3]
        if number_choice == "5": choice["description"] = description_type[4]
        final_countdown, count_category = final_calculation(transactions_by_status, choice)
        logger.info("Данные из final_calculation возвращены")
        for i in count_category:
            x = count_category[i]
        print(f"\nРаспечатываю итоговый список транзакций:\n\nВсего банковских операций в выборке: {x}")
        for i in final_countdown:
            if i.get("description") == "Открытие вклада" and i.get("from") is np.nan or i.get("from") == "":
                i["from"] = ""
            else:
                i["from"] = str(i["from"]) + " -> "
            print(f"\n{i["date"]} {i["description"]}\n{i["from"]}{i["to"]}\n{i["amount"]} "
                  f"{i["currency_name"]}")
            logger.info("Программа выполнена через final_calculation")
    else:
        print(f"\nРаспечатываю итоговый список транзакций:\n\nВсего банковских операций в выборке: "
              f"{len(transactions_by_status)}")
        for i in transactions_by_status:
            if i.get("description") == "Открытие вклада" and i.get("from") is np.nan or i.get("from") is None \
                    or i.get("from") == "-" or i.get("from") == "":
                i["from"] = ""
            else:
                i["from"] = str(i.get("from")) + " -> "
            print(f"\n{i["date"]} {i["description"]}\n{i["from"]}{i["to"]}\n{i["amount"]} \
                  {i["currency_name"]}")
            logger.info("Программа выполнена по более простому сценарию")


if __name__ == '__main__':
    main()
