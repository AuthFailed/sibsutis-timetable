from aiogram.types.inline_keyboard import *
from config import db, bot

Btn = InlineKeyboardButton


def main_menu():
    """Клавиатура для главного меню.
    -Расписание
    -Время пар
    -Доп. информация
    -Параметры
    """
    kb = InlineKeyboardMarkup()

    get_schedule = Btn(text='📅 Расписание', callback_data='get_schedule')
    get_lesson_time = Btn(text='⌚ Время пар', callback_data='get_lesson_time')
    additional_info = Btn(text='ℹ️ Доп. информация',
                          callback_data='additional_info')
    settings = Btn(text='⚙  Параметры', callback_data='open_parameters_menu')

    kb.row(get_schedule, get_lesson_time)
    kb.add(additional_info)
    kb.add(settings)
    return kb


def get_schedule_by_day():
    """
    Клавиатура для получения расписания.
    -Сегодня
    -Завтра
    -Неделя
    -🏠 В меню
    """
    kb = InlineKeyboardMarkup()

    today = Btn(text='Сегодня', callback_data='get_today_schedule')
    tomorrow = Btn(text='Завтра', callback_data='get_tomorrow_schedule')
    week = Btn(text='Неделя', callback_data='get_week_schedule')
    to_menu = Btn(text='🏠 В меню', callback_data='to_main_menu')

    kb.row(today, tomorrow)
    kb.add(week)
    kb.add(to_menu)
    return kb


def make_settings_keyboard_for_user(user_id):
    """Персональная клавиатура настроек пользователя.
    -Персональные настройки
    -Админ-меню
    -🏠 В меню
    """

    kb = InlineKeyboardMarkup()
    user_status = db.get_person(user_id=user_id)['is_admin']

    personal_settings = Btn(text='Персон. настройки', callback_data='personal_settings')
    kb.add(personal_settings)
    if user_status:
       kb.add(Btn(text='🛡️ Админка 🛡️', callback_data='generate_admin_keyboard'))
    delete_me = Btn(text='🗑️ Удалить аккаунт 🗑️', callback_data='delete_me')
    to_menu = Btn(text='🏠 В меню', callback_data='to_main_menu')

    kb.add(delete_me)
    kb.add(to_menu)
    return kb


def personal_settings_menu(user_id, faculty, course, group):
    """Меню персональных настроек.
    -Сменить факультет
    -Сменить курс
    -Сменить группу
    """
    kb = InlineKeyboardMarkup()
    kb.add(Btn(text='⚖️ Сменить факультет', callback_data='change_faculty'))
    kb.row(Btn(text='🏫 Сменить курс', callback_data='change_course'),
           Btn(text='👥 Сменить группу', callback_data='choose_group'))
    kb.row(Btn(text='⚙  В параметры', callback_data='open_parameters_menu'),
           Btn(text='🏠 В меню', callback_data='to_main_menu'))
    return kb


def faculty_menu():
    """Меню выбора факультета.
    -МТС
    -МРМ
    -ИВТ
    -ГФ
    -АЭС
    """
    kb = InlineKeyboardMarkup()

    mts = Btn(text='МТС', callback_data='MTS_faculty')
    mrm = Btn(text='МРМ', callback_data='MRM_faculty')
    ivt = Btn(text='ИВТ', callback_data='IVT_faculty')
    gf = Btn(text='ГФ', callback_data='GF_faculty')
    aes = Btn(text='АЭС', callback_data='AES_faculty')

    kb.row(mts, mrm)
    kb.row(ivt, gf)
    kb.add(aes)
    return kb


