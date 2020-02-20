from aiogram.types.inline_keyboard import *
from aiogram.types.reply_keyboard import *
from config import db, bot

InlBtn = InlineKeyboardButton


def main_menu():
    """Клавиатура для главного меню."""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    kb.row("Учёба", "Время пар")
    kb.row("Доп. Информация", "Настройки")

    return kb


def get_schedule_by_day():
    """Клавиатура для получения расписания."""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    kb.row("Сегодня", "Завтра", "Неделя")
    kb.row("◀️", "🚪", "👴", "❓")

    return kb


def schedule_menu_help():
    """Меню подсказок"""
    kb = InlineKeyboardMarkup()

    audience_help = InlBtn(text="🚪", callback_data="audience_help")
    teacher_help = InlBtn(text="👴", callback_data="teacher_help")

    kb.row(audience_help, teacher_help)
    return kb


def make_settings_keyboard_for_user(user_id):
    """Персональная клавиатура настроек пользователя."""

    kb = InlineKeyboardMarkup()
    user_status = db.get_person(user_id=user_id)["is_admin"]

    personal_settings = InlBtn(
        text="Персон. настройки", callback_data="personal_settings"
    )
    kb.add(personal_settings)

    if user_status:
        kb.add(InlBtn(text="🛡️ Админка 🛡️", callback_data="generate_admin_keyboard"))
    delete_me = InlBtn(text="🗑️ Удалить аккаунт 🗑️", callback_data="delete_me")

    kb.add(delete_me)
    return kb


def personal_settings_menu(user_id, faculty, course, group):
    """Меню персональных настроек."""
    kb = InlineKeyboardMarkup()
    kb.add(InlBtn(text="⚖️ Сменить факультет", callback_data="change_faculty"))
    kb.row(
        InlBtn(text="🏫 Сменить курс", callback_data="change_course"),
        InlBtn(text="👥 Сменить группу", callback_data="choose_group"),
    )
    kb.add(InlBtn(text="⚙  В параметры", callback_data="open_parameters_menu"))
    return kb


def faculty_menu():
    """Меню выбора факультета."""
    kb = InlineKeyboardMarkup()
    kb = Inli
    mts = InlBtn(text="МТС", callback_data="MTS_faculty")
    mrm = InlBtn(text="МРМ", callback_data="MRM_faculty")
    ivt = InlBtn(text="ИВТ", callback_data="IVT_faculty")
    gf = InlBtn(text="ГФ", callback_data="GF_faculty")
    aes = InlBtn(text="АЭС", callback_data="AES_faculty")

    kb.row(mts, mrm)
    kb.row(ivt, gf)
    kb.add(aes)
    return kb


