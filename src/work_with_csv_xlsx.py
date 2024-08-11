import logging
import os
import os.path
from pathlib import Path

import pandas as pd

main_path = Path(__file__).resolve().parents[1]

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(f'{main_path}/logs/csv_xlsx.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(funcName)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

logger.info(f'Родительская директория: {main_path}')


def reading_csv(file_name_csv: str) -> str:
    """Функция чтения CSV-файла"""
    logger.info('Старт функции чтения CSV')
    if file_name_csv != '':
        file_csv = os.path.join(main_path, "data", file_name_csv)
        logger.info(f'путь к файлу: {file_csv}')
    else:
        logger.info('Ошибка: Имя файла данных отсутствует')
        print('Работа функции завершена с ошибкой: Имя файла данных отсутствует')
        return 'Работа функции завершена с ошибкой: Имя файла данных отсутствует'
    if os.path.exists(file_csv) and os.stat(file_csv).st_size != 0:
        try:
            reader_csv = pd.read_csv(file_csv, delimiter=';')
            logger.info(f'Чтение {file_name_csv}')
            dimension_csv = reader_csv.shape
            logger.info(f'Размерность файла {file_name_csv} {dimension_csv}')
            print(f'Размерность данных в файле {file_name_csv} (стр/колон): {dimension_csv}')
            print(reader_csv.head(), '\nРабота функции завершена.\n')
            logger.info('Вывод на печать первых 5-ти строк файла CSV. Coda.')
        except Exception as ex:
            logger.error(f'Ошибка: {ex}')
            print(f'Работа функции завершена с ошибкой: {ex}')
            return f'Работа функции завершена с ошибкой: {ex}'
    else:
        logger.info('Ошибка: Файл не найден или пуст.')
        print('Работа функции завершена с ошибкой: Файл не найден или пуст.')
        return 'Работа функции завершена с ошибкой: Файл не найден или пуст.'
    return 'Работа функции завершена.'  # Пусть возвращает - для теста, все равно возвращается None.


def reading_xlsx(file_name_xlsx: str) -> str:
    """Функция чтения XLSX-файла"""
    logger.info('Старт функции чтения файла XLSX')
    if file_name_xlsx != '':
        file_xlsx = os.path.join(main_path, "data", file_name_xlsx)
        logger.info(f'Путь к файлу: {file_xlsx}')
    else:
        logger.info('Ошибка: Имя файла данных отсутствует')
        print('Работа функции завершена с ошибкой: Имя файла данных отсутствует')
        return 'Работа функции завершена с ошибкой: Имя файла данных отсутствует'
    if os.path.exists(file_xlsx) and os.stat(file_xlsx).st_size != 0:
        try:
            reader_xlsx = pd.read_excel(file_xlsx)
            logger.info(f'Чтение {file_name_xlsx}')
            dimension_xlsx = reader_xlsx.shape
            logger.info(f'Размерность файла {file_name_xlsx} {dimension_xlsx}')
            print(f'Размерность данных в файле {file_name_xlsx} (стр/колон): {dimension_xlsx}')
            print(reader_xlsx.head(), '\nРабота функции завершена.\n')
            logger.info(f'Вывод на печать первых 5-ти строк файла {file_name_xlsx}. Coda.')
        except Exception as ex:
            logger.error(f'Ошибка: {ex}')
            print(f'Работа функции завершена с ошибкой: {ex}')
            return f'Работа функции завершена с ошибкой: {ex}'
    else:
        logger.info('Ошибка: Файл не найден или пуст.')
        print('Работа функции завершена с ошибкой: Файл не найден или пуст.')
        return 'Работа функции завершена с ошибкой: Файл не найден или пуст.'
    return 'Работа функции завершена.'  # Пусть возвращается для теста, все равно возвращается None.
