# -*- coding: utf-8 -*-
import re
from datetime import datetime, date
from urllib import request

import pytz
import requests
from bs4 import BeautifulSoup as Soup
from openpyxl import load_workbook, utils as u
from openpyxl.utils import get_column_letter

import group_list as gl
from main import db
global number_of_lessons


def get_xls_for_user(user_group):
    """Выбрать/скачать файл для определённой группы."""
    if user_group in gl.mts_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A2%D0%A1", "МТС1к")
        wb = load_workbook("./schedule_files/МТС1к.xlsx")
    elif user_group in gl.mts_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A2%D0%A1", "МТС2к")
        wb = load_workbook("./schedule_files/МТС2к.xlsx")
    elif user_group in gl.mts_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A2%D0%A1", "МТС3к")
        wb = load_workbook("./schedule_files/МТС3к.xlsx")
    elif user_group in gl.mts_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A2%D0%A1", "МТС4к")
        wb = load_workbook("./schedule_files/МТС4к.xlsx")
    elif user_group in gl.mrm_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A0%D0%9C", "МРМ1к")
        wb = load_workbook("./schedule_files/МРМ1к.xlsx")
    elif user_group in gl.mrm_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A0%D0%9C", "МРМ2к")
        wb = load_workbook("./schedule_files/МРМ2к.xlsx")
    elif user_group in gl.mrm_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A0%D0%9C", "МРМ3к")
        wb = load_workbook("./schedule_files/МРМ3к.xlsx")
    elif user_group in gl.mrm_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%9C%D0%A0%D0%9C", "МРМ4к")
        wb = load_workbook("./schedule_files/МРМ4к.xlsx")
    elif user_group in gl.ivt_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%98%D0%92%D0%A2", "ИВТ1к")
        wb = load_workbook("./schedule_files/ИВТ1к.xlsx")
    elif user_group in gl.ivt_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%98%D0%92%D0%A2", "ИВТ2к")
        wb = load_workbook("./schedule_files/ИВТ2к.xlsx")
    elif user_group in gl.ivt_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%98%D0%92%D0%A2", "ИВТ3к")
        wb = load_workbook("./schedule_files/ИВТ3к.xlsx")
    elif user_group in gl.ivt_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%98%D0%92%D0%A2", "ИВТ4к")
        wb = load_workbook("./schedule_files/ИВТ4к.xlsx")
    elif user_group in gl.gf_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%93%D0%A4", "ГФ1к")
        wb = load_workbook("./schedule_files/ГФ1к.xlsx")
    elif user_group in gl.gf_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%93%D0%A4", "ГФ2к")
        wb = load_workbook("./schedule_files/ГФ2к.xlsx")
    elif user_group in gl.gf_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%93%D0%A4", "ГФ3к")
        wb = load_workbook("./schedule_files/ГФ3к.xlsx")
    elif user_group in gl.gf_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            u"/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            u"%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%93%D0%A4", "ГФ4к")
        wb = load_workbook("./schedule_files/ГФ4к.xlsx")
    elif user_group in gl.aes_1_course:
        update_schedule_files(
            "https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            "/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            "%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%90%D0%AD%D0%A1",
            "АЭС1к")
        wb = load_workbook("./schedule_files/АЭС1к.xlsx")
    elif user_group in gl.aes_2_course:
        update_schedule_files(
            "https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            "/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            "%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%90%D0%AD%D0%A1",
            "АЭС2к")
        wb = load_workbook("./schedule_files/АЭС2к.xlsx")
    elif user_group in gl.aes_3_course:
        update_schedule_files(
            "https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            "/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            "%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%90%D0%AD%D0%A1",
            "АЭС3к")
        wb = load_workbook("./schedule_files/АЭС3к.xlsx")
    elif user_group in gl.aes_4_course:
        update_schedule_files(
            "https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            "/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            "%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%90%D0%AD%D0%A1",
            "АЭС4к")
        wb = load_workbook("./schedule_files/АЭС4к.xlsx")
    else:
        update_schedule_files(
            "https://sibsutis.ru/students/study/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20xlsx"
            "/2019(%D0%BE%D1%81%D0%B5%D0%BD%D1%8C,"
            "%D0%B4%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BB%D0%BE%D0%BC%D0%B0)/%D0%90%D0%AD%D0%A1",
            "АЭС5к")
        wb = load_workbook("./schedule_files/АЭС5к.xlsx")
    wb = wb.get_sheet_by_name("TDSheet")
    return wb


