# Импорт сторонних библиотек
import dask.dataframe as dd

# Импорт встроенных библиотек
import math

# Импорт пользовательских библиотек
from ..project.project import ResearchProject
from .preprocess import find_number, find_year, correct_month, month_to_int, check_days_in_month


class Query:
    def __init__(self, project: ResearchProject):
        self.project = project

    def raw_response(self, token: str):
        # Переменные
        df = self.project.df

        # Вычисление вхождений токена в корпус
        result = df.loc[df['token'].str.contains(token)].compute()

        # Парсинг данных
        # Парсинг номера выпуска и года издания выпуска
        result['newspaper_issue'] = result['filename'].apply(
            lambda x: find_number(x))
        result['newspaper_year'] = result['filename'].apply(
            lambda x: find_year(x))

        # Изменение данных
        # Создание столбца с числом вхождений каждого токена в корпус
        result['token_'] = [1 for _ in range(len(result))]

        # Корректировка месяца выхода газеты
        result['newspaper_month'] = result['newspaper_month'].apply(
            lambda x: month_to_int(correct_month(x)))
        result[['newspaper_month']] = result[[
            'newspaper_month']].fillna(value=0)
        result['newspaper_month'] = result['newspaper_month'].apply(math.floor)

        # Вывод данных
        return result

    def response(self, token: str):
        # Ввод данных
        result = self.raw_response(token)

        # Фильтрация данных
        date_df = result.loc[(result.newspaper_month != 0) | (result.newspaper_day != 0) | (
            result.newspaper_month <= 12) | (result.newspaper_day <= 31)]

        # Создание аттрибута "issue_date" с датой выпуска газеты
        # Проверка количества дней на соответствие количеству дней в определенном месяце
        date_df['newspaper_day_checked'] = date_df.apply(
            lambda x: check_days_in_month(x['newspaper_day'], x['newspaper_month']), axis=1)
        date_df = date_df[date_df['newspaper_day_checked'] != 0]

        # Преобразование строки в объект datetime
        date_df['issue_date'] = dd.to_datetime(date_df.apply(
            lambda x: f"{x['newspaper_month']}/{x['newspaper_day_checked']}/{x['newspaper_year']}", axis=1)).compute()

        # Вывод данных
        # Удаление лишних аттрибутов
        date_df = date_df.drop(columns=['newspaper_day_checked'])

        return date_df