def group_keyboard(user_id):
    """Меню выбора группы."""
    kb = InlineKeyboardMarkup()
    db_answer = db.get_person(user_id=user_id)
    faculty = db_answer['faculty']
    course = db_answer['course']
    if faculty == 'МТС' and course == 1:
        kb.row(Btn(text='МО-95', callback_data='МО-95'),
               Btn(text='МО-96', callback_data='МО-96'),
               Btn(text='ММ-91', callback_data='ММ-91'))
        kb.row(Btn(text='ММ-92', callback_data='ММ-92'),
               Btn(text='МП-98', callback_data='МП-98'))
        kb.row(Btn(text='МИ-97', callback_data='МИ-97'),
               Btn(text='МГ-196', callback_data='МГ-196'))
    elif faculty == 'МТС' and course == 2:
        kb.row(Btn(text='МО-85', callback_data='МО-85'),
               Btn(text='МО-86', callback_data='МО-86'),
               Btn(text='МИ-87', callback_data='МИ-87'),
               Btn(text='ММП-81', callback_data='ММП-81'))
        kb.row(Btn(text='МГ-186', callback_data='МГ-186'),
               Btn(text='МГ-187', callback_data='МГ-187'),
               Btn(text='ММП-82', callback_data='ММП-82'),
               Btn(text='МПП-88', callback_data='МПП-88'))
    elif faculty == 'МТС' and course == 3:
        kb.row(Btn(text='ММП-71', callback_data='ММП-71'),
               Btn(text='ММП-72', callback_data='ММП-72'),
               Btn(text='МО-75', callback_data='МО-75'),
               Btn(text='МПП-78', callback_data='МПП-78'),
               Btn(text='МИ-77', callback_data='МИ-77'))
    elif faculty == 'МТС' and course == 4:
        kb.row(Btn(text='МО-65', callback_data='МО-65'),
               Btn(text='МО-66', callback_data='МО-66'),
               Btn(text='МИ-67', callback_data='МИ-67'),
               Btn(text='ММП-61', callback_data='ММП-61'),
               Btn(text='МПП-68', callback_data='МПП-68'))
    elif faculty == 'МРМ' and course == 1:
        kb.row(Btn(text='РИ-91', callback_data='РИ-91'),
               Btn(text='РИ-92', callback_data='РИ-92'),
               Btn(text='РИ-93', callback_data='РИ-93'))
        kb.row(Btn(text='РС-91', callback_data='РС-91'),
               Btn(text='РС-92', callback_data='РС-92'),
               Btn(text='РСК-91', callback_data='РСК-91'))
        kb.row(Btn(text='РТ-91', callback_data='РТ-91'),
               Btn(text='РЦ-91', callback_data='РЦ-91'),
               Btn(text='РП-91', callback_data='РП-91'))
    elif faculty == 'МРМ' and course == 2:
        kb.row(Btn(text='РИ-87', callback_data='РИ-87'),
               Btn(text='РИ-88', callback_data='РИ-88'),
               Btn(text='РИ-89', callback_data='РИ-89'))
        kb.row(Btn(text='РСК-812', callback_data='РСК-812'),
               Btn(text='РСК-811', callback_data='РСК-811'),
               Btn(text='МГ-185', callback_data='МГ-185'))
        kb.row(Btn(text='РА-85', callback_data='РА-85'),
               Btn(text='РТ-84', callback_data='РТ-84'),
               Btn(text='РС-81', callback_data='РС-81'))
        kb.row(Btn(text='РЦ-82', callback_data='РЦ-82'),
               Btn(text='РП-86', callback_data='РП-86'),
               Btn(text='МГ-189', callback_data='МГ-189'))
    elif faculty == 'МРМ' and course == 3:
        kb.row(Btn(text='РИ-77', callback_data='РИ-77'),
               Btn(text='РИ-78', callback_data='РИ-78'),
               Btn(text='РА-75', callback_data='РА-75'))
        kb.row(Btn(text='РТ-74', callback_data='РТ-74'),
               Btn(text='РС-711', callback_data='РС-711'),
               Btn(text='РЦ-72', callback_data='РЦ-72'))
        kb.row(Btn(text='РС-71', callback_data='РС-71'),
               Btn(text='РП-76', callback_data='РП-76'),
               Btn(text='РСК-711', callback_data='РСК-711'),
               Btn(text='РСК-712', callback_data='РСК-712'))
    elif faculty == 'МРМ' and course == 4:
        kb.row(Btn(text='РИ-67', callback_data='РИ-67'),
               Btn(text='РИ-68', callback_data='РИ-68'),
               Btn(text='РЦ-62', callback_data='РЦ-62'))
        kb.row(Btn(text='РС-61', callback_data='РС-61'),
               Btn(text='РМ-63', callback_data='РМ-63'),
               Btn(text='РА-65', callback_data='РА-65'))
        kb.row(Btn(text='РТ-64', callback_data='РТ-64'),
               Btn(text='РП-66', callback_data='РП-66'),
               Btn(text='РСК-611', callback_data='РСК-611'))
    elif faculty == 'ИВТ' and course == 1:
        kb.row(Btn(text='ИП-913', callback_data='ИП-913'),
               Btn(text='ИВ-923', callback_data='ИВ-923'),
               Btn(text='ИВ-922', callback_data='ИВ-922'),
               Btn(text='ИП-916', callback_data='ИП-916'))
        kb.row(Btn(text='ИП-911', callback_data='ИП-911'),
               Btn(text='ИП-917', callback_data='ИП-917'),
               Btn(text='ИА-931', callback_data='ИА-931'),
               Btn(text='ИП-915', callback_data='ИП-915'))
        kb.row(Btn(text='ИА-932', callback_data='ИА-932'),
               Btn(text='ИП-914', callback_data='ИП-914'),
               Btn(text='ИП-912', callback_data='ИП-912'),
               Btn(text='ИС-942', callback_data='ИС-942'))
        kb.row(Btn(text='ИИ-961', callback_data='ИИ-961'),
               Btn(text='ИВ-921', callback_data='ИВ-921'),
               Btn(text='ИИ-962', callback_data='ИИ-962'),
               Btn(text='ИС-941', callback_data='ИС-941'))
        kb.row(Btn(text='МГ-192', callback_data='МГ-192'),
               Btn(text='МГ-191', callback_data='МГ-191'))
    elif faculty == 'ИВТ' and course == 2:
        kb.row(Btn(text='ИП-811', callback_data='ИП-811'),
               Btn(text='ИА-832', callback_data='ИА-832'),
               Btn(text='ИП-814', callback_data='ИП-814'),
               Btn(text='ИВ-823', callback_data='ИВ-823'))
        kb.row(Btn(text='ИП-816', callback_data='ИП-816'),
               Btn(text='ИА-831', callback_data='ИА-831'),
               Btn(text='ИП-815', callback_data='ИП-815'),
               Btn(text='ИП-813', callback_data='ИП-813'))
        kb.row(Btn(text='МГ-182', callback_data='МГ-182'),
               Btn(text='МГ-181', callback_data='МГ-181'),
               Btn(text='ИВ-821', callback_data='ИВ-821'),
               Btn(text='ИИ-861', callback_data='ИИ-861'))
        kb.row(Btn(text='ИС-842', callback_data='ИС-842'),
               Btn(text='ИМ-871', callback_data='ИМ-871'),
               Btn(text='ИП-812', callback_data='ИП-812'),
               Btn(text='ИВ-822', callback_data='ИВ-822'))
        kb.row(Btn(text='ИС-841', callback_data='ИС-841'),
               Btn(text='ИИ-862', callback_data='ИИ-862'))
    elif faculty == 'ИВТ' and course == 3:
        kb.row(Btn(text='ИП-713', callback_data='ИП-713'),
               Btn(text='ИП-715', callback_data='ИП-715'),
               Btn(text='ИВ-722', callback_data='ИВ-722'))
        kb.row(Btn(text='ИИ-761', callback_data='ИИ-761'),
               Btn(text='ИИ-762', callback_data='ИИ-762'),
               Btn(text='ИА-731', callback_data='ИА-731'))
        kb.row(Btn(text='ИС-742', callback_data='ИС-742'),
               Btn(text='ИП-714', callback_data='ИП-714'),
               Btn(text='ИС-741', callback_data='ИС-741'))
        kb.row(Btn(text='ИП-711', callback_data='ИП-711'),
               Btn(text='ИВ-721', callback_data='ИВ-721'),
               Btn(text='ИМ-771', callback_data='ИМ-771'))
        kb.row(Btn(text='ИП-712', callback_data='ИП-712'),
               Btn(text='ИА-732', callback_data='ИА-732'),
               Btn(text='ИБ-751', callback_data='ИБ-751'))
    elif faculty == 'ИВТ' and course == 4:
        kb.row(Btn(text='ИИ-661', callback_data='ИИ-661'),
               Btn(text='ИП-612', callback_data='ИП-612'),
               Btn(text='ИП-615', callback_data='ИП-615'))
        kb.row(Btn(text='ИВ-622', callback_data='ИВ-622'),
               Btn(text='ИИ-662', callback_data='ИИ-662'),
               Btn(text='ИП-614', callback_data='ИП-614'))
        kb.row(Btn(text='ИС-641', callback_data='ИС-641'),
               Btn(text='ИС-641', callback_data='ИС-641'),
               Btn(text='ИП-613', callback_data='ИП-613'))
        kb.row(Btn(text='ИП-611', callback_data='ИП-611'),
               Btn(text='ИМ-671', callback_data='ИМ-671'),
               Btn(text='ИА-631', callback_data='ИА-631'))
    elif faculty == 'ГФ' and course == 1:
        kb.row(Btn(text='ГР-91', callback_data='ГР-91'),
               Btn(text='ГР-92', callback_data='ГР-92'))
    elif faculty == 'ГФ' and course == 2:
        kb.row(Btn(text='ГР-81', callback_data='ГР-81'),
               Btn(text='ГР-82', callback_data='ГР-82'))
    elif faculty == 'ГФ' and course == 3:
        kb.row(Btn(text='ГР-71', callback_data='ГР-71'),
               Btn(text='ГР-72', callback_data='ГР-72'))
    elif faculty == 'ГФ' and course == 4:
        kb.row(Btn(text='ГР-61', callback_data='ГР-61'),
               Btn(text='ГР-62', callback_data='ГР-62'),
               Btn(text='ГР-63', callback_data='ГР-63'))
    elif faculty == 'АЭС' and course == 1:
        kb.row(Btn(text='АВ-912', callback_data='АВ-912'),
               Btn(text='АБ-95', callback_data='АБ-95'),
               Btn(text='АБ-98', callback_data='АБ-98'),
               Btn(text='АБ-97', callback_data='АБ-97'))
        kb.row(Btn(text='АП-93', callback_data='АП-93'),
               Btn(text='АБ-96', callback_data='АБ-96'),
               Btn(text='АБ-94', callback_data='АБ-94'),
               Btn(text='АП-92', callback_data='АП-92'))
        kb.row(Btn(text='АВ-911', callback_data='АВ-911'),
               Btn(text='АБ-99', callback_data='АБ-99'))
    elif faculty == 'АЭС' and course == 2:
        kb.row(Btn(text='АБ-87', callback_data='АБ-87'),
               Btn(text='АБ-86', callback_data='АБ-86'),
               Btn(text='АБ-88', callback_data='АБ-88'))
        kb.row(Btn(text='АВ-81', callback_data='АВ-81'),
               Btn(text='АВ-82', callback_data='АВ-82'),
               Btn(text='АБ-89', callback_data='АБ-89'))
        kb.row(Btn(text='АП-84', callback_data='АП-84'),
               Btn(text='АБ-85', callback_data='АБ-85'),
               Btn(text='АП-83', callback_data='АП-83'))
    elif faculty == 'АЭС' and course == 3:
        kb.row(Btn(text='АП-72', callback_data='АП-72'),
               Btn(text='АВ-712', callback_data='АВ-712'),
               Btn(text='АБ-751', callback_data='АБ-751'))
        kb.row(Btn(text='АБ-76', callback_data='АБ-76'),
               Btn(text='АП-73', callback_data='АП-73'),
               Btn(text='АБ-75', callback_data='АБ-75'))
        kb.row(Btn(text='АВ-711', callback_data='АВ-711'),
               Btn(text='АБ-74', callback_data='АБ-74'))
    elif faculty == 'АЭС' and course == 4:
        kb.row(Btn(text='А-63', callback_data='А-63'),
               Btn(text='А-64', callback_data='А-64'),
               Btn(text='АБ-65', callback_data='АБ-65'),
               Btn(text='АБ-66', callback_data='АБ-66'))
        kb.row(Btn(text='АБ-67', callback_data='АБ-67'),
               Btn(text='АП-62', callback_data='АП-62'),
               Btn(text='АВ-611', callback_data='АВ-611'))
    elif faculty == 'АЭС' and course == 5:
        kb.row(Btn(text='АБ-55', callback_data='АБ-55'),
               Btn(text='АБ-56', callback_data='АБ-56'),
               Btn(text='АВ-51', callback_data='АВ-51'))
    return kb


