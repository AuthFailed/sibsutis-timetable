# -*- coding: utf-8 -*-

import logging
from datetime import *
from datetime import datetime

import pytz
import telebot
from telebot import TeleBot

import config as cfg
import dbworker
import keyboards as kb
import xls_handler

bot = TeleBot(cfg.token)

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

db = dbworker.Database(dbname=cfg.db_name,
                       username=cfg.db_username,
                       password=cfg.db_password,
                       host=cfg.db_host)


def get_time_to_lesson():
    """Получаем время до пары."""
    now = datetime.now().astimezone(pytz.timezone('Asia/Bangkok'))
    current_time = str(now.hour) + ':' + str(now.minute)

    today8 = now.replace(hour=8, minute=0)
    today930 = now.replace(hour=9, minute=30)
    today950 = now.replace(hour=9, minute=50)
    today1125 = now.replace(hour=11, minute=25)
    today1140 = now.replace(hour=11, minute=40)
    today1315 = now.replace(hour=13, minute=15)
    today1345 = now.replace(hour=13, minute=45)
    today1520 = now.replace(hour=15, minute=20)
    today1535 = now.replace(hour=15, minute=35)
    today1710 = now.replace(hour=17, minute=10)
    today1725 = now.replace(hour=17, minute=25)
    today1855 = now.replace(hour=18, minute=55)

    message = '⏰ Время пар:\n\n*1 пара*     __8:00 - 9:30__\n*2 пара*     __9:50 - 11:25__\n*3 пара*     __11:40 - ' \
              '13:15__\n*4 пара*     __13:45 - 15:20__\n*5 пара*     __15:35 - 17:10__\n*6 пара*     __17:25 - 18:55__ '
    if now < today8:
        message += '\n\n*Пары еще не начались*'
    elif today8 <= now <= today930:
        dt = today930 - now
        message += '\n\nСейчас идёт *1* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    elif today950 > now > today930:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today950 <= now <= today1125:
        dt = today1125 - now
        message += '\n\nСейчас идёт *2* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    elif today1125 < now < today1140:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today1140 <= now <= today1315:
        dt = today1315 - now
        message += '\n\nСейчас идёт *3* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    elif today1315 < now < today1345:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today1345 <= now <= today1520:
        dt = today1520 - now
        message += '\n\nСейчас идёт *4* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    elif today1520 < now < today1535:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today1535 <= now <= today1710:
        dt = today1710 - now
        message += '\n\nСейчас идёт *5* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    elif today1710 < now < today1725:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today1725 <= now <= today1855:
        dt = today1855 - now
        message += '\n\nСейчас идёт *6* пара, конец через *' + \
                   str(dt.seconds // 60) + '* минут'
    else:
        message += '\n\n*Пары кончились, отдыхай*'
    return message


def get_course(msg):
    """Смена этапа на изменение курса."""
    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='*Выберите курс:*',
                          reply_markup=kb.course_keyboard(msg.chat.id),
                          parse_mode='Markdown')


def get_group(msg):
    """Смена этапа на изменение группы."""
    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='*Выберите группу:*',
                          reply_markup=kb.group_keyboard(msg.chat.id),
                          parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def start_message(msg):
    """Стартовое сообщение."""
    if db.user_exists(user_id=msg.chat.id):
        bot.send_message(chat_id=msg.chat.id,
                         text='❗ Вы *уже зарегистрированы* в системе!\nЧтобы получить доступ к меню, используйте '
                              'команду */menu*',
                         reply_markup=kb.main_menu(),
                         parse_mode='Markdown')

    else:
        db.get_person(msg.chat.id)
        bot.reply_to(message=msg, text='Приветствую, *{}*. Выберите свою факультет:'.format(msg.from_user.first_name),
                     reply_markup=kb.faculty_menu(),
                     parse_mode='Markdown')


@bot.message_handler(commands=['menu'])
def send_message_main_menu(msg):
    """Сообщение с основным меню."""
    if not db.user_exists(msg.from_user.id):
        start_message(msg)
    else:
        bot.send_message(msg.chat.id, '*Меню:*',
                         reply_markup=kb.main_menu(),
                         parse_mode='Markdown')