def group_keyboard(user_id):
    """Меню выбора группы."""
    kb = InlineKeyboardMarkup()
    db_answer = db.get_person(user_id=user_id)
    faculty = db_answer["faculty"]
    course = db_answer["course"]
    if faculty == "МТС" and course == 1:
        kb.row(
            InlBtn(text="МО-95", callback_data="МО-95"),
            InlBtn(text="МО-96", callback_data="МО-96"),
            InlBtn(text="ММ-91", callback_data="ММ-91"),
        )
        kb.row(
            InlBtn(text="ММ-92", callback_data="ММ-92"),
            InlBtn(text="МП-98", callback_data="МП-98"),
        )
        kb.row(
            InlBtn(text="МИ-97", callback_data="МИ-97"),
            InlBtn(text="МГ-196", callback_data="МГ-196"),
        )
    elif faculty == "МТС" and course == 2:
        kb.row(
            InlBtn(text="МО-85", callback_data="МО-85"),
            InlBtn(text="МО-86", callback_data="МО-86"),
            InlBtn(text="МИ-87", callback_data="МИ-87"),
            InlBtn(text="ММП-81", callback_data="ММП-81"),
        )
        kb.row(
            InlBtn(text="МГ-186", callback_data="МГ-186"),
            InlBtn(text="МГ-187", callback_data="МГ-187"),
            InlBtn(text="ММП-82", callback_data="ММП-82"),
            InlBtn(text="МПП-88", callback_data="МПП-88"),
        )
    elif faculty == "МТС" and course == 3:
        kb.row(
            InlBtn(text="ММП-71", callback_data="ММП-71"),
            InlBtn(text="ММП-72", callback_data="ММП-72"),
            InlBtn(text="МО-75", callback_data="МО-75"),
            InlBtn(text="МПП-78", callback_data="МПП-78"),
            InlBtn(text="МИ-77", callback_data="МИ-77"),
        )
    elif faculty == "МТС" and course == 4:
        kb.row(
            InlBtn(text="МО-65", callback_data="МО-65"),
            InlBtn(text="МО-66", callback_data="МО-66"),
            InlBtn(text="МИ-67", callback_data="МИ-67"),
            InlBtn(text="ММП-61", callback_data="ММП-61"),
            InlBtn(text="МПП-68", callback_data="МПП-68"),
        )
    elif faculty == "МРМ" and course == 1:
        kb.row(
            InlBtn(text="РИ-91", callback_data="РИ-91"),
            InlBtn(text="РИ-92", callback_data="РИ-92"),
            InlBtn(text="РИ-93", callback_data="РИ-93"),
        )
        kb.row(
            InlBtn(text="РС-91", callback_data="РС-91"),
            InlBtn(text="РС-92", callback_data="РС-92"),
            InlBtn(text="РСК-91", callback_data="РСК-91"),
        )
        kb.row(
            InlBtn(text="РТ-91", callback_data="РТ-91"),
            InlBtn(text="РЦ-91", callback_data="РЦ-91"),
            InlBtn(text="РП-91", callback_data="РП-91"),
        )
    elif faculty == "МРМ" and course == 2:
        kb.row(
            InlBtn(text="РИ-87", callback_data="РИ-87"),
            InlBtn(text="РИ-88", callback_data="РИ-88"),
            InlBtn(text="РИ-89", callback_data="РИ-89"),
        )
        kb.row(
            InlBtn(text="РСК-812", callback_data="РСК-812"),
            InlBtn(text="РСК-811", callback_data="РСК-811"),
            InlBtn(text="МГ-185", callback_data="МГ-185"),
        )
        kb.row(
            InlBtn(text="РА-85", callback_data="РА-85"),
            InlBtn(text="РТ-84", callback_data="РТ-84"),
            InlBtn(text="РС-81", callback_data="РС-81"),
        )
        kb.row(
            InlBtn(text="РЦ-82", callback_data="РЦ-82"),
            InlBtn(text="РП-86", callback_data="РП-86"),
            InlBtn(text="МГ-189", callback_data="МГ-189"),
        )
    elif faculty == "МРМ" and course == 3:
        kb.row(
            InlBtn(text="РИ-77", callback_data="РИ-77"),
            InlBtn(text="РИ-78", callback_data="РИ-78"),
            InlBtn(text="РА-75", callback_data="РА-75"),
        )
        kb.row(
            InlBtn(text="РТ-74", callback_data="РТ-74"),
            InlBtn(text="РС-711", callback_data="РС-711"),
            InlBtn(text="РЦ-72", callback_data="РЦ-72"),
        )
        kb.row(
            InlBtn(text="РС-71", callback_data="РС-71"),
            InlBtn(text="РП-76", callback_data="РП-76"),
            InlBtn(text="РСК-711", callback_data="РСК-711"),
            InlBtn(text="РСК-712", callback_data="РСК-712"),
        )
    elif faculty == "МРМ" and course == 4:
        kb.row(
            InlBtn(text="РИ-67", callback_data="РИ-67"),
            InlBtn(text="РИ-68", callback_data="РИ-68"),
            InlBtn(text="РЦ-62", callback_data="РЦ-62"),
        )
        kb.row(
            InlBtn(text="РС-61", callback_data="РС-61"),
            InlBtn(text="РМ-63", callback_data="РМ-63"),
            InlBtn(text="РА-65", callback_data="РА-65"),
        )
        kb.row(
            InlBtn(text="РТ-64", callback_data="РТ-64"),
            InlBtn(text="РП-66", callback_data="РП-66"),
            InlBtn(text="РСК-611", callback_data="РСК-611"),
        )
    elif faculty == "ИВТ" and course == 1:
        kb.row(
            InlBtn(text="ИП-913", callback_data="ИП-913"),
            InlBtn(text="ИВ-923", callback_data="ИВ-923"),
            InlBtn(text="ИВ-922", callback_data="ИВ-922"),
            InlBtn(text="ИП-916", callback_data="ИП-916"),
        )
        kb.row(
            InlBtn(text="ИП-911", callback_data="ИП-911"),
            InlBtn(text="ИП-917", callback_data="ИП-917"),
            InlBtn(text="ИА-931", callback_data="ИА-931"),
            InlBtn(text="ИП-915", callback_data="ИП-915"),
        )
        kb.row(
            InlBtn(text="ИА-932", callback_data="ИА-932"),
            InlBtn(text="ИП-914", callback_data="ИП-914"),
            InlBtn(text="ИП-912", callback_data="ИП-912"),
            InlBtn(text="ИС-942", callback_data="ИС-942"),
        )
        kb.row(
            InlBtn(text="ИИ-961", callback_data="ИИ-961"),
            InlBtn(text="ИВ-921", callback_data="ИВ-921"),
            InlBtn(text="ИИ-962", callback_data="ИИ-962"),
            InlBtn(text="ИС-941", callback_data="ИС-941"),
        )
        kb.row(
            InlBtn(text="МГ-192", callback_data="МГ-192"),
            InlBtn(text="МГ-191", callback_data="МГ-191"),
        )
    elif faculty == "ИВТ" and course == 2:
        kb.row(
            InlBtn(text="ИП-811", callback_data="ИП-811"),
            InlBtn(text="ИА-832", callback_data="ИА-832"),
            InlBtn(text="ИП-814", callback_data="ИП-814"),
            InlBtn(text="ИВ-823", callback_data="ИВ-823"),
        )
        kb.row(
            InlBtn(text="ИП-816", callback_data="ИП-816"),
            InlBtn(text="ИА-831", callback_data="ИА-831"),
            InlBtn(text="ИП-815", callback_data="ИП-815"),
            InlBtn(text="ИП-813", callback_data="ИП-813"),
        )
        kb.row(
            InlBtn(text="МГ-182", callback_data="МГ-182"),
            InlBtn(text="МГ-181", callback_data="МГ-181"),
            InlBtn(text="ИВ-821", callback_data="ИВ-821"),
            InlBtn(text="ИИ-861", callback_data="ИИ-861"),
        )
        kb.row(
            InlBtn(text="ИС-842", callback_data="ИС-842"),
            InlBtn(text="ИМ-871", callback_data="ИМ-871"),
            InlBtn(text="ИП-812", callback_data="ИП-812"),
            InlBtn(text="ИВ-822", callback_data="ИВ-822"),
        )
        kb.row(
            InlBtn(text="ИС-841", callback_data="ИС-841"),
            InlBtn(text="ИИ-862", callback_data="ИИ-862"),
        )
    elif faculty == "ИВТ" and course == 3:
        kb.row(
            InlBtn(text="ИП-713", callback_data="ИП-713"),
            InlBtn(text="ИП-715", callback_data="ИП-715"),
            InlBtn(text="ИВ-722", callback_data="ИВ-722"),
        )
        kb.row(
            InlBtn(text="ИИ-761", callback_data="ИИ-761"),
            InlBtn(text="ИИ-762", callback_data="ИИ-762"),
            InlBtn(text="ИА-731", callback_data="ИА-731"),
        )
        kb.row(
            InlBtn(text="ИС-742", callback_data="ИС-742"),
            InlBtn(text="ИП-714", callback_data="ИП-714"),
            InlBtn(text="ИС-741", callback_data="ИС-741"),
        )
        kb.row(
            InlBtn(text="ИП-711", callback_data="ИП-711"),
            InlBtn(text="ИВ-721", callback_data="ИВ-721"),
            InlBtn(text="ИМ-771", callback_data="ИМ-771"),
        )
        kb.row(
            InlBtn(text="ИП-712", callback_data="ИП-712"),
            InlBtn(text="ИА-732", callback_data="ИА-732"),
            InlBtn(text="ИБ-751", callback_data="ИБ-751"),
        )
    elif faculty == "ИВТ" and course == 4:
        kb.row(
            InlBtn(text="ИИ-661", callback_data="ИИ-661"),
            InlBtn(text="ИП-612", callback_data="ИП-612"),
            InlBtn(text="ИП-615", callback_data="ИП-615"),
        )
        kb.row(
            InlBtn(text="ИВ-622", callback_data="ИВ-622"),
            InlBtn(text="ИИ-662", callback_data="ИИ-662"),
            InlBtn(text="ИП-614", callback_data="ИП-614"),
        )
        kb.row(
            InlBtn(text="ИС-641", callback_data="ИС-641"),
            InlBtn(text="ИС-641", callback_data="ИС-641"),
            InlBtn(text="ИП-613", callback_data="ИП-613"),
        )
        kb.row(
            InlBtn(text="ИП-611", callback_data="ИП-611"),
            InlBtn(text="ИМ-671", callback_data="ИМ-671"),
            InlBtn(text="ИА-631", callback_data="ИА-631"),
        )
    elif faculty == "ГФ" and course == 1:
        kb.row(
            InlBtn(text="ГР-91", callback_data="ГР-91"),
            InlBtn(text="ГР-92", callback_data="ГР-92"),
        )
    elif faculty == "ГФ" and course == 2:
        kb.row(
            InlBtn(text="ГР-81", callback_data="ГР-81"),
            InlBtn(text="ГР-82", callback_data="ГР-82"),
        )
    elif faculty == "ГФ" and course == 3:
        kb.row(
            InlBtn(text="ГР-71", callback_data="ГР-71"),
            InlBtn(text="ГР-72", callback_data="ГР-72"),
        )
    elif faculty == "ГФ" and course == 4:
        kb.row(
            InlBtn(text="ГР-61", callback_data="ГР-61"),
            InlBtn(text="ГР-62", callback_data="ГР-62"),
            InlBtn(text="ГР-63", callback_data="ГР-63"),
        )
    elif faculty == "АЭС" and course == 1:
        kb.row(
            InlBtn(text="АВ-912", callback_data="АВ-912"),
            InlBtn(text="АБ-95", callback_data="АБ-95"),
            InlBtn(text="АБ-98", callback_data="АБ-98"),
            InlBtn(text="АБ-97", callback_data="АБ-97"),
        )
        kb.row(
            InlBtn(text="АП-93", callback_data="АП-93"),
            InlBtn(text="АБ-96", callback_data="АБ-96"),
            InlBtn(text="АБ-94", callback_data="АБ-94"),
            InlBtn(text="АП-92", callback_data="АП-92"),
        )
        kb.row(
            InlBtn(text="АВ-911", callback_data="АВ-911"),
            InlBtn(text="АБ-99", callback_data="АБ-99"),
        )
    elif faculty == "АЭС" and course == 2:
        kb.row(
            InlBtn(text="АБ-87", callback_data="АБ-87"),
            InlBtn(text="АБ-86", callback_data="АБ-86"),
            InlBtn(text="АБ-88", callback_data="АБ-88"),
        )
        kb.row(
            InlBtn(text="АВ-81", callback_data="АВ-81"),
            InlBtn(text="АВ-82", callback_data="АВ-82"),
            InlBtn(text="АБ-89", callback_data="АБ-89"),
        )
        kb.row(
            InlBtn(text="АП-84", callback_data="АП-84"),
            InlBtn(text="АБ-85", callback_data="АБ-85"),
            InlBtn(text="АП-83", callback_data="АП-83"),
        )
    elif faculty == "АЭС" and course == 3:
        kb.row(
            InlBtn(text="АП-72", callback_data="АП-72"),
            InlBtn(text="АВ-712", callback_data="АВ-712"),
            InlBtn(text="АБ-751", callback_data="АБ-751"),
        )
        kb.row(
            InlBtn(text="АБ-76", callback_data="АБ-76"),
            InlBtn(text="АП-73", callback_data="АП-73"),
            InlBtn(text="АБ-75", callback_data="АБ-75"),
        )
        kb.row(
            InlBtn(text="АВ-711", callback_data="АВ-711"),
            InlBtn(text="АБ-74", callback_data="АБ-74"),
        )
    elif faculty == "АЭС" and course == 4:
        kb.row(
            InlBtn(text="А-63", callback_data="А-63"),
            InlBtn(text="А-64", callback_data="А-64"),
            InlBtn(text="АБ-65", callback_data="АБ-65"),
            InlBtn(text="АБ-66", callback_data="АБ-66"),
        )
        kb.row(
            InlBtn(text="АБ-67", callback_data="АБ-67"),
            InlBtn(text="АП-62", callback_data="АП-62"),
            InlBtn(text="АВ-611", callback_data="АВ-611"),
        )
    elif faculty == "АЭС" and course == 5:
        kb.row(
            InlBtn(text="АБ-55", callback_data="АБ-55"),
            InlBtn(text="АБ-56", callback_data="АБ-56"),
            InlBtn(text="АВ-51", callback_data="АВ-51"),
        )
    return kb


