from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from datetime import timedelta


def send_hello(context):
    context.bot.send_message(chat_id=203438658,
                             text='Привет!')
    #context.job.interval += 6
    # if context.job.job > 15:
    #     context.bot.send_message(chat_id=203438658, text='Пока!')
    #     context.job.schedule_removal()


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    subscribe_user(db, user)
    update.message.reply_text('Вы подписались')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы отписались')

# print(dir(context))
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bot_data', '_chat_data', '_dispatcher', '_user_data', 'args', 'async_args', 'async_kwargs', 'bot', 'bot_data', 'chat_data', 'dispatcher', 'error', 'from_error', 'from_job', 'from_update', 'job', 'job_queue', 'match', 'matches', 'update', 'update_queue', 'user_data']
# print(dir(context.job))
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_enabled', '_removed', 'callback', 'context', 'enabled', 'from_aps_job', 'job', 'job_queue', 'name', 'next_t', 'removed', 'run', 'schedule_removal']
# print(dir(context.job.job))
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__unicode__', '_get_run_times', '_jobstore_alias', '_modify', '_scheduler', 'args', 'coalesce', 'executor', 'func', 'func_ref', 'id', 'kwargs', 'max_instances', 'misfire_grace_time', 'modify', 'name', 'next_run_time', 'pause', 'pending', 'remove', 'reschedule', 'resume', 'trigger']
