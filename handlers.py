from glob import glob
import logging
from random import choice

from googletrans import Translator
from utils import get_keyboard, get_user_emo


def greet_user(bot, update, user_data):
    """
    Функция которая вызывается когда жмем на кнопку старт
    :param bot:
    :param update:
    :return:
    """
    emo = get_user_emo(user_data)
    logging.info(update.message)
    text = f'Привет {emo}!\nХочеш рандомную фотку офиса жми /office или пиши на русском, а я буду переводить на английский ...'
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    """
    Функция которая обрабатывает текстовые сообщения, переводит их с русского на английский язык.
    :param bot:
    :param update:
    :return:
    """
    emo = get_user_emo(user_data)
    user_text = update.message.text
    logging.info(user_text)
    translator = Translator()
    user_text = translator.translate(user_text, src='ru', dest='en').text
    update.message.reply_text(f'{emo}eng=> ' + user_text, reply_markup=get_keyboard())


def send_office_picture(bot, update, user_data):
    """
    Функия которая будет срабатывать когда пользователь будет нажимать хендлер 'office' и выдавать ему
    рандомное изображение из нашей папки.
    :param bot:
    :param update:
    :return:
    """
    logging.info(update.message)
    office_list = glob('images/*office*.jp*g')
    office_pic = choice(office_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(office_pic, 'rb'), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:  # Если у пользователя есть аватарка мы ее удаляем
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(f'Готово: {emo}', reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    """
    обработчик контакта
    :param bot:
    :param message:
    :param user_data:
    :return:
    """
    logging.info(update.message.contact)
    update.message.reply_text(f'Готово: {get_user_emo(user_data)}', reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    """
    обработчик контакта
    :param bot:
    :param message:
    :param user_data:
    :return:
    """
    logging.info(update.message.location)
    update.message.reply_text(f'Готово: {get_user_emo(user_data)}', reply_markup=get_keyboard())

