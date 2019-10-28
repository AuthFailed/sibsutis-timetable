# -*- coding: utf-8 -*-

import re
from datetime import *
from datetime import datetime

import pytz
from telebot import TeleBot

import config
import dbworker
import keyboards as kb
import xls_handler

bot = TeleBot(config.token)


def get_time_to_lesson():
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


def get_course(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='*Выберите курс:*',
                          reply_markup=kb.course_keyboard(message.chat.id), parse_mode='Markdown')


def get_group(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='*Выберите группу:*',
                          parse_mode='Markdown', reply_markup=kb.group_keyboard(message.chat.id))


def set_email(message):
    if not dbworker.user_exists(message.chat.id):
        if re.match(r"\A[^@]+@([^@]+\.)+[^@]", message.text):
            dbworker.change_mail(user_id=message.chat.id, mail=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='*Меню:*',
                             reply_markup=kb.make_settings_keyboard_for_user(message.chat.id),
                             parse_mode='Markdown')
    else:
        if re.match(r"\A[^@]+@([^@]+\.)+[^@]", message.text):
            dbworker.change_mail(user_id=message.chat.id, mail=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='*Меню:*',
                             reply_markup=kb.make_settings_keyboard_for_user(message.chat.id),
                             parse_mode='Markdown')


# def send_mail():
#     # Основные параметры
#     msg = MIMEMultipart()
#     msg['Subject'] = 'Изменение расписания'
#     msg['From'] = 'authfailed@gmail.com'

# body = email.mime.text.MIMEText( get_edit_time() + "\nСкачать обновленное расписание можно <a
# href=\"https://sibsutis.ru/students/study/webdav_bizproc_history_get/3062720/3062720/?ncc=1&force_download=1
# \">здесь</a>", 'html') msg.attach(body)

#     # Прикрепляем расписание
#     filename = './new_shedule.doc'
#     fp = open(filename, 'rb')
#     att = email.mime.application.MIMEApplication(fp.read(), _subtype="doc")
#     fp.close()
#     att.add_header('Content-Disposition', 'attachment',
#                    filename="Расписание.doc")
#     msg.attach(att)

#     # Соединяемся с сервером
#     mail = smtplib.SMTP('smtp.gmail.com', 587)
#     mail.ehlo()
#     mail.starttls()
#     mail.login(config.login, config.password)
#     mail.sendmail("authfailed@gmail.con", [
#                   'authfailed@gmail.com',
#                   'lorarin97@mail.ru'], msg.as_string())
#     print("Уведомления отправлены!")


@bot.message_handler(commands=['start'])
def start_message(message):
    if dbworker.user_exists(user_id=message.chat.id):
        bot.send_message(chat_id=message.chat.id,
                         text='❗ Вы *уже зарегистрированы* в системе!\nЧтобы получить доступ к меню, используйте '
                              'команду */menu*',
                         parse_mode='Markdown', reply_markup=kb.main_menu())

    else:
        dbworker.get_person(message.chat.id)

        bot.send_message(chat_id=message.chat.id,
                         text='Приветствую, *' + message.from_user.first_name +
                              '*. Выбери свою факультет:',
                         parse_mode='Markdown', reply_markup=kb.faculty_menu())


@bot.message_handler(commands=['menu'])
def send_message_main_menu(message):
    if not dbworker.user_exists(message.from_user.id):
        start_message(message)
    else:
        bot.send_message(message.chat.id, '*Меню:*',
                         parse_mode='Markdown', reply_markup=kb.main_menu())


@bot.message_handler(commands=['iamadmin'])
def i_am_admin(message):
    is_admin = dbworker.get_info(
        column='user_admin', user_id=message.chat.id)[0][0]
    if message.chat.id in config.admins and is_admin is False:
        dbworker.db.execute('UPDATE Users SET user_admin=True where user_id=%s' % message.chat.id)
        bot.send_message(message.chat.id, 'Группа изменена!')
    elif is_admin:
        bot.send_message(message.chat.id, 'Вы уже администратор!')
    else:
        bot.send_message(message.chat.id, 'Вы не администратор!')