def get_today_schedule(user_group):
    """Получить сегодняшнее расписание."""
    info = []
    message_to_send = ""
    today = get_weekday(datetime.weekday(datetime.now(pytz.timezone('Asia/Bangkok'))))
    if today[1] != "Воскресенье":
        letter = ''
        num_of_lessons = 0

        xls = get_xls_for_user(user_group)

        for cellobj in xls["C4":"Z4"]:
            for cell in cellobj:
                if user_group == cell.value:
                    letter = get_column_letter(u.coordinate_to_tuple(cell.coordinate)[1])
                    break
        message_to_send += "*" + today[1]
        for i in range(0, len(today[0])):
            point = letter + str(today[0][i])
            if type(xls[point]).__name__ == "MergedCell":
                point = xls[point].column + str(xls[point].row - 1)
            if xls[point].value is not None:
                time = xls["B%s" % (int(xls[point].row))].value
                info = work_with_time(time=time, cell=xls[point].value)[:]
                message_to_send += info[0]
                num_of_lessons += 1
        if len(info):
            if info[1] is not 0:
                message_to_send = format_message(message_to_send)
                message_to_send += "\nСегодня *{0}* пар(ы). Последняя пара кончается в *{1}*.".format(num_of_lessons,
                                                                                                      info[1][11:-3])
            else:
                message_to_send += "\n\nСегодня выходной! Отдыхай 😊"
        else:
            message_to_send += "\n\nСегодня выходной! Отдыхай 😊"
    else:
        message_to_send += "*Воскресенье*\n\nСегодня выходной! Отдыхай 😊"
    return message_to_send


def get_tomorrow_schedule(user_group):
    """Получить завтрашнее расписание."""
    info = []
    num_of_lessons = 0
    if datetime.weekday(datetime.now().astimezone(pytz.timezone('Asia/Bangkok'))) + 1 == 7:
        tomorrow = get_weekday(0)
    else:
        tomorrow = get_weekday(datetime.weekday(datetime.now().astimezone(pytz.timezone('Asia/Bangkok'))) + 1)
    if tomorrow[1] != "Воскресенье":
        letter = ""
        message_to_send = ""

        xls = get_xls_for_user(user_group)

        for cellobj in xls["C4":"Z4"]:
            for cell in cellobj:
                if user_group == cell.value:
                    letter = get_column_letter(u.coordinate_to_tuple(cell.coordinate)[1])
                    break

        message_to_send += "*" + tomorrow[1] + "*\n\n"
        for i in range(0, len(tomorrow[0])):
            point = letter + str(tomorrow[0][i])
            if type(xls[point]).__name__ == "MergedCell":
                point = xls[point].column + str(xls[point].row - 1)
            if xls[point].value is not None:
                time = xls["B%s" % (int(xls[point].row))].value
                info = work_with_time(time=time, cell=xls[point].value)[:]
                message_to_send += info[0]
                num_of_lessons += 1
            message_to_send = format_message(message_to_send)
            if len(info):
                message_to_send += "\n\nЗавтра *{0}* пар(ы). Последняя пара кончается в *{1}*.".format(num_of_lessons,
                                                                                                       info[1][11:-3]
                                                                                                       )
        else:
            message_to_send += "\n\nЗавтра выходной! Отдыхай 😊"
        return message_to_send
    else:
        message_to_send = "*Воскресенье*\n\nЗавтра выходной! Отдыхай 😊"
        return message_to_send


def work_with_time(time, cell):
    print(time, cell)
    message_to_send = ''
    last_lesson_time = ''
    if time == "8:00:00 - 9:35:00":
        message_to_send += "*8:00 — 9:35*\n" + cell + "\n"
        last_lesson_time = time
    elif time == "9:50:00 - 11:25:00":
        message_to_send += "*9:50 — 11:25*\n" + cell + "\n"
        last_lesson_time = time
    elif time == "11:40:00 - 13:15:00":
        message_to_send += "*11:40 — 13:15*\n" + cell + "\n"
        last_lesson_time = time
    elif time == "13:45:00 - 15:20:00":
        message_to_send += "*13:45 — 15:20*\n" + cell + "\n"
        last_lesson_time = time
    elif time == "15:35:00 - 17:10:00":
        message_to_send += "*15:35 — 17:10*\n" + cell + "\n"
        last_lesson_time = time
    elif time == "17:25:00 - 19:00:00":
        message_to_send += "*17:25 — 19:00*\n" + cell + "\n"
        last_lesson_time = time
    arr = [message_to_send, last_lesson_time]
    return arr


def format_message(text, teacher=True, audience=True):
    """Форматируем сообщение перед отправкой."""
    text = text.replace("(Лекционные занятия)", "`(Лекция)`") \
        .replace("(Лабораторные работы)", "`(Лабораторная)`") \
        .replace("(Практические занятия)", "`(Практика)`") \
        .replace("(Занятия по ин.язу)", "`(Занятия по ин.язу)`") \
        .replace("(Занятия по физической культуре)", "`(Занятия по физической культуре)`")
    return personal_format_msg(show_teacher=teacher, show_audience=audience, text=text)


