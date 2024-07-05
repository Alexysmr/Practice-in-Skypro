from src.widget import get_date, mask_account, mask_account_card

name_numbers = input("Введите название и номер карты в формате 'Visa Classic XXXXXX...(16 цифр)':\n")
bank_account = f"Счёт {input("Введите номер счёта в формате 'Счет ХХХХ...(номер)':\n")}"

print(*mask_account_card(name_numbers))
print(mask_account(bank_account))

print(get_date(full_date_time="2024-03-11T02:26:18.671407"))
