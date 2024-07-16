from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, mask_account, get_date
from src.masks import get_mask_card_number, get_mask_account

clients = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
           {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
           {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
           {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

numbers = input("Введите номер карты (16 цифр): ")
print(get_mask_card_number(numbers))

bank_account = input("Введите номер счёта (20 цифр): ")
print(get_mask_account(bank_account))

name_numbers = input("Введите название и номер карты в формате 'Visa Classic XXXXXX...(16 цифр)':\n")
print(*mask_account_card(name_numbers), sep=" ")

bank_user_account = f"Счёт {input("Введите номер счёта в формате 'Счет ХХХХ...(номер 20 цифр)':\n")}"
print(mask_account(bank_user_account))

print(get_date(full_date_time="2024-03-11T02:26:18.671407"))

print(filter_by_state(clients))
print(filter_by_state(clients, state='CANCELED'))
print(sort_by_date(clients))