@bot.message_handler(commands=['iamadmin'])
def i_am_admin(msg):
    """Установка прав администратора пользователю."""
    is_admin = db.get_info(
        column='user_admin', user_id=msg.chat.id)[0][0]
    if msg.chat.id in cfg.admins and is_admin is False:
        db.execute("UPDATE Users SET user_admin=True where user_id=%s" % msg.chat.id)
        bot.send_message(msg.chat.id, 'Группа успешно изменена! Теперь у вас есть доступ к *Админ-Меню* в настройках.', parse_mode='Markdown')
    elif is_admin:
        bot.send_message(msg.chat.id, 'Вы уже администратор!', parse_mode='Markdown')
    else:
        bot.send_message(msg.chat.id, 'Вы не администратор!', parse_mode='Markdown')


@bot.message_handler(commands=['execute'])
def execute_first(msg):
    """Первый этап запроса к базе данных."""
    is_admin = db.get_info(
        column='user_admin', user_id=msg.chat.id)[0][0]
    if is_admin:
        msg = bot.send_message(
            msg.chat.id, '*Введите запрос:*', parse_mode='Markdown')
    else:
        bot.send_message(msg.chat.id, 'Вы не администратор!', parse_mode='Markdown')


def db_execute(msg):
    """Второй этап запроса к базе данных."""
    try:
        bot.send_message(msg.chat.id, db.execute(msg.text))
    except Exception as e:
        bot.send_message(
            msg.chat.id, 'Не удалось выполнить запрос.\n %s' % e, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    """Отлавливаем кэллбэки телеграма."""
    if call.data == 'to_main_menu':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text='*Меню:*',
                              reply_markup=kb.main_menu(),
                              parse_mode='Markdown')
    elif call.data == "to_settings":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text='*Настройки:*',
                              parse_mode='Markdown',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == 'get_lesson_time':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=get_time_to_lesson(), reply_markup=kb.lesson_time(),
                              parse_mode='Markdown')
    elif call.data == 'open_settings_menu':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text='*Настройки:*',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                              parse_mode='Markdown')
    elif call.data == 'choose_group':
        bot.answer_callback_query(call.id)
        get_group(call.message)
    elif call.data == 'reload_time':
        if call.message.text != get_time_to_lesson().replace("*", "").replace("__", ""):
            bot.edit_message_text(text=get_time_to_lesson(), chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=kb.lesson_time(),
                                  parse_mode='Markdown')
        else:
            bot.answer_callback_query(call.id, text='Не нажимайте так часто!')
    elif call.data == 'change_faculty':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Выберите факультет:*', reply_markup=kb.faculty_menu(),
                              parse_mode='Markdown')
    elif call.data == 'change_course':
        bot.answer_callback_query(call.id)
        get_course(call.message)
    elif call.data == 'MTS_faculty':
        db.change_faculty(call.from_user.id, faculty='МТС')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'MRM_faculty':
        db.change_faculty(call.message.chat.id, faculty='МРМ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'IVT_faculty':
        db.change_faculty(call.message.chat.id, faculty='ИВТ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'GF_faculty':
        db.change_faculty(call.message.chat.id, faculty='ГФ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'AES_faculty':
        db.change_faculty(call.message.chat.id, faculty='АЭС')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'set_1_course':
        db.change_course(user_id=call.message.chat.id, course='1')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_2_course':
        db.change_course(user_id=call.message.chat.id, course='2')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_3_course':
        db.change_course(user_id=call.message.chat.id, course='3')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_4_course':
        db.change_course(user_id=call.message.chat.id, course='4')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_5_course':
        db.change_course(user_id=call.message.chat.id, course='5')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)

    elif call.data == 'set_6_course':
        db.change_course(user_id=call.message.chat.id, course='6')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'change_show_teacher_status_off':
        bot.answer_callback_query(call.id)
        db.change_show_teacher_status(user_id=call.message.chat.id, status=False)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      inline_message_id=call.inline_message_id,
                                      reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == 'change_show_teacher_status_on':
        bot.answer_callback_query(call.id)
        db.change_show_teacher_status(user_id=call.message.chat.id, status=True)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      inline_message_id=call.inline_message_id,
                                      reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == 'change_show_audience_status_on':
        bot.answer_callback_query(call.id)
        db.change_show_audience_status(user_id=call.message.chat.id, status=True)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      inline_message_id=call.inline_message_id,
                                      reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == 'change_show_audience_status_off':
        bot.answer_callback_query(call.id)
        db.change_show_audience_status(user_id=call.message.chat.id, status=False)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      inline_message_id=call.inline_message_id,
                                      reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))

    elif call.data == 'delete_me':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы уверены? *Аккаунт восстановлению не подлежит!*',
                              parse_mode='Markdown',
                              reply_markup=kb.delete_me_menu())

    elif call.data == 'delete_me_yes':
        bot.answer_callback_query(call.id)
        if db.user_exists(call.message.chat.id):
            try:
                db.delete_person(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Аккаунт был *удален!*\nЧтобы заново зарегистрироваться используйте '
                                           'команду /start.',
                                      parse_mode='Markdown')
            except Exception as e:
                bot.send_message(call.message.chat.id, 'Ошибка! \n %s' % e, parse_mode='Markdown')
        else:
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id, '*Вы не зарегистрированы!*\n qИспользуйте команду /start.', parse_mode='Markdown')

    elif call.data == 'delete_me_no':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Настройки:*',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                              parse_mode='Markdown')

    elif call.data == 'generate_admin_keyboard':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Админ-меню:*', reply_markup=kb.admin_menu(), parse_mode='Markdown')

    elif call.data == 'adminmenu_delete_string':
        bot.answer_callback_query(call.id)
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите ключ:*',
            parse_mode='Markdown')
        try:
            bot.register_next_step_handler(msg, db.delete_person)
            bot.send_message(chat_id=call.message.chat.id,
                             text='Пользователь успешно удалён!', parse_mode='Markdown')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='*Админ-меню:*', reply_markup=kb.admin_menu(), parse_mode='Markdown')
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла непредвиденная ошибка!\nТекст ошибки: %s' % e, parse_mode='Markdown')

    elif call.data == 'adminmenu_truncate_table':
        bot.answer_callback_query(call.id)
        try:
            db.truncate_table()
            bot.send_message(chat_id=call.message.chat.id,
                             text='База успешно очищена.',
                             parse_mode='Markdown')
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла непредвиденная ошибка!\nТекст ошибки: %s' % e, parse_mode='Markdown')

    elif call.data == 'adminmenu_truncate_db':
        bot.answer_callback_query(call.id)
        try:
            db.execute('TRUNCATE TABLE Users')
            bot.send_message(chat_id=call.message.chat.id,
                             text='База успешно очищена!', parse_mode='Markdown')
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла  непредвиденная ошибка!\nТекст ошибки: %s' % e, parse_mode='Markdown')

    elif call.data == 'get_schedule':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Выберите пункт:*',
                              reply_markup=kb.get_schedule_by_day(), parse_mode='Markdown')

    elif call.data == 'get_today_schedule':
        bot.send_chat_action(call.message.chat.id, action="typing")
        user_group = db.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]
        show_teacher = db.get_info(column='show_teacher', user_id=call.message.chat.id)[0][0]
        show_audience = db.get_info(column='show_audience', user_id=call.message.chat.id)[0][0]
        message_to_send = xls_handler.get_today_schedule(user_group)
        message_to_send = xls_handler.format_message(text=message_to_send,
                                                     teacher=show_teacher,
                                                     audience=show_audience)
        if message_to_send.replace("*", "").replace("_", "") != call.message.text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send,
                                  reply_markup=kb.get_schedule_by_day(), parse_mode='Markdown')
            bot.answer_callback_query(call.id, text="")
        else:
            bot.answer_callback_query(call.id, text='Вы видите расписание на сегодняшний день!')

    elif call.data == 'get_tomorrow_schedule':
        bot.answer_callback_query(call.id)
        bot.send_chat_action(call.message.chat.id, action="typing")
        user_group = db.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]
        show_teacher = db.get_info(column='show_teacher', user_id=call.message.chat.id)[0][0]
        show_audience = db.get_info(column='show_audience', user_id=call.message.chat.id)[0][0]
        message_to_send = xls_handler.get_tomorrow_schedule(user_group)
        message_to_send = xls_handler.format_message(text=message_to_send,
                                                     teacher=show_teacher,
                                                     audience=show_audience)
        if message_to_send.replace("*", "").replace("_", "") != call.message.text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send,
                                  reply_markup=kb.get_schedule_by_day(),
                                  parse_mode='Markdown')
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, text='Вы видите расписание на завтрашний день!')

    elif call.data == 'adminmenu_users_count':
        bot.answer_callback_query(call.id)
        arr = db.get_user_count()
        message_to_send = '__Всего пользователей:__ *%s*\n\nМТС: *%s*\nМРМ: *%s*\nИВТ: *%s*\nАЭС: *%s*\nГФ: *%s*' % (
            arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
        if call.message.text != message_to_send.replace("*", "").replace("__", ""):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send, reply_markup=kb.admin_user_count_keyboard(),
                                  parse_mode='Markdown')
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, text='Изменений нет!')
    elif call.data == 'adminmenu_shedule_updates':
        bot.answer_callback_query(call.id)
        query_result = db.execute("SELECT (file_name, version) from fs")
        bot.send_message(call.message.chat.id, query_result)
    elif call.data == 'get_bot_statistic':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Статистика бота*',
                              reply_markup=kb.admin_statistic_menu(),
                              parse_mode='Markdown')
    elif call.data == 'get_edit_db':
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Настройка базы данных*',
                              reply_markup=kb.admin_edit_db_menu(),
                              parse_mode='Markdown')
        bot.answer_callback_query(call.id, text="")
    elif call.data == 'execute_query':
        msg = bot.send_message(call.message.chat.id, text='Введите текст запроса:', parse_mode='Markdown')
        bot.register_next_step_handler(msg, db_execute)
    elif call.data == 'get_addresses':
        bot.answer_callback_query(call.id)
        bot.send_chat_action(call.message.chat.id, action='typing')
        bot.send_message(chat_id=call.message.chat.id,
                         text='Главный корпус *(№1)* находится по адресу *ул. Гурьевская, д. 51*',
                         parse_mode='Markdown')
        bot.send_location(chat_id=call.message.chat.id,
                          latitude=55.0131135,
                          longitude=82.9483222)
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Корпус 2* и *корпус 3* находятся по адресу *ул. Кирова, д. 86*',
                         parse_mode='Markdown')
        bot.send_location(chat_id=call.message.chat.id,
                          latitude=55.0139281,
                          longitude=82.9478923)
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Корпус 4* находится по адресу *ул. Нижегородская, д. 23*')
        bot.send_location(chat_id=call.message.chat.id,
                          latitude=55.0126721,
                          longitude=82.9466813)
        bot.send_message(chat_id=call.message.chat.id,
                         text='*Корпус 5* находится по адресу *ул. Бориса Богаткова, д. 51*',
                         parse_mode='Markdown')
        bot.send_location(chat_id=call.message.chat.id,
                          latitude=55.016897,
                          longitude=82.949896)
    else:
        bot.answer_callback_query(call.id)
        user_group = db.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]
        if not user_group:
            db.change_group(call.message.chat.id, call.data)
            db.change_reg_date(call.message.chat.id, str(date.today()))
            bot.answer_callback_query(call.id, text='Группа выбрана.')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='*Меню:*', reply_markup=kb.main_menu(),
                                  parse_mode='Markdown')
        else:
            db.change_group(call.message.chat.id, call.data)
            bot.answer_callback_query(call.id, text='Курс изменён.')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='*Настройки:*',
                                  reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                                  parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