def course_keyboard(user_id):
    """Меню выбора курса.
    -1 курс
    -2 курс
    -3 курс
    -4 курс
    -5 курс
    -6 курс
    """
    faculty = db.get_info(user_id=user_id, column='faculty')
    kb = InlineKeyboardMarkup()

    first_course = Btn(text='1 курс', callback_data='set_1_course')
    second_course = Btn(text='2 курс', callback_data='set_2_course')
    third_course = Btn(text='3 курс', callback_data='set_3_course')
    fourth_course = Btn(text='4 курс', callback_data='set_4_course')

    kb.row(first_course, second_course)
    kb.row(third_course, fourth_course)
    if faculty == 'АЭС':
        fifth_course = Btn(text='5 курс', callback_data='set_5_course')
        kb.row(fifth_course)
    return kb


def week_menu():
    kb = InlineKeyboardMarkup()
    monday = Btn(text="Пн", callback_data='get_monday_schedule')
    tuesday = Btn(text="Вт", callback_data='get_tuesday_schedule')
    wednesday = Btn(text="Ср", callback_data='get_wednesday_schedule')
    thursday = Btn(text="Чт", callback_data='get_thursday_schedule')
    friday = Btn(text="Пт", callback_data='get_friday_schedule')
    saturday = Btn(text="Сб", callback_data='get_saturday_schedule')
    all_week = Btn(text="Вся неделя", callback_data='get_all_week')
    get_back = Btn(text="Вернуться", callback_data='get_schedule')

    kb.row(monday, tuesday, wednesday, thursday, friday, saturday)
    kb.add(all_week)
    kb.add(get_back)

    return kb


