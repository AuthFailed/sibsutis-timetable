from telebot.types import *
from telebot.types import InlineKeyboardButton as Btn

from main import db


def main_menu():
    """
    Клавиатура для главного меню.
    -Расписание
    -Время пар
    -Адреса корпусов
    -Настройки
    """
    kb = InlineKeyboardMarkup()
    get_schedule = Btn(
        '📅 Получить расписание', callback_data='get_schedule')
    get_lesson_time = Btn(
        '⌚ Время пар', callback_data='get_lesson_time')
    get_addresses = Btn(
        '🏠 Адреса корпусов', callback_data='get_addresses'
    )
    settings = Btn(
        '⚙️Настройки', callback_data='open_settings_menu')
    kb.add(get_schedule)
    kb.add(get_lesson_time)
    kb.add(get_addresses)
    kb.add(settings)
    return kb


def get_schedule_by_day():
    """
    Клавиатура для получения расписания.
    -Сегодня
    -Завтра
    -Неделя
    -В меню
    """
    kb = InlineKeyboardMarkup()

    today = Btn(
        'Сегодня', callback_data='get_today_schedule')
    tomorrow = Btn(
        'Завтра', callback_data='get_tomorrow_schedule')
    week = Btn(
        'Неделя', callback_data='get_week_schedule')
    to_menu = Btn(
        '🏠 В меню', callback_data='to_main_menu')
    kb.row(today, tomorrow)
    kb.add(week)
    kb.add(to_menu)
    return kb


def make_settings_keyboard_for_user(user_id):
    """Персональная клавиатура настроек пользователя.
    -Смена факультета
    -Смена курса
    -Смена группы
    -Изменение форматирования (преподаватели и аудитория)
    -Админ-меню
    """
    user_faculty = db.get_info(
        column='user_faculty', user_id=user_id)[0][0]
    user_status = db.get_info(column='user_admin', user_id=user_id)[0][0]
    user_group = db.get_info(column='user_group', user_id=user_id)[0][0]
    user_course = db.get_info(
        column='user_course', user_id=user_id)[0][0]
    show_teacher = db.get_info(column='show_teacher', user_id=user_id)[0][0]
    show_audience = db.get_info(column='show_audience', user_id=user_id)[0][0]
    kb = InlineKeyboardMarkup()
    if not user_faculty:
        kb.add(Btn('⚖️ Выбрать факультет', callback_data='change_faculty'))
    else:
        kb.add(Btn('⚖️ Сменить факультет (%s)' %
                   user_faculty, callback_data='change_faculty'))
    if not user_course and user_group is None:
        kb.row(Btn('🏫 Выбрать курс', callback_data='change_course'), Btn(
            '👥 Выбрать группу', callback_data='choose_group'))
    elif not user_course and user_group is not None:
        kb.row(Btn('🏫 Выбрать курс', callback_data='change_course'), Btn(
            '👥 Сменить группу (%s)' % user_group, callback_data='choose_group'))
    elif user_course is not None and user_group is None:
        kb.row(Btn('🏫 Сменить курс (%s)' % user_course, callback_data='change_course'), Btn(
            '👥 Выбрать группу', callback_data='choose_group'))
    else:
        kb.row(Btn('🏫 Сменить курс (%s)' % user_course, callback_data='change_course'), Btn(
            '👥 Сменить группу (%s)' % user_group, callback_data='choose_group'))
    if show_teacher is True and show_audience is True:
        kb.row(Btn('Показывать преподавателя (✔)', callback_data='change_show_teacher_status_off'),
               Btn('Показывать аудиторию (✔)', callback_data='change_show_audience_status_off'))
    elif show_teacher is False and show_audience is True:
        kb.row(Btn('Показывать преподавателя (❌)', callback_data='change_show_teacher_status_on'),
               Btn('Показывать аудиторию (✔)', callback_data='change_show_audience_status_off'))
    elif show_teacher is True and show_audience is False:
        kb.row(Btn('Показывать преподавателя (✔)', callback_data='change_show_teacher_status_off'),
               Btn('Показывать аудиторию (❌)', callback_data='change_show_audience_status_on'))
    else:
        kb.row(Btn('Показывать преподавателя (❌)', callback_data='change_show_teacher_status_on'),
               Btn('Показывать аудиторию (❌)', callback_data='change_show_audience_status_on'))

    if user_status:
        kb.add(Btn(
            '🛡️ Админка 🛡️', callback_data='generate_admin_keyboard'))
    delete_me = Btn('🗑️ Удалить аккаунт 🗑️', callback_data='delete_me')
    to_menu = Btn(
        '🏠 В меню', callback_data='to_main_menu')
    kb.add(delete_me)
    kb.add(to_menu)
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

    mts = Btn('МТС', callback_data='MTS_faculty')
    mrm = Btn('МРМ', callback_data='MRM_faculty')
    ivt = Btn('ИВТ', callback_data='IVT_faculty')
    gf = Btn('ГФ', callback_data='GF_faculty')
    aes = Btn('АЭС', callback_data='AES_faculty')

    kb.row(mts, mrm)
    kb.row(ivt, gf)
    kb.add(aes)
    return kb