# TODO исправить работу форматирования текста
def personal_format_msg(text, show_teacher, show_audience):
    """Дополнительное форматирование сообщения в зависимости от настроек пользователя."""
    if show_audience and show_teacher:
        return text
    elif show_audience is False and show_teacher:
        result = re.findall(r"а\.(.*?)\)", text)
        for r in range(0, len(result)):
            text = text.replace(result[r], "")
    elif show_teacher is False and show_audience:
        result = re.findall(r"\)`\n(.*)", text)
        for r in range(0, len(result)):
            text = text.replace(result[r], "")
    elif show_audience is False and show_teacher is False:
        result = re.findall(r"\)`\n(.*)", text)
        for r in result:
            text = text.replace(result[r], "")
        result = re.findall(r"а\.(.*?)\)", text)
        for r in result:
            text = text.replace(result[r], "")
    return text


def update_schedule_files(link, group):
    """Обновление устаревших файлов расписания."""
    url = request.urlopen(link)
    if url.getcode() == 200:
        soup = Soup(url, "html.parser")
        text = soup.find("a", attrs={"class": "element-title",
                                     "data-bx-title": "%s.xlsx" % group})
        parsed_time = text["data-bx-datemodify"]
        download_link = u"https://sibsutis.ru%s" % (text["data-bx-download"])
        if db.execute(query="SELECT update_time from fs WHERE file_name=%s" % group) != parsed_time:
            db.update_time(file_name=group, time=parsed_time)
            r = requests.get(download_link.encode('utf8'), allow_redirects=True)
            open('./schedule_files/{}.xlsx'.format(group), 'wb').write(r.content)
    else:
        raise Exception("Соединение не установлено")


def get_weekday(current_date):
    """Узнаём день недели."""
    tday = []
    if is_week_even():
        if current_date == 0:
            rows = ["5", "7", "9", "11", "13", "15"]
            day_of_week = "Понедельник"
        elif current_date == 1:
            rows = ["17", "19", "21", "23", "25", "27"]
            day_of_week = "Вторник"
        elif current_date == 2:
            rows = ["29", "31", "33", "35", "37", "39"]
            day_of_week = "Среда"
        elif current_date == 3:
            rows = ["41", "43", "45", "47", "49", "51"]
            day_of_week = "Четверг"
        elif current_date == 4:
            rows = ["53", "55", "57", "59", "61", "63"]
            day_of_week = "Пятница"
        elif current_date == 5:
            rows = ["65", "67", "69", "71", "73", "75"]
            day_of_week = "Суббота"
        else:
            rows = []
            day_of_week = "Воскресенье"
    else:
        if current_date == 0:
            rows = ["6", "8", "10", "12", "14", "16"]
            day_of_week = "Понедельник"
        elif current_date == 1:
            rows = ["18", "20", "22", "24", "26", "28"]
            day_of_week = "Вторник"
        elif current_date == 2:
            rows = ["30", "32", "34", "36", "38", "40"]
            day_of_week = "Среда"
        elif current_date == 3:
            rows = ["42", "44", "46", "48", "50", "52"]
            day_of_week = "Четверг"
        elif current_date == 4:
            rows = ["54", "56", "58", "60", "62", "64"]
            day_of_week = "Пятница"
        elif current_date == 5:
            rows = ["66", "68", "70", "72", "74", "76"]
            day_of_week = "Суббота"
        else:
            rows = []
            day_of_week = "Воскресенье"
    for obj in rows, day_of_week:
        tday.append(obj)
    return tday


def get_week_from_date(date_object):
    """Получае номер учебной недели."""
    date_ordinal = date_object.toordinal()
    year = date_object.year
    week = ((date_ordinal - _week1_start_ordinal(year)) // 7) + 1
    if week >= 52 and date_ordinal > + _week1_start_ordinal(year + 1):
        year += 1
        week = 1
    return week - 34


def _week1_start_ordinal(year):
    """Устанавливаем начало года на 1 января."""
    jan1 = date(year, 1, 1)
    jan1_ordinal = jan1.toordinal()
    jan1_weekday = jan1.weekday()
    week1_start_ordinal = jan1_ordinal - ((jan1_weekday + 1) % 7)
    return week1_start_ordinal


def is_week_even():
    """Проверка недели на чётность."""
    if get_week_from_date(datetime.now()) % 2 != 0:
        return False
    else:
        return True