def lesson_time():
    """Меню обновления времени.
    -Обновить
    -🏠 В меню
    """
    kb = InlineKeyboardMarkup()
    kb.add(Btn(text='🔄 Обновить', callback_data='reload_time'))
    kb.add(Btn(text='🏠 В меню', callback_data='to_main_menu'))
    return kb


def additional_info():
    """Меню дополнительной информации.
    -Адреса корпусов
    -🏠 В меню
    """
    kb = InlineKeyboardMarkup()
    kb.add(Btn(text='🏠 В меню', callback_data='to_main_menu'))
    return kb


def formatting(user_id):
    """Меню настройки форматирования.
    -Показывать преподавателя
    -Показывать аудиторию
    """
    kb = InlineKeyboardMarkup()
    is_show_teacher = db.get_info(user_id=user_id, column='show_teacher')
    is_show_audience = db.get_info(user_id=user_id, column='show_audience')
    if is_show_teacher is True and is_show_audience is True:
        kb.add(Btn(text='Показывать преподавателя (✔)',
                   callback_data='change_show_teacher_status_off'))
        kb.add(Btn(text='Показывать аудиторию (✔)',
                   callback_data='change_show_audience_status_off'))
    elif is_show_teacher is False and is_show_audience is True:
        kb.add(Btn(text='Показывать преподавателя (❌)',
                   callback_data='change_show_teacher_status_on'))
        kb.add(Btn(text='Показывать аудиторию (✔)',
                   callback_data='change_show_audience_status_off'))
    elif is_show_teacher is True and is_show_audience is False:
        kb.add(Btn(text='Показывать преподавателя (✔)',
                   callback_data='change_show_teacher_status_off'))
        kb.add(Btn(text='Показывать аудиторию (❌)',
                   callback_data='change_show_audience_status_on'))
    else:
        kb.add(Btn(text='Показывать преподавателя (❌)',
                   callback_data='change_show_teacher_status_on'))
        kb.add(Btn(text='Показывать аудиторию (❌)',
                   callback_data='change_show_audience_status_on'))
    kb.row(Btn(text='⚙  В параметры', callback_data='open_parameters_menu'),
           Btn(text='🏠 В меню', callback_data='to_main_menu'))
    return kb


