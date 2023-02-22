# Импорт локальных модулей
import re
import math


def find_number(string: str):
    # Обработка данных
    number_s = re.findall(r'№\s{1}\d+', string)[0]
    number = math.floor(int(re.findall(r'\d+', number_s)[0]))

    # Вывод данных
    return number


def find_year(string: str):
    # Обработка данных
    number_s = re.findall(r'\d{4}', string)[0]
    number = math.floor(int(re.findall(r'\d+', number_s)[0]))

    # Вывод данных
    return number


def correct_month(month: str):
    # Импорт сторонних библиотек
    from Levenshtein import distance

    # Обработка данных
    if month != 'не определен':
        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        scores = [distance(month, m) for m in months]
        if min(scores) < 3:
            return months[scores.index(min(scores))]
        else:
            return 'не определен'
    else:
        return 'не определен'


def month_to_int(month: str):
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
        'не определен': 0
    }

    for k in months.keys():
        if month == k:
            return months[month]


def check_days_in_month(day: int, month: int):
    months = {
        0: 0,
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    if day > months[month]:
        return 0
    else:
        return day