def group_keyboard(user_id):
    """Меню выбора группы."""
    kb = InlineKeyboardMarkup()
    user_faculty = db.get_info(
        column='user_faculty', user_id=user_id)[0][0]
    user_course = db.get_info(
        column='user_course', user_id=user_id)[0][0]
    if user_faculty == 'МТС' and user_course == 1:
        kb.row(Btn('МО-95', callback_data='МО-95'),
               Btn('МО-96', callback_data='МО-96'),
               Btn('ММ-91', callback_data='ММ-91'))
        kb.row(Btn('ММ-92', callback_data='ММ-92'),
               Btn('МП-98', callback_data='МП-98'))
        kb.row(Btn('МИ-97', callback_data='МИ-97'),
               Btn('МГ-196', callback_data='МГ-196'))
    elif user_faculty == 'МТС' and user_course == 2:
        kb.row(Btn('МО-85', callback_data='МО-85'),
               Btn('МО-86', callback_data='МО-86'),
               Btn('МИ-87', callback_data='МИ-87'),
               Btn('ММП-81', callback_data='ММП-81'))
        kb.row(Btn('МГ-186', callback_data='МГ-186'),
               Btn('МГ-187', callback_data='МГ-187'),
               Btn('ММП-82', callback_data='ММП-82'),
               Btn('МПП-88', callback_data='МПП-88'))
    elif user_faculty == 'МТС' and user_course == 3:
        kb.row(Btn('ММП-71', callback_data='ММП-71'),
               Btn('ММП-72', callback_data='ММП-72'),
               Btn('МО-75', callback_data='МО-75'),
               Btn('МПП-78', callback_data='МПП-78'),
               Btn('МИ-77', callback_data='МИ-77'))
    elif user_faculty == 'МТС' and user_course == 4:
        kb.row(Btn('МО-65', callback_data='МО-65'),
               Btn('МО-66', callback_data='МО-66'),
               Btn('МИ-67', callback_data='МИ-67'),
               Btn('ММП-61', callback_data='ММП-61'),
               Btn('МПП-68', callback_data='МПП-68'))
    elif user_faculty == 'МРМ' and user_course == 1:
        kb.row(Btn('РИ-91', callback_data='РИ-91'),
               Btn('РИ-92', callback_data='РИ-92'),
               Btn('РИ-93', callback_data='РИ-93'))
        kb.row(Btn('РС-91', callback_data='РС-91'),
               Btn('РС-92', callback_data='РС-92'),
               Btn('РСК-91', callback_data='РСК-91'))
        kb.row(Btn('РТ-91', callback_data='РТ-91'),
               Btn('РЦ-91', callback_data='РЦ-91'),
               Btn('РП-91', callback_data='РП-91'))
    elif user_faculty == 'МРМ' and user_course == 2:
        kb.row(Btn('РИ-87', callback_data='РИ-87'),
               Btn('РИ-88', callback_data='РИ-88'),
               Btn('РИ-89', callback_data='РИ-89'))
        kb.row(Btn('РСК-812', callback_data='РСК-812'),
               Btn('РСК-811', callback_data='РСК-811'),
               Btn('МГ-185', callback_data='МГ-185'))
        kb.row(Btn('РА-85', callback_data='РА-85'),
               Btn('РТ-84', callback_data='РТ-84'),
               Btn('РС-81', callback_data='РС-81'))
        kb.row(Btn('РЦ-82', callback_data='РЦ-82'),
               Btn('РП-86', callback_data='РП-86'),
               Btn('МГ-189', callback_data='МГ-189'))
    elif user_faculty == 'МРМ' and user_course == 3:
        kb.row(Btn('РИ-77', callback_data='РИ-77'),
               Btn('РИ-78', callback_data='РИ-78'),
               Btn('РА-75', callback_data='РА-75'))
        kb.row(Btn('РТ-74', callback_data='РТ-74'),
               Btn('РС-711', callback_data='РС-711'),
               Btn('РЦ-72', callback_data='РЦ-72'))
        kb.row(Btn('РС-71', callback_data='РС-71'),
               Btn('РП-76', callback_data='РП-76'),
               Btn('РСК-711', callback_data='РСК-711'),
               Btn('РСК-712', callback_data='РСК-712'))
    elif user_faculty == 'МРМ' and user_course == 4:
        kb.row(Btn('РИ-67', callback_data='РИ-67'),
               Btn('РИ-68', callback_data='РИ-68'),
               Btn('РЦ-62', callback_data='РЦ-62'))
        kb.row(Btn('РС-61', callback_data='РС-61'),
               Btn('РМ-63', callback_data='РМ-63'),
               Btn('РА-65', callback_data='РА-65'))
        kb.row(Btn('РТ-64', callback_data='РТ-64'),
               Btn('РП-66', callback_data='РП-66'),
               Btn('РСК-611', callback_data='РСК-611'))
    elif user_faculty == 'ИВТ' and user_course == 1:
        kb.row(Btn('ИП-913', callback_data='ИП-913'),
               Btn('ИВ-923', callback_data='ИВ-923'),
               Btn('ИВ-922', callback_data='ИВ-922'),
               Btn('ИП-916', callback_data='ИП-916'))
        kb.row(Btn('ИП-911', callback_data='ИП-911'),
               Btn('ИП-917', callback_data='ИП-917'),
               Btn('ИА-931', callback_data='ИА-931'),
               Btn('ИП-915', callback_data='ИП-915'))
        kb.row(Btn('ИА-932', callback_data='ИА-932'),
               Btn('ИП-914', callback_data='ИП-914'),
               Btn('ИП-912', callback_data='ИП-912'),
               Btn('ИС-942', callback_data='ИС-942'))
        kb.row(Btn('ИИ-961', callback_data='ИИ-961'),
               Btn('ИВ-921', callback_data='ИВ-921'),
               Btn('ИИ-962', callback_data='ИИ-962'),
               Btn('ИС-941', callback_data='ИС-941'))
    elif user_faculty == 'ИВТ' and user_course == 2:
        kb.row(Btn('ИП-811', callback_data='ИП-811'),
               Btn('ИА-832', callback_data='ИА-832'),
               Btn('ИП-814', callback_data='ИП-814'),
               Btn('ИВ-823', callback_data='ИВ-823'))
        kb.row(Btn('ИП-816', callback_data='ИП-816'),
               Btn('ИА-831', callback_data='ИА-831'),
               Btn('ИП-815', callback_data='ИП-815'),
               Btn('ИП-813', callback_data='ИП-813'))
        kb.row(Btn('МГ-182', callback_data='МГ-182'),
               Btn('МГ-181', callback_data='МГ-181'),
               Btn('ИВ-821', callback_data='ИВ-821'),
               Btn('ИИ-861', callback_data='ИИ-861'))
        kb.row(Btn('ИС-842', callback_data='ИС-842'),
               Btn('ИМ-871', callback_data='ИМ-871'),
               Btn('ИП-812', callback_data='ИП-812'),
               Btn('ИВ-822', callback_data='ИВ-822'))
        kb.row(Btn('ИС-841', callback_data='ИС-841'),
               Btn('ИИ-862', callback_data='ИИ-862'))
    elif user_faculty == 'ИВТ' and user_course == 3:
        kb.row(Btn('ИП-713', callback_data='ИП-713'),
               Btn('ИП-715', callback_data='ИП-715'),
               Btn('ИВ-722', callback_data='ИВ-722'))
        kb.row(Btn('ИИ-761', callback_data='ИИ-761'),
               Btn('ИИ-762', callback_data='ИИ-762'),
               Btn('ИА-731', callback_data='ИА-731'))
        kb.row(Btn('ИС-742', callback_data='ИС-742'),
               Btn('ИП-714', callback_data='ИП-714'),
               Btn('ИС-741', callback_data='ИС-741'))
        kb.row(Btn('ИП-711', callback_data='ИП-711'),
               Btn('ИВ-721', callback_data='ИВ-721'),
               Btn('ИМ-771', callback_data='ИМ-771'))
        kb.row(Btn('ИП-712', callback_data='ИП-712'),
               Btn('ИА-732', callback_data='ИА-732'))
    elif user_faculty == 'ИВТ' and user_course == 4:
        kb.row(Btn('ИИ-661', callback_data='ИИ-661'),
               Btn('ИП-612', callback_data='ИП-612'),
               Btn('ИП-615', callback_data='ИП-615'))
        kb.row(Btn('ИВ-622', callback_data='ИВ-622'),
               Btn('ИИ-662', callback_data='ИИ-662'),
               Btn('ИП-614', callback_data='ИП-614'))
        kb.row(Btn('ИС-641', callback_data='ИС-641'),
               Btn('ИС-641', callback_data='ИС-641'),
               Btn('ИП-613', callback_data='ИП-613'))
        kb.row(Btn('ИП-611', callback_data='ИП-611'),
               Btn('ИМ-671', callback_data='ИМ-671'),
               Btn('ИА-631', callback_data='ИА-631'))
    elif user_faculty == 'ГФ' and user_course == 1:
        kb.row(Btn('ГР-91', callback_data='ГР-91'),
               Btn('ГР-92', callback_data='ГР-92'))
    elif user_faculty == 'ГФ' and user_course == 2:
        kb.row(Btn('ГР-81', callback_data='ГР-81'),
               Btn('ГР-82', callback_data='ГР-82'))
    elif user_faculty == 'ГФ' and user_course == 3:
        kb.row(Btn('ГР-71', callback_data='ГР-71'),
               Btn('ГР-72', callback_data='ГР-72'))
    elif user_faculty == 'ГФ' and user_course == 4:
        kb.row(Btn('ГР-61', callback_data='ГР-61'),
               Btn('ГР-62', callback_data='ГР-62'),
               Btn('ГР-63', callback_data='ГР-63'))
    elif user_faculty == 'АЭС' and user_course == 1:
        kb.row(Btn('АВ-912', callback_data='АВ-912'),
               Btn('АБ-95', callback_data='АБ-95'),
               Btn('АБ-98', callback_data='АБ-98'),
               Btn('АБ-97', callback_data='АБ-97'))
        kb.row(Btn('АП-93', callback_data='АП-93'),
               Btn('АБ-96', callback_data='АБ-96'),
               Btn('АБ-94', callback_data='АБ-94'),
               Btn('АП-92', callback_data='АП-92'))
        kb.row(Btn('АВ-911', callback_data='АВ-911'),
               Btn('АБ-99', callback_data='АБ-99'))
    elif user_faculty == 'АЭС' and user_course == 2:
        kb.row(Btn('АБ-87', callback_data='АБ-87'),
               Btn('АБ-86', callback_data='АБ-86'),
               Btn('АБ-88', callback_data='АБ-88'))
        kb.row(Btn('АВ-81', callback_data='АВ-81'),
               Btn('АВ-82', callback_data='АВ-82'),
               Btn('АБ-89', callback_data='АБ-89'))
        kb.row(Btn('АП-84', callback_data='АП-84'),
               Btn('АБ-85', callback_data='АБ-85'),
               Btn('АП-83', callback_data='АП-83'))
    elif user_faculty == 'АЭС' and user_course == 3:
        kb.row(Btn('АП-72', callback_data='АП-72'),
               Btn('АВ-712', callback_data='АВ-712'),
               Btn('АБ-751', callback_data='АБ-751'))
        kb.row(Btn('АБ-76', callback_data='АБ-76'),
               Btn('АП-73', callback_data='АП-73'),
               Btn('АБ-75', callback_data='АБ-75'))
        kb.row(Btn('АВ-711', callback_data='АВ-711'),
               Btn('АБ-74', callback_data='АБ-74'))
    elif user_faculty == 'АЭС' and user_course == 4:
        kb.row(Btn('А-63', callback_data='А-63'),
               Btn('А-64', callback_data='А-64'),
               Btn('АБ-65', callback_data='АБ-65'),
               Btn('АБ-66', callback_data='АБ-66'))
        kb.row(Btn('АБ-67', callback_data='АБ-67'),
               Btn('АП-62', callback_data='АП-62'),
               Btn('АВ-611', callback_data='АВ-611'))
    elif user_faculty == 'АЭС' and user_course == 5:
        kb.row(Btn('АБ-55', callback_data='АБ-55'),
               Btn('АБ-56', callback_data='АБ-56'),
               Btn('АВ-51', callback_data='АВ-51'))
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
    user_faculty = db.get_info(
        column='user_faculty', user_id=user_id)[0][0]
    kb = InlineKeyboardMarkup()

    first_course = Btn('1 курс', callback_data='set_1_course')
    second_course = Btn('2 курс', callback_data='set_2_course')
    third_course = Btn('3 курс', callback_data='set_3_course')
    fourth_course = Btn('4 курс', callback_data='set_4_course')

    kb.row(first_course, second_course)
    kb.row(third_course, fourth_course)
    if user_faculty == 'АЭС':
        fifth_course = Btn('5 курс', callback_data='set_5_course')
        kb.row(fifth_course)
    return kb


