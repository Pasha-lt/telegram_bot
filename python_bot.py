from telegram.ext import Updater, CommandHandler
import logging
from glob import glob
from random import choice

from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import MessageHandler, Filters, RegexHandler
from googletrans import Translator
from emoji import emojize

import settings



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


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

def main():
    """
    Команды инициализации и запуска бота
    """
    mybot = Updater(settings.TOKEN)
    db = mybot.dispatcher # специальный обьект который принимает входящие и расскидываем их по командам
    db.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    db.add_handler(CommandHandler('office', send_office_picture, pass_user_data=True))
    db.add_handler(RegexHandler('^(Прислать офис)$', send_office_picture, pass_user_data=True))
    db.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    db.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    db.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    db.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    logging.info('Блог запускается')  # При запуске бота нам будет писать в нашем bot.log
    mybot.start_polling()  # заставляем регуляно ходить на платформу телеграмм и проверять наличие сообщений.
    mybot.idle()  # Бот будет работать пока мы его принудительно не остановим.


if __name__ == '__main__':
    main()