@bot.message_handler(commands=['execute'])
def execute_first(message):
    is_admin = dbworker.get_info(
        column='user_admin', user_id=message.chat.id)[0][0]
    print(is_admin)
    if is_admin:
        msg = bot.send_message(
            message.chat.id, '*Введите запрос:*', parse_mode='Markdown')
        bot.register_next_step_handler(msg, db_execute)
    else:
        bot.send_message(message.chat.id, 'Вы не администратор!')


def db_execute(query):
    try:
        bot.send_message(query.chat.id, dbworker.execute(query.text))
    except Exception as e:
        bot.send_message(
            query.chat.id, 'Не удалось выполнить запрос.\n %s' % e)


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "to_settings":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Настройки:*',
                              parse_mode='Markdown',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == "off_notifications":
        dbworker.notification_status(call.from_user.id, status=False)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Настройки:*',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                              parse_mode='Markdown')
    elif call.data == "on_notifications":
        dbworker.notification_status(call.from_user.id, status=True)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id))
    elif call.data == 'get_lesson_time':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=get_time_to_lesson(), parse_mode='Markdown', reply_markup=kb.lesson_time())
    elif call.data == 'open_settings_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Настройки:*',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                              parse_mode='Markdown')
    elif call.data == 'choose_group':
        get_group(call.message)
    elif call.data == 'to_main_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Меню:*', parse_mode='Markdown', reply_markup=kb.main_menu())
    elif call.data == 'edit_mail':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите email:*',
            parse_mode='Markdown')
        bot.register_next_step_handler(msg, set_email)
    elif call.data == 'reload_time':
        if call.message.text != get_time_to_lesson().replace("*", "").replace("__", ""):
            bot.edit_message_text(text=get_time_to_lesson(), chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, parse_mode='Markdown',
                                  reply_markup=kb.lesson_time())
        else:
            bot.answer_callback_query(call.id, text='Не нажимайте так часто!')
    elif call.data == 'change_faculty':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Выберите факультет:*', reply_markup=kb.faculty_menu(), parse_mode='Markdown')
    elif call.data == 'change_course':
        get_course(call.message)
    elif call.data == 'MTS_faculty':
        dbworker.change_faculty(call.message.chat.id, 'МТС')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'MRM_faculty':
        dbworker.change_faculty(call.message.chat.id, 'МРМ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'IVT_faculty':
        dbworker.change_faculty(call.message.chat.id, 'ИВТ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'GF_faculty':
        dbworker.change_faculty(call.message.chat.id, 'ГФ')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'AES_faculty':
        dbworker.change_faculty(call.message.chat.id, 'АЭС')
        bot.answer_callback_query(call.id, text='Факультет выбран.')
        get_course(call.message)
    elif call.data == 'set_1_course':
        dbworker.change_course(user_id=call.message.chat.id, course='1')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_2_course':
        dbworker.change_course(user_id=call.message.chat.id, course='2')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_3_course':
        dbworker.change_course(user_id=call.message.chat.id, course='3')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_4_course':
        dbworker.change_course(user_id=call.message.chat.id, course='4')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_5_course':
        dbworker.change_course(user_id=call.message.chat.id, course='5')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'set_6_course':
        dbworker.change_course(user_id=call.message.chat.id, course='6')
        bot.answer_callback_query(call.id, text='Курс выбран.')
        get_group(call.message)
    elif call.data == 'delete_me':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы уверены? *Аккаунт восстановлению не подлежит!*',
                              parse_mode='Markdown',
                              reply_markup=kb.delete_me_menu())
    elif call.data == 'delete_me_yes':
        if dbworker.user_exists(call.message.chat.id):
            try:
                dbworker.delete_person(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Аккаунт был *удален!*\nЧтобы заново зарегистрироваться используйте '
                                           'команду /start.',
                                      parse_mode='Markdown')
            except Exception as e:
                bot.send_message(call.message.chat.id, 'Ошибка! \n %s' % e)
        else:
            bot.send_message(
                call.message.chat.id, '*Вы не зарегистрированы!*\n qИспользуйте команду /start.')
    elif call.data == 'delete_me_no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Настройки:*',
                              reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                              parse_mode='Markdown')
    elif call.data == 'generate_admin_keyboard':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Админ-меню:*', parse_mode='Markdown', reply_markup=kb.admin_menu())
    elif call.data == 'adminmenu_delete_string':
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Введите ключ:*',
            parse_mode='Markdown')
        try:
            bot.register_next_step_handler(msg, dbworker.delete_person)
            bot.send_message(chat_id=call.message.chat.id,
                             text='Пользователь успешно удалён!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='*Админ-меню:*', parse_mode='Markdown', reply_markup=kb.admin_menu())
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла непредвиденная ошибка!\nТекст ошибки: %s' % e)
    elif call.data == 'adminmenu_delete_db':
        try:
            dbworker.delete_db()
            bot.send_message(chat_id=call.message.chat.id,
                             text='База успешно удалена. Перезагрузите бота для повторного создания базы.')
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла непредвиденная ошибка!\nТекст ошибки: %s' % e)
    elif call.data == 'adminmenu_truncate_db':
        try:
            dbworker.execute('TRUNCATE TABLE Users')
            bot.send_message(chat_id=call.message.chat.id,
                             text='База успешно очищена!')
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Произошла  непредвиденная ошибка!\nТекст ошибки: %s' % e)
    elif call.data == 'get_schedule':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Выберите пункт:*', parse_mode='Markdown', reply_markup=kb.get_schedule_by_day())
    elif call.data == 'get_today_schedule':
        bot.send_chat_action(call.message.chat.id, action="typing")
        user_group = dbworker.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]

        message_to_send = xls_handler.get_today_schedule(user_group)
        print(bool(message_to_send != call.message.text))
        if message_to_send.replace("*", "").replace("__", "") != call.message.text:

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send, parse_mode='Markdown', reply_markup=kb.get_schedule_by_day())
            bot.answer_callback_query(call.id, text="")
        else:
            bot.answer_callback_query(call.id, text='Вы видите расписание на сегодняшний день!')

    elif call.data == 'get_tomorrow_schedule':
        bot.send_chat_action(call.message.chat.id, action="typing")
        user_group = dbworker.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]

        message_to_send = xls_handler.get_tomorrow_schedule(user_group)
        print(message_to_send)
        if message_to_send.replace("*", "").replace("__", "") != call.message.text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send, parse_mode='Markdown', reply_markup=kb.get_schedule_by_day())
            bot.answer_callback_query(call.id, text="")
        else:
            bot.answer_callback_query(call.id, text='Вы видите расписание на завтрашний день!')

    elif call.data == 'adminmenu_users_count':
        arr = dbworker.get_user_count()
        message_to_send = '__Всего пользователей:__ *%s*\n\nМТС: *%s*\nМРМ: *%s*\nИВТ: *%s*\nАЭС: *%s*\nГФ: *%s*' % (
            arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
        if call.message.text != message_to_send.replace("*", "").replace("__", ""):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=message_to_send, reply_markup=kb.admin_user_count_keyboard(),
                                  parse_mode='Markdown')
            bot.answer_callback_query(call.id, text="")
        else:
            bot.answer_callback_query(call.id, text='Изменений нет!')
    elif call.data == 'get_bot_statistic':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Статистика бота*', parse_mode='Markdown', reply_markup=kb.admin_statistic_menu())
    elif call.data == 'get_edit_db':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='*Настройка базы данных*', parse_mode='Markdown',
                              reply_markup=kb.admin_edit_db_menu())
        bot.answer_callback_query(call.id, text="")
    else:
        user_group = dbworker.get_info(
            column='user_group', user_id=call.message.chat.id)[0][0]
        if not user_group:
            dbworker.change_group(call.message.chat.id, call.data)
            dbworker.change_reg_date(call.message.chat.id, str(date.today()))
            bot.answer_callback_query(call.id, text='Группа выбрана.')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='*Меню:*', reply_markup=kb.main_menu(), parse_mode='Markdown')
        else:
            dbworker.change_group(call.message.chat.id, call.data)
            bot.answer_callback_query(call.id, text='Курс изменён.')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Настройки:*',
                                  reply_markup=kb.make_settings_keyboard_for_user(call.message.chat.id),
                                  parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling(none_stop=True)
    # check_for_updates()
