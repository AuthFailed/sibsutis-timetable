# -*- coding: utf-8 -*-
from datetime import datetime
from urllib import request

import requests
from bs4 import BeautifulSoup as bs
from openpyxl import load_workbook, utils as u
from openpyxl.utils import get_column_letter

import group_list as gl

last_update = {
    "МТС1к": "",
    "МТС2к": "",
    "МТС3к": "",
    "МТС4к": "",
    "МРМ1к": "",
    "МРМ2к": "",
    "МРМ3к": "",
    "МРМ4к": "",
    "ИВТ1к": "",
    "ИВТ2к": "",
    "ИВТ3к": "",
    "ИВТ4к": "",
    "ГФ1к": "",
    "ГФ2к": "",
    "ГФ3к": "",
    "ГФ4к": "",
    "АЭС1к": "",
    "АЭС2к": "",
    "АЭС3к": "",
    "АЭС4к": "",
    "АЭС5к": "",
}


def get_xls_for_user(user_group):
    if user_group in gl.mts_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МТС", "МТС1к")
        wb = load_workbook("./schedule_files/МТС1к.xlsx")
    elif user_group in gl.mts_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МТС", "МТС2к")
        wb = load_workbook("./schedule_files/МТС2к.xlsx")
    elif user_group in gl.mts_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МТС", "МТС3к")
        wb = load_workbook("./schedule_files/МТС3к.xlsx")
    elif user_group in gl.mts_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МТС", "МТС4к")
        wb = load_workbook("./schedule_files/МТС4к.xlsx")
    elif user_group in gl.mrm_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МРМ", "МРМ1к")
        wb = load_workbook("./schedule_files/МРМ1к.xlsx")
    elif user_group in gl.mrm_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МРМ", "МРМ2к")
        wb = load_workbook("./schedule_files/МРМ2к.xlsx")
    elif user_group in gl.mrm_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МРМ", "МРМ3к")
        wb = load_workbook("./schedule_files/МРМ3к.xlsx")
    elif user_group in gl.mrm_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/МРМ", "МРМ4к")
        wb = load_workbook("./schedule_files/МРМ4к.xlsx")
    elif user_group in gl.ivt_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ИВТ", "ИВТ1к")
        wb = load_workbook("./schedule_files/ИВТ1к.xlsx")
    elif user_group in gl.ivt_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ИВТ", "ИВТ2к")
        wb = load_workbook("./schedule_files/ИВТ2к.xlsx")
    elif user_group in gl.ivt_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ИВТ", "ИВТ3к")
        wb = load_workbook("./schedule_files/ИВТ3к.xlsx")
    elif user_group in gl.ivt_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ИВТ", "ИВТ4к")
        wb = load_workbook("./schedule_files/ИВТ4к.xlsx")
    elif user_group in gl.gf_1_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ГФ", "ГФ1к")
        wb = load_workbook("./schedule_files/ГФ1к.xlsx")
    elif user_group in gl.gf_2_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ГФ", "ГФ2к")
        wb = load_workbook("./schedule_files/ГФ2к.xlsx")
    elif user_group in gl.gf_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ГФ", "ГФ3к")
        wb = load_workbook("./schedule_files/ГФ3к.xlsx")
    elif user_group in gl.gf_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/ГФ", "ГФ4к")
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
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/АЭС", "АЭС2к")
        wb = load_workbook("./schedule_files/АЭС2к.xlsx")
    elif user_group in gl.aes_3_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/АЭС", "АЭС3к")
        wb = load_workbook("./schedule_files/АЭС3к.xlsx")
    elif user_group in gl.aes_4_course:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/АЭС", "АЭС4к")
        wb = load_workbook("./schedule_files/АЭС4к.xlsx")
    else:
        update_schedule_files(
            u"https://sibsutis.ru/students/study/Расписание%20xlsx/2019(осень,до%20перелома)/АЭС", "АЭС5к")
        wb = load_workbook("./schedule_files/АЭС5к.xlsx")
    wb = wb.get_sheet_by_name("TDSheet")
    return wb


