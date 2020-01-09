from config import bot
import logging

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('ScheduleBot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def add_error_to_log(user, error):
    bot.send_message(chat_id=-1001482242520, text=f"Пользователь *{user}* - Произошла ошибка:\n{error}")


def get_error_name(error):
    pass
