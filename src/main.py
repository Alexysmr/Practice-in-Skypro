import pandas as pd

from src.reports import choice_options, spending_by_category
from src.services import searche_line, simple_search
from src.utils import read_transactions_data, the_beginning_of_the_event
from src.views import filtering_transactions

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

file_name = "operations_corr_date.xlsx"

data_df, data_list_dict = read_transactions_data(file_name)
current_datetime, period = the_beginning_of_the_event()
print(filtering_transactions(data_df, current_datetime, period))
data_df = data_df.drop("number_of_week", axis=1)
transactions = data_df
sign = searche_line(data_df)
print(simple_search(sign, data_list_dict))
category, date = choice_options(data_df)
print(spending_by_category(transactions, category, date))