def admin_menu():
    """Админ-меню.
    -Статистика
    -Управление БД
    -Выполнить запрос
    -Вернуться
    """
    kb = InlineKeyboardMarkup()

    statistic = Btn(text='📈 Статистика', callback_data='get_bot_statistic')
    edit_db = Btn(text='📙 Управление БД', callback_data='get_edit_db')
    execute_query = Btn(text='💡 Выполнить запрос',
                        callback_data='execute_query')
    to_settings = Btn(text='Вернуться', callback_data='open_parameters_menu')

    kb.add(statistic, edit_db)
    kb.add(execute_query)
    kb.add(to_settings)
    return kb


def admin_statistic_menu():
    """Меню статистики [Админ-меню]
    -Кол-во пользователей
    -Вернуться в админку
    """
    kb = InlineKeyboardMarkup()

    users_count = Btn(text='📈 Кол-во юзеров',
                      callback_data='adminmenu_users_count')
    schedule_updates = Btn(text='🆕 Обновления расписания',
                           callback_data='adminmenu_schedule_updates')
    return_to_adminmenu = Btn(
        text='Вернуться в админку', callback_data='generate_admin_keyboard')
    kb.add(users_count, schedule_updates)
    kb.add(return_to_adminmenu)
    return kb


def admin_user_count_keyboard():
    """Меню подсчета пользователей.
    -Обновить
    -Вернуться в админку
    """
    kb = InlineKeyboardMarkup()
    reload = Btn(text='Обновить', callback_data='adminmenu_users_count')
    return_to_stats = Btn(
        text='Вернуться в админку', callback_data='get_bot_statistic')
    kb.add(reload)
    kb.add(return_to_stats)
    return kb


def admin_edit_db_menu():
    """Управление базой данных [Админ-меню]
    -Удалить запись
    -Очистить базу
    -Вернуться в админку
    """
    kb = InlineKeyboardMarkup()

    delete_string = Btn(text='Удалить запись',
                        callback_data='adminmenu_delete_string')
    truncate_table = Btn(text='Очистить базу',
                         callback_data='adminmenu_truncate_table')
    return_to_adminmenu = Btn(
        text='Вернуться в админку', callback_data='generate_admin_keyboard')
    kb.add(delete_string, truncate_table)
    kb.add(return_to_adminmenu)
    return kb


def delete_me_menu():
    """Меню самоудаления.
    -Уверен, удалить
    -Я передумал
    """
    kb = InlineKeyboardMarkup()
    kb.row(Btn(text='Уверен, удалить', callback_data='delete_me_yes'),
           Btn(text='Я передумал(а)', callback_data='open_parameters_menu'))
    return kb


async def es_open_user(user_id):
    user = await bot.get_chat(chat_id=user_id)
    print(user)
    kb = InlineKeyboardMarkup()
    show_profile = Btn(text="Открыть профиль", url=f"https://t.me/{user.username}")
    kb.add(show_profile)
    return kb