def lesson_time():
    """Меню обновления времени."""
    kb = InlineKeyboardMarkup()
    kb.add(Btn(
        '🔄 Обновить', callback_data='reload_time'))
    kb.add(Btn('🏠 В меню', callback_data='to_main_menu'))
    return kb


def admin_menu():
    """Админ-меню.
    -Статистика
    -Управление БД
    -Выполнить запрос
    -В настройки
    """
    kb = InlineKeyboardMarkup()

    statistic = Btn('📈 Статистика', callback_data='get_bot_statistic')
    edit_db = Btn('📙 Управление БД', callback_data='get_edit_db')
    execute_query = Btn('Выполнить запрос', callback_data='execute_query')
    to_settings = Btn('⚙️ В настройки', callback_data='to_settings')

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

    users_count = Btn(
        'Кол-во юзеров', callback_data='adminmenu_users_count')
    shedule_updates = Btn('Обновления расписания', callback_data='adminmenu_shedule_updates')
    return_to_adminmenu = Btn(
        'Вернуться в админку', callback_data='generate_admin_keyboard')
    kb.add(users_count, shedule_updates)
    kb.add(return_to_adminmenu)
    return kb


def admin_user_count_keyboard():
    """Меню подсчета пользователей.
    -Обновить
    -Вернуться в админку
    """
    kb = InlineKeyboardMarkup()
    reload = Btn('Обновить', callback_data='adminmenu_users_count')
    return_to_adminmenu = Btn(
        'Вернуться в админку', callback_data='generate_admin_keyboard')
    kb.add(reload)
    kb.add(return_to_adminmenu)
    return kb


def admin_edit_db_menu():
    """Управление базой данных [Админ-меню]
    -Удалить запись
    -Очистить базу
    -Вернуться в админку
    """
    kb = InlineKeyboardMarkup()

    delete_string = Btn(
        'Удалить запись', callback_data='adminmenu_delete_string')
    delete_db = Btn('Очистить базу', callback_data='adminmenu_truncate_table')
    truncate_db = Btn(
        'Очистить базу', callback_data='adminmenu_truncate_db')
    return_to_adminmenu = Btn(
        'Вернуться в админку', callback_data='generate_admin_keyboard')
    kb.add(delete_string, truncate_db)
    kb.add(delete_db)
    kb.add(return_to_adminmenu)
    return kb


def delete_me_menu():
    """Меню самоудаления."""
    kb = InlineKeyboardMarkup()
    kb.row(Btn('Уверен, удалить', callback_data='delete_me_yes'),
           Btn('Я передумал(а)', callback_data='delete_me_no'))
    return kb
