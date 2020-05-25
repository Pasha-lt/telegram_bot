from random import choice
from emoji import emojize
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_user_emo(user_data):
    """
    Функция проверяет есть ли закрепленный за пользователем смайлик, если нет то создает его.
    :param user_data: - данные о пользователи.
    :return: смайлик закрепленый за пользователем.
    """
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def get_keyboard():
    """
    :return: возвращаем нашу клавиатуру.
    """
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Прислать офис', 'Сменить аватарку'], [contact_button, location_button]],
                                      resize_keyboard=True)
    return my_keyboard