from datetime import datetime
from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "chat_id": chat_id
        }
        db.users.insert_one(user)
    return user


def save_currency(db, user_id, default_currency):
    user = db.users.find_one({"user_id": user_id})
    if default_currency not in user.get('default_exch_currency'):
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'default_exch_currency': [default_currency]}}
        )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'default_exch_currency': default_currency}}
        )
