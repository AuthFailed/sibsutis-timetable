from config import db, bot
import keyboards as kb

"""Система событий."""

chat_id = -1001482242520


async def new_user(username, user_id):
    db_answer = db.get_person(user_id=msg.from_user.id)
    user_faculty = db_answer["faculty"]
    user_course = db_answer["course"]
    user_group = db_answer["group"]
    user_reg_date = db_answer["registration_date"]

    answer_message = (
        f"*Новый пользователь*\n\n"
        f"Пользователь: @{username}\n"
        f"Факультет: *{user_faculty}*\n"
        f"Курс: *{user_course}*\n"
        f"Группа: *{user_group}*\n"
        f"Дата регистрации: *{user_reg_date}*"
    )
    await bot.send_message(
        chat_id=chat_id,
        text=answer_message,
        reply_markup=await kb.es_open_user(user_id),
    )


async def request_schedule(username, user_info, selected_day):
    user_id = user_info["user_id"]
    user_faculty = user_info["faculty"]
    user_course = user_info["course"]
    user_group = user_info["group"]

    answer_message = (
        f"*Запрос расписания*\n\n"
        f"Пользователь: @{username}\n"
        f"Факультет: *{user_faculty}*\n"
        f"Курс: *{user_course}*\n"
        f"Группа: *{user_group}*\n"
        f"День: *{selected_day}*"
    )
    await bot.send_message(
        chat_id=chat_id,
        text=answer_message,
        reply_markup=await kb.es_open_user(user_id),
    )


async def deleted_user(username, user_id, db_answer):
    faculty = db_answer['faculty']
    course = db_answer['course']
    group = db_answer['group']
    answer_message = f"*Пользователь удалился*\n\n" f"Пользователь: @{username}\n" f"Факультет: {faculty}\n" f"Курс: {course}\n" f"Группа: {group}"
    await bot.send_message(
        chat_id=chat_id, text=answer_message, parse_mode="Markdown",
    )


async def new_error(error_name):
    await bot.send_message(
        chat_id=chat_id, text=f"*Произошла ошибка\n\n" f"Ошибка: *{error_name}*"
    )


async def new_admin(username, user_id):
    await bot.send_message(
        chat_id=chat_id,
        text=f"*Новый администратор*\n\n"
        f"Пользователь @{username} стал администратором.",
        reply_markup=await kb.es_open_user(user_id),
    )


async def try_to_get_admin_mode(username, user_id):
    await bot.send_message(
        chat_id=chat_id,
        text=f"*Попытка получить админку*\n\n"
        f"Пользователь @{username} пытался получить админку.",
        reply_markup=await kb.es_open_user(user_id),
    )


async def run_in_group(username, user_id):
    await bot.send_message(
        chat_id=chat_id,
        text=f"*Попытка использовать бота в группе*\n\n"
        f"Пользователь @{username} попытался использовать бота в публичном чате.",
        reply_markup=await kb.es_open_user(user_id),
    )


async def user_change_group(
    username,
    user_id,
    first_state={"faculty": "", "course": "", "group": ""},
    last_state={"faculty": "", "course": "", "group": ""},
):
    await bot.send_message(
        chat_id=chat_id,
        text=f"*Пользователь изменил личную информацию*\n\n"
        f"Пользователь: @{username}\n"
        f"Состояние:\n"
        f"*\t\tФакультет: {first_state['faculty']}*   ->   *{last_state['faculty']}*\n"
        f"*\t\tКурс:            {first_state['course']}*   ->   *{last_state['course']}*\n"
        f"*\t\tГруппа:       {first_state['group']}*   ->   *{last_state['group']}*",
        reply_markup=await kb.es_open_user(user_id),
    )


def changed_personal_info(msg, setting, original_state, final_state):
    # answer_message = ""
    # answer_message = f"Пользователь @{msg.from_user.username} сменил {setting}:\n*{original_state}* ⇒ *{final_state}*"
    # bot.send_message(chat_id=chat_id,
    #                  text=answer_message,
    #                  parse_mode='Markdown')
    pass
