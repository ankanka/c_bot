from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
import requests

def c_keyboard(list1, list2, button = ['Справка']):
    return ReplyKeyboardMarkup([list1, list2, button])