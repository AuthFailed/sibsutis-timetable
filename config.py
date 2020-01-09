import dbworker
from aiogram import Bot, Dispatcher

token = '972207314:AAGN5yTBaB1zC-C9p40X5m0c_SbModyRJv8'
db_name = "dekm6lki1450k0"
db_username = "umwkhombqpcthb"
db_password = "d8c7ab8898b8ce89e938b0e913b43d71ab06baba2170e4557f51272991e97355"
db_host = "ec2-174-129-24-148.compute-1.amazonaws.com"

admin_list = [418609567]

bot = Bot(token=token, parse_mode='MarkdownV2')
dp = Dispatcher(bot)

db = dbworker.Database()
