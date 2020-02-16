from config import db, bot
import keyboards as kb

"""Система событий."""

chat_id = -1001482242520


async def new_user(msg):
    db_answer = db.get_person(user_id=msg.from_user.id)
    user_faculty = db_answer['faculty']
    user_course = db_answer['course']
    user_group = db_answer['group']
    user_reg_date = db_answer['registration_date']
    answer_message = f"*Новый пользователь*\n\n" \
                     f"Пользователь: @*{msg.from_user.username}*\n" \
                     f"Факультет: *{user_faculty}*\n" \
                     f"Курс: *{user_course}*\n" \
                     f"Группа: *{user_group}*\n" \
                     f"Дата регистрации: *{user_reg_date}*"
    await bot.send_message(chat_id=chat_id,
                           text=answer_message,
                           reply_markup=await kb.es_open_user(msg.from_user.id))


async def deleted_user(msg):
    await bot.send_message(chat_id=chat_id,
                           text=f"*Пользователь удалился*\n\n"
                                f"Пользователь: @*{msg.from_user.username}*\n",
                           parse_mode="Markdown")


async def new_error(error_name):
    await bot.send_message(chat_id=chat_id,
                           text=f"*Произошла ошибка\n\n"
                                f"Ошибка: *{error_name}*")


async def new_admin(msg):
    await bot.send_message(chat_id=chat_id,
                           text=f"*Новый администратор*\n\n"
                                f"Пользователь @*{msg.from_user.username}* стал администратором.",
                           reply_markup=kb.es_open_user(msg.from_user.id))


def changed_personal_info(msg, setting, original_state, final_state):
    # answer_message = ""
    # answer_message = f"Пользователь @{msg.from_user.username} сменил {setting}:\n*{original_state}* ⇒ *{final_state}*"
    # bot.send_message(chat_id=chat_id,
    #                  text=answer_message,
    #                  parse_mode='Markdown')
    pass
