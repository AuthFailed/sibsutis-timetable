# -*- coding: utf-8 -*-
import logging
import asyncio
import uvloop
from aiogram import executor, types
from aiogram.utils.markdown import *
from aiogram.utils.exceptions import *
from aiogram.types import *
import config as cfg
from config import db
import keyboards as kb

import event_handler
import error_handler
from subprocess import call
from datetime import *
from datetime import datetime
import pytz
import xls_handler

# Configure logging
logging.basicConfig(level=logging.INFO)

dp = cfg.dp
bot = cfg.bot


def filter_chat_is_private(msg: types.Message, *_, **__):
    return ChatType.is_private(msg)


async def is_admin(user_id):
    user_status = db.get_info(user_id=user_id, column='user_admin')
    if user_status:
        return True
    else:
        return False


async def db_execute(msg):
    """Запрос к базе данных."""
    try:
        msg.reply(text=db.execute(msg.text))
    except Exception as e:
        msg.reply(text='Не удалось выполнить запрос\.\n__%s__' % e)
        error_handler.add_error_to_log(user=msg.from_user.username, error=e)


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

    message = '⏰ Время пар:\n\n*1 пара*     __8:00 \- 9:30__\n*2 пара*     __9:50 \- 11:25__\n*3 пара*     __11:40 \- ' \
              '13:15__\n*4 пара*     __13:45 \- 15:20__\n*5 пара*     __15:35 \- 17:10__\n*6 пара*     __17:25 \- 18:55__ '
    if now < today8:
        message += '\n\n*Пары еще не начались*'
    elif today8 <= now <= today930:
        dt = today930 - now
        message += f'\n\nСейчас идёт {b("1")} пара, конец через {b(str(dt.seconds // 60))} минут'
    elif today950 > now > today930:
        message += '\n\nСейчас ' + current_time + ' | Перемена'
    elif today950 <= now <= today1125:
        dt = today1125 - now
        message += f'\n\nСейчас идёт *2* пара, конец через *' + \
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


async def get_course(msg):
    """Смена этапа на изменение курса."""
    await msg.edit_text(text='*Выберите курс:*',
                        reply_markup=kb.course_keyboard(msg.chat.id),
                        )


async def get_group(msg):
    """Смена этапа на изменение группы."""
    await msg.edit_text(text='*Выберите группу:*',
                        reply_markup=kb.group_keyboard(msg.chat.id),
                        )


@dp.message_handler(commands=['start'])
async def start_message(msg: types.Message):
    """Стартовое сообщение."""
    if filter_chat_is_private(msg):
        if db.user_exists(user_id=msg.chat.id):
            await msg.answer(text='❗ Вы *уже зарегистрированы* в системе\!\n'
                                  'Чтобы получить доступ к меню, используйте команду */menu*')

        else:
            db.get_person(msg.chat.id)
            await msg.answer(text=f'Приветствую, *{msg.from_user.first_name}*\. Выберите свою факультет:',
                             reply_markup=kb.faculty_menu())
    else:
        await msg.answer(
            text=f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}), бот работает только в *личных сообщениях*\.")


@dp.message_handler(commands=['menu'])
async def send_message_main_menu(msg: Message):
    """Сообщение с основным меню."""
    if filter_chat_is_private(msg=msg):
        if not db.user_exists(msg.from_user.id):
            await start_message(msg)
        else:
            await msg.answer(text='*Меню:*',
                             reply_markup=kb.main_menu())
    else:
        await msg.answer(
            text=f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}), бот работает только в *личных сообщениях*\.")


@dp.message_handler(commands=['iamadmin'])
async def i_am_admin(msg: Message):
    """Установка прав администратора пользователю."""
    if filter_chat_is_private(msg):
        if msg.from_user.id in cfg.admin_list and is_admin is False:
            db.execute("UPDATE Users SET user_admin=True where user_id=%s" % msg.from_user.id)
            await msg.answer(text='Группа успешно изменена! Теперь у вас есть доступ к *Админ\-Меню* в настройках\.',
                             )
            
        elif is_admin:
            await msg.answer(text='Вы уже администратор!')
        else:
            await msg.answer('Вы не администратор!')
    else:
        await msg.answer(
            text=f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}), бот работает только в *личных сообщениях*\\.",
            parse_mode="Markdown")