def get_today_schedule(user_group):
    today = get_weekday(datetime.weekday(datetime.now()))
    if today[2] != "Воскресенье":
        letter = ''
        message_to_send = ""
        xls = get_xls_for_user(user_group)

        for cellObj in xls["C4":"Z4"]:
            for cell in cellObj:
                if user_group == cell.value:
                    letter = get_column_letter(u.coordinate_to_tuple(cell.coordinate)[1])
                    break

        first_point = letter + str(today[0])
        second_point = letter + str(today[1])
        message_to_send += "*" + today[2] + "*\n\n"
        for cellObj in xls[first_point:second_point]:
            for cell in cellObj:
                if cell.value is not None:
                    time = xls["B%s" % cell.row].value
                    if time == "8:00:00 - 9:35:00":
                        message_to_send += "*8:00 — 9:35*\n__" + cell.value + "__\n"
                    elif time == "9:50:00 - 11:25:00":
                        message_to_send += "*9:50 — 11:25*\n__" + cell.value + "__\n"
                    elif time == "11:40:00 - 13:15:00":
                        message_to_send += "*11:40 — 13:15*\n__" + cell.value + "__\n"
                    elif time == "13:45:00 - 15:20:00":
                        message_to_send += "*13:45 — 15:20*\n__" + cell.value + "__\n"
                    elif time == "15:35:00 - 17:10:00":
                        message_to_send += "*15:35 — 17:10*\n__" + cell.value + "__\n"
                    elif time == "17:25:00 - 19:00:00":
                        message_to_send += "*17:25 — 19:00*\n__" + cell.value + "__\n"
        return message_to_send
    else:
        message_to_send = "Сегодня выходной! Отдыхай 😊"
        return message_to_send


def get_tomorrow_schedule(user_group):
    if datetime.weekday(datetime.now()) + 1 == 7:
        tomorrow = get_weekday(0)
    else:
        tomorrow = get_weekday(datetime.weekday(datetime.now()) + 1)
    if tomorrow[2] != "Воскресенье":
        letter = ""
        message_to_send = ""
        xls = get_xls_for_user(user_group)

        for cellObj in xls["C4":"Z4"]:
            for cell in cellObj:
                if user_group == cell.value:
                    letter = get_column_letter(u.coordinate_to_tuple(cell.coordinate)[1])
                    break

        first_point = letter + str(tomorrow[0])
        second_point = letter + str(tomorrow[1])
        message_to_send += "*" + tomorrow[2] + "*\n\n"
        for cellObj in xls[first_point:second_point]:
            for cell in cellObj:
                if cell.value is not None:
                    time = xls["B%s" % cell.row].value
                    if time == "8:00:00 - 9:35:00":
                        message_to_send += "*8:00 — 9:35*\n__" + cell.value + "__\n"
                    elif time == "9:50:00 - 11:25:00":
                        message_to_send += "*9:50 — 11:25*\n__" + cell.value + "__\n"
                    elif time == "11:40:00 - 13:15:00":
                        message_to_send += "*11:40 — 13:15*\n__" + cell.value + "__\n"
                    elif time == "13:45:00 - 15:20:00":
                        message_to_send += "*13:45 — 15:20*\n__" + cell.value + "__\n"
                    elif time == "15:35:00 - 17:10:00":
                        message_to_send += "*15:35 — 17:10*\n__" + cell.value + "__\n"
                    elif time == "17:25:00 - 19:00:00":
                        message_to_send += "*17:25 — 19:00*\n__" + cell.value + "__\n"
        return message_to_send
    else:
        message_to_send = "Сегодня выходной! Отдыхай 😊"
        return message_to_send


def update_schedule_files(link, group):
    url = request.urlopen(link)
    if url.getcode() == 200:
        soup = bs(url, "html.parser")
        text = soup.find("a", attrs={"class": "element-title",
                                     "data-bx-title": "%s.xlsx" % group})
        parsed_time = text["data-bx-datemodify"]
        download_link = u"https://sibsutis.ru%s" % (text["data-bx-download"])
        if last_update[group] != parsed_time:
            last_update.update({group: parsed_time})
            r = requests.get(download_link.encode('utf8'), allow_redirects=True)
            open('./schedule_files/{}.xlsx'.format(group), 'wb').write(r.content)
    else:
        print("Соединение не установлено!")


def get_weekday(date):
    tday = []
    day_of_week = ""
    first_row = ""
    second_row = ""
    if date == 0:
        first_row = "5"
        second_row = "16"
        day_of_week = "Понедельник"
    elif date == 1:
        first_row = "17"
        second_row = "28"
        day_of_week = "Вторник"
    elif date == 2:
        first_row = "29"
        second_row = "40"
        day_of_week = "Среда"
    elif date == 3:
        first_row = "41"
        second_row = "52"
        day_of_week = "Четверг"
    elif date == 4:
        first_row = "53"
        second_row = "64"
        day_of_week = "Пятница"
    elif date == 5:
        first_row = "65"
        second_row = "76"
        day_of_week = "Суббота"
    else:
        first_row = ""
        second_row = ""
        day_of_week = "Воскресенье"
    for obj in first_row, second_row, day_of_week:
        tday.append(obj)
    return tday