def course_keyboard(user_id):
    """Меню выбора курса."""
    faculty = db.get_info(user_id=user_id, column="faculty")
    kb = InlineKeyboardMarkup()

    first_course = InlBtn(text="1 курс", callback_data="set_1_course")
    second_course = InlBtn(text="2 курс", callback_data="set_2_course")
    third_course = InlBtn(text="3 курс", callback_data="set_3_course")
    fourth_course = InlBtn(text="4 курс", callback_data="set_4_course")

    kb.row(first_course, second_course)
    kb.row(third_course, fourth_course)
    if faculty == "АЭС":
        fifth_course = InlBtn(text="5 курс", callback_data="set_5_course")
        kb.row(fifth_course)
    return kb


def week_menu():
    """Меню расписания на неделю"""
    kb = InlineKeyboardMarkup()
    monday = InlBtn(text="Пн", callback_data="get_monday_schedule")
    tuesday = InlBtn(text="Вт", callback_data="get_tuesday_schedule")
    wednesday = InlBtn(text="Ср", callback_data="get_wednesday_schedule")
    thursday = InlBtn(text="Чт", callback_data="get_thursday_schedule")
    friday = InlBtn(text="Пт", callback_data="get_friday_schedule")
    saturday = InlBtn(text="Сб", callback_data="get_saturday_schedule")
    all_week = InlBtn(text="Вся неделя", callback_data="get_all_week")

    kb.row(monday, tuesday, wednesday, thursday, friday, saturday)
    kb.add(all_week)

    return kb


