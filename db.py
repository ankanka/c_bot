from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]

# data = {
#     "username": "Грэм Чепмен",
#     "chat_id": 12345,
#     "messages": [
#         {"id": 1, "text": "Стой! Как тебя зовут?"},
#         {"id": 2, "text": "Перед тобой Артур, король бриттов."}
#     ]
# }

# создать коллекцию testcollections и сложить туда данные
#db.testcollection.insert_one(data) 


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "chat_id": chat_id
        }
        db.users.insert_one(user)
    return user