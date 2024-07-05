from src.widget import mask_account_card, mask_account, get_date

name_numbers = input("Введите название и номер карты в формате Visa Classic XXXXXX...(16 цифр):\n")
bank_account = f"Счёт {input("Введите номер счёта: ")}"

print(*mask_account_card(name_numbers))
print(mask_account(bank_account))

get_date(full_date_time="2024-03-11T02:26:18.671407")
