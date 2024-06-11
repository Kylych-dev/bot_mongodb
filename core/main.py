from pymongo import MongoClient
from datetime import datetime
from decouple import config
from settings import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION

client = MongoClient(MONGO_HOST, MONGO_PORT)

db = client[MONGO_DB]

collection = db[MONGO_COLLECTION]

# res = collection.insert_one({'name': 'John', 'age': 25})
# user = {'id': 2, 'name': 'John', 'age': 25}
# user = collection.insert_one(user).inserted_id

# res = collection.find_one({'name': 'John'})

#
# user = {'_id': 2, 'name': 'Frank', 'age': 30}
# user = collection.insert_one(user).inserted_id
#
# print(user)

# document = collection.find()

# document = collection.find_one()
# print(document)

# for num, doc in enumerate(document):
#     print(f'{num} ---> {doc}')

# Пример критерия поиска: документы с датой '2022-01-02T03:19:00.000+00:00'

# target_date = datetime.strptime('2022-05-02T03:19:00.000+00:00', '%Y-%m-%dT%H:%M:%S.%f%z')
#
# # Использование find_one() для получения одного документа по критерию
# document = collection.find_one({'dt': target_date})
#
# # Печать найденного документа
# print(document)



date_format_db = '%Y-%m-%dT%H:%M:%S.%f%z'

# Преобразование строки в объект datetime
target_date = datetime.strptime('2022-01-02T01:42:00.000+00:00', date_format_db)

# Использование find_one() для получения одного документа по критерию
document = collection.find_one({'dt': target_date})

# Форматирование результата
if document:
    output_json = {
        "dataset": document['value'],
        "labels": document['dt'].strftime(date_format_db)
    }
else:
    output_json = {
        "dataset": None,
        "labels": None
    }

# Печать результата
print(output_json)


'''
"dataset": 5906586,
"labels": "2022-09-01T00:00:00", 
'''