def lesson_time():
    """Меню обновления времени."""
    kb = InlineKeyboardMarkup()
    kb.add(InlBtn(text="🔄Обновить", callback_data="reload_time"))
    return kb


def additional_info():
    """Меню дополнительной информации."""
    kb = InlineKeyboardMarkup()
    kb.add(InlBtn(text="🏠 В меню", callback_data="to_main_menu"))
    return kb


def admin_menu():
    """Админ-меню."""
    kb = InlineKeyboardMarkup()

    statistic = InlBtn(text="📈 Статистика", callback_data="get_bot_statistic")
    edit_db = InlBtn(text="📙 Управление БД", callback_data="get_edit_db")
    execute_query = InlBtn(text="💡 Выполнить запрос", callback_data="execute_query")
    to_settings = InlBtn(text="Вернуться", callback_data="open_parameters_menu")

    kb.add(statistic, edit_db)
    kb.add(execute_query)
    kb.add(to_settings)
    return kb


def admin_statistic_menu():
    """Меню статистики [Админ-меню]."""
    kb = InlineKeyboardMarkup()

    users_count = InlBtn(text="📈 Кол-во юзеров", callback_data="adminmenu_users_count")
    schedule_updates = InlBtn(
        text="🆕 Обновления расписания", callback_data="adminmenu_schedule_updates"
    )
    return_to_adminmenu = InlBtn(
        text="Вернуться в админку", callback_data="generate_admin_keyboard"
    )
    kb.add(users_count, schedule_updates)
    kb.add(return_to_adminmenu)
    return kb


