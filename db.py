from pymongo import MongoClient
import settings
#from c_scenario import set_exch_currency

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]

# data = {
#     "username": " Чепмен",
#     "chat_id": 12345,
#     "messages": [
#         {"id": 1, "text": "! Как тебя зовут?"},
#         {"id": 2, "text": "Перед тобой Артур, король бриттов."}
#     ]
# }

# #создать коллекцию testcollections и сложить туда данные
# db.testcollection.insert_one(data1)


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "chat_id": chat_id,
            "default_exch_currency": set_exch_currency()
        }
        db.users.insert_one(user)
    return user
