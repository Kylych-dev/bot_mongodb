from pymongo import MongoClient
from datetime import datetime, timedelta
from calendar import monthrange

from .settings import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION


# Подключение к MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]



def aggregate_data(dt_from_str, dt_upto_str, group_type):
    # Преобразование строк в объекты datetime
    dt_from = datetime.fromisoformat(dt_from_str)
    dt_upto = datetime.fromisoformat(dt_upto_str)

    # Определение условий агрегации в зависимости от типа группировки
    if group_type == 'hour':
        group_id = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
            'day': {'$dayOfMonth': '$dt'},
            'hour': {'$hour': '$dt'}
        }
        date_format = '%Y-%m-%dT%H:00:00'
        delta = timedelta(hours=1)
    elif group_type == 'day':
        group_id = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'},
            'day': {'$dayOfMonth': '$dt'}
        }
        date_format = '%Y-%m-%dT00:00:00'
        delta = timedelta(days=1)
    elif group_type == 'month':
        group_id = {
            'year': {'$year': '$dt'},
            'month': {'$month': '$dt'}
        }

        date_format = '%Y-%m-01T00:00:00'
        _, num_days = monthrange(dt_from.year, dt_from.month)  # Определение количества дней в месяце
        delta = timedelta(days=num_days)


    # Подготовка условий для запроса агрегации
    pipeline = [
        {'$match': {'dt': {'$gte': dt_from, '$lte': dt_upto}}},
        {'$group': {'_id': group_id, 'total_value': {'$sum': '$value'}}},
        {'$project': {
            '_id': 0,
            'date': {
                '$dateToString': {
                    'format': date_format,
                    'date': {
                        '$dateFromParts': {
                            'year': '$_id.year',
                            'month': '$_id.month',
                            'day': '$_id.day' if 'day' in group_id else 1,
                            'hour': '$_id.hour' if 'hour' in group_id else 0
                        }
                    }
                }
            },
            'total_value': 1
        }}
    ]

    # Выполнение запроса агрегации
    result = collection.aggregate(pipeline)

    # Создание полного списка дат в диапазоне с шагом в один день (или час)
    current_date = dt_from
    full_dates = []



    while current_date <= dt_upto:
        formatted_date = current_date.strftime(date_format)
        if formatted_date not in full_dates:
            full_dates.append(formatted_date)
        current_date += delta



    # while current_date <= dt_upto:
    #     full_dates.append(current_date.strftime(date_format))
    #     current_date += delta

    # Формирование выходного JSON
    result_dict = {doc['date']: doc['total_value'] for doc in result}
    dataset = [result_dict.get(date, 0) for date in full_dates]
    labels = full_dates

    output_json = {
        "dataset": dataset,
        "labels": labels
    }

    return output_json


'''

# Пример использования
dt_from_str = '2022-02-01T00:00:00'
dt_upto_str = '2022-02-02T00:00:00'
group_type = 'month'  # 'hour', 'day', или 'month'

output = aggregate_data(dt_from_str, dt_upto_str, group_type)
print(output)


2022-10-01T00:00:00",
   "dt_upto": "2022-11-30T23:59:00

'''