def admin_user_count_keyboard():
    """Меню подсчета пользователей."""
    kb = InlineKeyboardMarkup()
    reload = InlBtn(text="Обновить", callback_data="adminmenu_users_count")
    return_to_stats = InlBtn(
        text="Вернуться в админку", callback_data="get_bot_statistic"
    )
    kb.add(reload)
    kb.add(return_to_stats)
    return kb


def admin_edit_db_menu():
    """Управление базой данных [Админ-меню]."""
    kb = InlineKeyboardMarkup()

    delete_string = InlBtn(
        text="Удалить запись", callback_data="adminmenu_delete_string"
    )
    truncate_table = InlBtn(
        text="Очистить базу", callback_data="adminmenu_truncate_table"
    )
    return_to_adminmenu = InlBtn(
        text="Вернуться в админку", callback_data="generate_admin_keyboard"
    )
    kb.add(delete_string, truncate_table)
    kb.add(return_to_adminmenu)
    return kb


def delete_me_menu():
    """Меню самоудаления."""
    kb = InlineKeyboardMarkup()
    kb.row(
        InlBtn(text="Уверен, удалить", callback_data="delete_me_yes"),
        InlBtn(text="Я передумал(а)", callback_data="open_parameters_menu"),
    )
    return kb


async def es_open_user(user_id):
    """Меню управления пользователем."""
    user = await bot.get_chat(chat_id=user_id)
    kb = InlineKeyboardMarkup()
    show_profile = InlBtn(text="Открыть профиль", url=f"https://t.me/{user.username}")
    kb.add(show_profile)
    return kb
