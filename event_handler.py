from config import db, bot
from aiogram.utils.markdown import *
import keyboards as kb

"""Система событий."""

chat_id = -1001482242520


async def new_user(msg):
    # user_faculty = db.get_info(user_id=msg.message.chat.id, column='user_faculty')
    # user_course = db.get_info(user_id=msg.message.chat.id, column='user_course')
    # user_group = db.get_info(user_id=msg.message.chat.id, column='user_group')
    db_answer = db.get_person(user_id=msg.from_user.id)
    user_faculty = db_answer['user_faculty']
    user_course = db_answer['user_course']
    user_group = db_answer['user_group']
    user_count = db.execute(query="SELECT count(distinct user_id) FROM users;")
    answer_message = f"{bold('Новый пользователь')}\n\n" \
                     f"Имя: {bold(msg.from_user.first_name)}/@{bold(msg.from_user.username)}\n" \
                     f"Факультет: {bold(user_faculty)}\n" \
                     f"Курс: {bold(user_course)}\n" \
                     f"Группа: {bold(user_group)}\n" \
                     f"Всего пользователей в базе: {bold(user_count)}"
    await bot.send_message(chat_id=chat_id,
                           text=answer_message,
                           reply_markup=kb.es_open_user(msg.from_user.id))


async def deleted_user(msg):
    await bot.send_message(chat_id=chat_id,
                           text=f"{bold('Пользователь удалился')}\n\n"
                                f"Имя: {bold(msg.from_user.first_name)}/@{bold(msg.from_user.username)}\n",
                           parse_mode="Markdown")


async def new_error(error_name, msg):
    await bot.send_message(chat_id=chat_id,
                           text=f"*Произошла ошибка\n\n"
                                f"Пользователь {msg.from_user.first_name}/@{msg.from_user.username} поймал ошибку:\n"
                                f"{b(error_name)}",
                           reply_markup=kb.es_open_user(msg.from_user.id))

async def new_admin(msg):
    await bot.send_message(chat_id=chat_id,
                    text=f"{b('Новый администратор')}\n\n"
         f"Пользователь {msg.from_user.first_name}/@{msg.from_user.username} стал администратором."),
         reply_markup=kb.es_open_user(msg.from_user.id)



def changed_personal_info(msg, setting, original_state, final_state):
    # answer_message = ""
    # answer_message = f"Пользователь @{msg.from_user.username} сменил {setting}:\n*{original_state}* ⇒ *{final_state}*"
    # bot.send_message(chat_id=chat_id,
    #                  text=answer_message,
    #                  parse_mode='Markdown')
    pass
