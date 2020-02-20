import dbworker
from aiogram import Bot, Dispatcher
from os import environ

admin_list = [418609567]

bot = Bot(token=environ.get("schedule_bot"), parse_mode="Markdown")
dp = Dispatcher(bot)
db = dbworker.Database()
