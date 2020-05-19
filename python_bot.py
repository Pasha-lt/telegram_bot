from telegram.ext import Updater, CommandHandler
import logging
from telegram.ext import MessageHandler, Filters
from googletrans import Translator
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update):
    """
        Функция которая вызывается когда жмем на кнопку старт
    :param bot:
    :param update:
    :return:
    """
    logging.info(update.message)
    logging.info('Вызван start')
    update.message.reply_text('Пиши на русском я буду переводить на английский ...')


def talk_to_me(bot, update):
    """
    Функция которая обрабатывает текстовые сообщения, переводит их с русского на английский язык.
    :param bot:
    :param update:
    :return:
    """
    user_text = update.message.text
    logging.info(user_text)
    translator = Translator()
    user_text = translator.translate(user_text, src='ru', dest='en').text
    update.message.reply_text('eng=> ' + user_text)


def main():
    """
    Команды инициализации и запуска бота
    :return:
    """
    mybot = Updater(settings.your_token)
    db = mybot.dispatcher # специальный обьект который принимает входящие и расскидываем их по командам
    db.add_handler(CommandHandler('start', greet_user))
    db.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('Блог запускается')  # При запуске бота нам будет писать в нашем bot.log
    mybot.start_polling()  # заставляем регуляно ходить на платформу телеграмм и проверять наличие сообщений.
    mybot.idle()  # Бот будет работать пока мы его принудительно не остановим.


if __name__ == '__main__':
    main()