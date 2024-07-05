from src.masks import get_mask_account, get_mask_card_number

numbers = input("Введите номер карты (16 цифр): ")
bank_account = input("Введите номер счёта (6 цифр): ")

print(get_mask_card_number(numbers))
print(get_mask_account(bank_account))