@dp.message_handler(commands=['ping', 'пинг'])
async def ping(msg):
    if filter_chat_is_private(msg):
        await msg.answer(text="Понг")
    else:
        await msg.answer(
            text=f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}), бот работает только в *личных сообщениях*\\.")


@dp.message_handler(commands=['server'])
async def send_server(msg: Message):
    if filter_chat_is_private(msg):
        if is_admin(msg.from_user.id):
            try:
                # по этому пути на сервере лежит скрипт сбора информации по статусу сервера
                call([". /root/code/sibsutis-timetable/status.sh"])
                # читает файл с результатами выполнения скрипта
                status = open("/root/code/sibsutis-timetable/status.txt", "r+").read()
                await msg.answer(text=status)
            except Exception as e:
                error_handler.logger.exception(str(e))
                await msg.answer(text="Ошибка при получении статуса сервера\. Подробности в журнале\.")
    else:
        await msg.answer(
            text=f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}), бот работает только в *личных сообщениях*\.")


@dp.callback_query_handler(lambda _call: True)
async def handle_callbacks(_call: CallbackQuery):
    """Отлавливаем кэллбэки телеграма."""
    chat_id = _call.message.chat.id
    username = _call.from_user.username

    if _call.data == 'to_main_menu':
        await _call.message.edit_text(text='*Меню:*',
                                      reply_markup=kb.main_menu())
        await _call.answer()

    elif _call.data == 'get_lesson_time':
        await _call.message.edit_text(text=get_time_to_lesson(), reply_markup=kb.lesson_time(), )
        await _call.answer()

    elif _call.data == 'open_parameters_menu':
        await _call.message.edit_text(text='*Параметры:*',
                                      reply_markup=kb.make_settings_keyboard_for_user(chat_id))
        await _call.answer()

    elif _call.data == 'personal_settings':
        db_answer = db.get_person(user_id=_call.from_user.id)
        user_faculty = db_answer['user_faculty']
        user_course = db_answer['user_course']
        user_group = db_answer['user_group']
        answer_message = "Ваши текущие настройки:\nФакультет: *{0}*\nКурс: *{1}*\nГруппа: *{2}*".format(user_faculty,
                                                                                                        user_course,
                                                                                                        text(
                                                                                                            user_group))
        await _call.message.edit_text(text=answer_message,
                                      reply_markup=kb.personal_settings_menu(user_id=chat_id, faculty=user_faculty,
                                                                             course=user_course, group=user_group))
        await _call.answer()

    elif _call.data == 'choose_group':
        await get_group(_call.message)
        await _call.answer()

    elif _call.data == 'reload_time':
        try:
            await _call.message.edit_text(text=get_time_to_lesson(),
                                          reply_markup=kb.lesson_time())
        except MessageNotModified:
            await _call.answer(text='Не нажимайте так часто!')

    elif _call.data == 'change_faculty':
        await _call.message.edit_text(text='*Выберите факультет:*', reply_markup=kb.faculty_menu())
        await _call.answer()

    elif _call.data == 'change_course':
        await _call.answer()
        await get_course(_call.message)

    elif _call.data == 'MTS_faculty':
        db.change_faculty(chat_id, faculty='МТС')
        await _call.answer(text='Факультет выбран.')
        await get_course(_call.message)

    elif _call.data == 'MRM_faculty':
        db.change_faculty(chat_id, faculty='МРМ')
        await _call.answer(text='Факультет выбран.')
        await get_course(_call.message)

    elif _call.data == 'IVT_faculty':
        db.change_faculty(chat_id, faculty='ИВТ')
        await _call.answer(text='Факультет выбран.')
        await get_course(_call.message)

    elif _call.data == 'GF_faculty':
        db.change_faculty(chat_id, faculty='ГФ')
        await _call.answer(text='Факультет выбран.')
        await get_course(_call.message)

    elif _call.data == 'AES_faculty':
        db.change_faculty(chat_id, faculty='АЭС')
        await _call.answer(text='Факультет выбран.')
        await get_course(_call.message)

    elif _call.data == 'set_1_course':
        db.change_course(user_id=chat_id, course='1')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'set_2_course':
        db.change_course(user_id=chat_id, course='2')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'set_3_course':
        db.change_course(user_id=chat_id, course='3')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'set_4_course':
        db.change_course(user_id=chat_id, course='4')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'set_5_course':
        db.change_course(user_id=chat_id, course='5')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'set_6_course':
        db.change_course(user_id=chat_id, course='6')
        await _call.answer(text='Курс выбран.')
        await get_group(_call.message)

    elif _call.data == 'edit_format_settings':
        await _call.message.edit_text(text="*Вид расписания:*",
                                      reply_markup=kb.formatting(chat_id))
        await _call.answer()

    elif _call.data == 'change_show_teacher_status_off':
        db.change_show_teacher_status(user_id=chat_id, status=False)
        await _call.message.edit_reply_markup(reply_markup=kb.formatting(chat_id))
        await _call.answer()

    elif _call.data == 'change_show_teacher_status_on':
        db.change_show_teacher_status(user_id=chat_id, status=True)
        await _call.message.edit_reply_markup(reply_markup=kb.formatting(chat_id))
        await _call.answer()

    elif _call.data == 'change_show_audience_status_on':
        db.change_show_audience_status(user_id=chat_id, status=True)
        await _call.message.edit_reply_markup(reply_markup=kb.formatting(chat_id))
        await _call.answer()

    elif _call.data == 'change_show_audience_status_off':
        db.change_show_audience_status(user_id=chat_id, status=False)
        await _call.message.edit_reply_markup(reply_markup=kb.formatting(chat_id))
        await _call.answer()

    elif _call.data == 'delete_me':
        await _call.message.edit_text(text='Вы уверены? *Аккаунт восстановлению не подлежит\!*',
                                      reply_markup=kb.delete_me_menu())
        await _call.answer()

    elif _call.data == 'delete_me_yes':
        if db.user_exists(chat_id):
            try:
                db.delete_person(chat_id)
                await _call.message.edit_text(
                    text='Аккаунт был *удален\!*\nЧтобы заново зарегистрироваться используйте '
                         'команду /start\.')
                await event_handler.deleted_user(msg=_call)
            except Exception as e:
                await _call.message.answer(text='Ошибка\! \n %s' % e)
                error_handler.add_error_to_log(user=username, error=e)
            await _call.answer()
        else:
            await _call.message.answer(text='*Вы не зарегистрированы\!*\n'
                                            'Используйте команду /start\.')
            await _call.answer()

    elif _call.data == 'generate_admin_keyboard':
        await _call.message.edit_text(
            text='*Админ\-меню:*', reply_markup=kb.admin_menu())
        await _call.answer()

    elif _call.data == 'adminmenu_delete_string':
        msg = await _call.message.edit_text(
            text='*Введите ключ:*')
        try:
            bot.register_next_step_handler(msg, db.delete_person)
            bot.send_message(chat_id=chat_id,
                             text='Пользователь успешно удалён\!')
            await _call.message.edit_text(
                text='*Админ\-меню:*', reply_markup=kb.admin_menu())
        except Exception as e:
            bot.send_message(chat_id=chat_id,
                             text=f'Произошла непредвиденная ошибка\!\nТекст ошибки: {e}')
            error_handler.add_error_to_log(user=username, error=e)
        await _call.answer()

    elif _call.data == 'adminmenu_truncate_table':
        try:
            db.execute('TRUNCATE TABLE Users')
            bot.send_message(chat_id=chat_id,
                             text='База успешно очищена\!')
        except Exception as e:
            bot.send_message(chat_id=chat_id,
                             text=f'Произошла непредвиденная ошибка\!\nТекст ошибки: {e}')
            error_handler.add_error_to_log(user=username, error=e)
        await _call.answer()

    elif _call.data == 'get_schedule':
        await _call.message.edit_text(
            text='*Выберите пункт:*',
            reply_markup=kb.get_schedule_by_day())
        await _call.answer()

    elif _call.data == 'get_today_schedule':
        bot.send_chat_action(chat_id, action="typing")
        db_answer = db.get_person(user_id=_call.from_user.id)

        user_faculty = db_answer['user_faculty']
        user_course = db_answer['user_course']
        user_group = db_answer['user_group']
        answer_message = xls_handler.get_today_schedule(user_group=user_group, user_id=_call.from_user.id)
        answer_message = xls_handler.format_message(text=answer_message,
                                                    teacher=show_teacher,
                                                    audience=show_audience)
        try:
            await _call.message.edit_text(
                text=answer_message,
                reply_markup=kb.get_schedule_by_day())
            await _call.answer()
        except MessageNotModified:
            await _call.answer(text='Вы видите расписание на сегодняшний день!')

    elif _call.data == 'get_tomorrow_schedule':
        bot.send_chat_action(chat_id, action="typing")
        db_answer = db.get_person(user_id=_call.from_user.id)
        user_group = db_answer['user_group']
        show_teacher = db_answer['show_teacher']
        show_audience = db_answer['show_audience']
        answer_message = xls_handler.get_tomorrow_schedule(user_group)
        answer_message = xls_handler.format_message(text=answer_message,
                                                    teacher=show_teacher,
                                                    audience=show_audience)
        try:
            await _call.message.edit_text(
                text=answer_message,
                reply_markup=kb.get_schedule_by_day())
            await _call.answer()
        except MessageNotModified:
            await _call.answer(text='Вы видите расписание на завтрашний день!')

    elif _call.data == 'get_week_schedule':
        await _call.message.edit_text(text="Расписание на неделю:\n",
                                      reply_markup=kb.get_schedule_by_day())
        await _call.answer()

    elif _call.data == 'adminmenu_users_count':
        arr = db.get_user_count()
        answer_message = '__Всего пользователей:__ *%s*\n\nМТС: *%s*\nМРМ: *%s*\nИВТ: *%s*\nАЭС: *%s*\nГФ: *%s*' % (
            arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
        try:
            await _call.message.edit_text(
                text=answer_message, reply_markup=kb.admin_user_count_keyboard())
            await _call.answer()
        except MessageNotModified:
            await _call.answer(text='Изменений нет!')

    elif _call.data == 'adminmenu_schedule_updates':
        query_result = db.execute("SELECT (file_name, version) from fs")
        bot.send_message(chat_id, query_result)
        await _call.answer()

    elif _call.data == 'get_bot_statistic':
        await _call.message.edit_text(
            text='*Статистика бота*',
            reply_markup=kb.admin_statistic_menu(),
        )
        await _call.answer()

    elif _call.data == 'get_edit_db':
        await _call.message.edit_text(
            text='*Настройка базы данных*',
            reply_markup=kb.admin_edit_db_menu())
        await _call.answer()

    elif _call.data == 'execute_query':
        msg = bot.send_message(chat_id, text='Введите текст запроса:')
        bot.register_next_step_handler(msg, db_execute)
        await _call.answer()

    elif _call.data == 'additional_info':
        await _call.message.edit_text(text='*Доп\. информация*',
                                      reply_markup=kb.additional_info())
        await _call.answer()

    else:
        user_group = db.get_info(
            column='user_group', user_id=chat_id)
        if not user_group:
            db.change_group(chat_id, _call.data)
            db.change_reg_date(chat_id, str(date.today()))
            await _call.message.edit_text(text='*Меню:*', reply_markup=kb.main_menu())
            await event_handler.new_user(msg=_call)
            await _call.answer(text='Группа выбрана.')
        else:
            db.change_group(chat_id, _call.data)
            db_answer = db.get_person(user_id=_call.from_user.id)
            user_faculty = db_answer['user_faculty']
            user_course = db_answer['user_course']
            user_group = db_answer['user_group']
            answer_message = "Ваши текущие настройки:\nФакультет: *{0}*\nКурс: *{1}*\nГруппа: *{2}*".format(
                user_faculty, user_course, user_group)

            await _call.message.edit_text(
                text=answer_message.replace("-", "\-"),
                reply_markup=kb.personal_settings_menu(user_id=chat_id, faculty=user_faculty,
                                                       course=user_course, group=user_group))
            await _call.answer(text='Курс изменён.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


uvloop.install()
