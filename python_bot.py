import logging
from telegram.ext import MessageHandler, Filters, RegexHandler, Updater, CommandHandler

from handlers import *
import settings



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



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