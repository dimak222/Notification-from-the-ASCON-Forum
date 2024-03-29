#-------------------------------------------------------------------------------
# Author:      dimak222
#
# Created:     25.08.2022
# Copyright:   (c) dimak222 2022
# Licence:     No
#-------------------------------------------------------------------------------

title = "Уведомление с форума ASCON" # наименование приложения
ver = "v0.9.1.2" # версия файла
url = "https://github.com/dimak222/Notification-from-the-ASCON-Forum" # ссылка на файл

#------------------------------Настройки!---------------------------------------

check_update = [True, '# проверять обновление программы ("True" - да; "False" или "" - нет)']
beta = [False, '# скачивать бета версии программы ("True" - да; "False" или "" - нет)']

only_new_topics = [False, '# показывать только новые (только что созданные) темы ("True" - да; "False" или "" - нет)']

my_topics = [False, '# показывать только интересующие темы через ";" ((пример: "Макрос "Уведомления о новых сообщениях на форуме"; Компас v21; Программа сохранения в PDF"); "False" или "" - выводит новые сообщения со всех тем)']
blacklist_of_topics = [False, '# перечисление не интересующих тем через ";" ((пример: "Трубопроводы, сваренные из гнутого листа. Накладки на стыки; Электрика: мощность резистора ПЭВР-50, как она изменяется при регулировании."); "False" или "" - выводит новые сообщения со всех тем)']

first_msg = [False, '# показывать первое прочитанное сообщение (непосредственно после запуска приложения) ("True" - да; "False" или "" - нет)']

icon_in_notifications = [False, '# показывать иконку в уведомлении, ("True" - да (влезает меньше текста в уведомлении); "False" или "" - нет)']

update_msg = [[55, 100], '# частота обновления сообщений, случайное значение от n до m секунд (нижняя граница не меньше 20 сек, верхняя граница не меньше 40 сек)']
error_time = [[30, 100], '# время ожидания между ошибками, случайное значение от n до m секунд (после 10 ошибок подряд выдаёт сообщение о прекращении работы)']

#------------------------------Импорт модулей-----------------------------------

import psutil # модуль вывода запущеных процессов
import os # работа с файовой системой
from sys import exit # для выхода из приложения без ошибки

from threading import Thread # библиотека потоков
import tkinter as tk # модуль окон
import tkinter.messagebox as mb # окно с сообщением

import urllib.request # модуль открытия сайтов

import re # модуль регулярных выражений

from winotify import Notification, audio # библиотека уведомлений в Windows

import random # импорт модуля случайных чисел
import time # модуль времени

#-------------------------------------------------------------------------------

def DoubleExe(): # проверка на уже запущеное приложение

    global program_directory # значение делаем глобальным

    list = [] # список найденых названий программы

    filename = psutil.Process().name() # имя запущеного файла
    filename2 = title + ".exe" # имя запущеного файла

    if filename != "python.exe": # если программа запущена не в IDE/консоли

        for process in psutil.process_iter(): # перебор всех процессов

            try: # попытаться узнать имя процесса
                proc_name = process.name() # имя процесса

            except psutil.NoSuchProcess: # в случае ошибки
                pass # пропускаем

            else: # если есть имя
                if proc_name == filename or proc_name == filename2: # сравниваем имя
                    list.append(process.cwd()) # добавляем в список название программы
                    if len(list) > 2: # если найдено больше двух названий программы (два процесса)
                        Message("Приложение уже запущено!") # сообщение, поверх всех окон и с автоматическим закрытием
                        exit() # выходим из программы

    if list == []: # если нет найденых названий программы
        program_directory = "" # ничего не указывааем (будет рядом с программой)

    else: # если путь найден
        program_directory = os.path.dirname(psutil.Process().exe()) # директория файла

def WindowsVer(ver): # проверка версии Windows ("7;8;8.1")

    import platform # модуль информации об операционной системе
    from sys import exit # для выхода из приложения без ошибки

    ver = ver.split(";") # разделяем на ";"

    if platform.win32_ver()[0] in ver: # проверяем все вписаные версии Windows
        Message("Эта версия Windows не поддерживается!=(") # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)
        exit() # выходим из програмы

def CheckUpdate(): # проверить обновление приложение

    global url # значение делаем глобальным

    if check_update: # если проверка обновлений включена

        try: # попытаться импортировать модуль обновления

            from Updater import Updater # импортируем модуль обновления

            if "url" not in globals(): # если нет ссылки на программу
                url = "" # нет ссылки

            Updater.Update(title, ver, beta, url, Resource_path("cat.ico")) # проверяем обновление (имя программы, версия программы, скачивать бета версию, ссылка на программу, путь к иконке)

        except SystemExit: # если закончили обновление (exit в Update)
            exit() # выходим из программы

        except: # не удалось
            pass # пропустить

def Resource_path(relative_path): # для сохранения картинки внутри exe файла

    try: # попытаться определить путь к папке
        base_path = sys._MEIPASS # путь к временной папки PyInstaller

    except Exception: # если ошибка
        base_path = os.path.abspath(".") # абсолютный путь

    return os.path.join(base_path, relative_path) # объеденяем и возващаем полный путь

def Message(text = "Ошибка!", counter = 4): # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)

    def Message_Thread(text, counter): # сообщение, поверх всех окон с автоматическим закрытием (текст, время закрытия)

        if counter == 0: # время до закрытия окна (если 0)
            counter = 1 # закрытие через 1 сек
        window_msg = tk.Tk() # создание окна
        try: # попытаться использовать значёк
            window_msg.iconbitmap(default = Resource_path("cat.ico")) # значёк программы
        except: # если ошибка
            pass # пропустить
        window_msg.attributes("-topmost", True) # окно поверх всех окон
        window_msg.withdraw() # скрываем окно "невидимое"
        time = counter * 1000 # время в милисекундах
        window_msg.after(time, window_msg.destroy) # закрытие окна через n милисекунд
        if mb.showinfo(title, text, parent = window_msg) == "": # информационное окно закрытое по времени
            pass # пропустить
        else: # если не закрыто по времени
            window_msg.destroy() # окно закрыто по кнопке
        window_msg.mainloop() # отображение окна

    msg_th = Thread(target = Message_Thread, args = (text, counter)) # запуск окна в отдельном потоке
    msg_th.start() # запуск потока

    msg_th.join() # ждать завершения процесса, иначе может закрыться следующие окно

def Txt_file(): # считываем значения настроек из txt файла

    import os # работа с файовой системой

    def Text_processing(lines, Path): # обработка текста (строки текста, путь к файлу)

        global parameters # делаем глобальным список с параметрами

        def Сlearing_the_list(lines): # очистка списка строк от "#"

            lines_clean = [] # список строк с чистым текстом (без текста после "#")

            for line in lines: # для каждой строки производим обработку

                if line.isspace(): # если пустая строка пропустить
                    continue

                ignore_grid = re.findall("\".[^\"]+?#.+?\"", line) # проверка строки на содержание текста с решоткой в ковычках "***#***"

                if ignore_grid != []: # если строка содержит текст с решоткой в ковычках "***#***"

                    line = line.replace(ignore_grid[0], "Текст с решоткой в ковычках!=)", 1) # заменяем текст с решоткой в ковычках "***#***" на "|"

                    line_clean = line.split("#", 1)[0] # если в строке есть "#" не записывать всё что после неё

                    line_clean = line_clean.replace("Текст с решоткой в ковычках!=)", ignore_grid[0], 1) # заменяем "|" на текст с решоткой в ковычках "***#***"

                else: # не содержит текст с решоткой в ковычках "***#***"
                    line_clean = line.split("#", 1) # если в строке есть "#" не записывать всё что после неё

                if line_clean[0].strip() == "": # если нет записи до #, пропустиь строку
                    continue

                lines_clean.append(line_clean) # список строк с чистым текстом (без текста после "#")

            return lines_clean # возврящаем чистые строки

        if lines == []: # если в файле нет записи, вписываем в файл опции для редактирования и инструкцию по использованию
            Сreate_settings_file(Path) # создать txt файл с записью в него значений

        else: # если есть текст обратобать его

            try: # попытаться обработать значения в txt файле

                lines_clean = Сlearing_the_list(lines) # очистка списка строк от "#"

                for line in lines_clean: # для каждой строки производим обработку
                    parameter = line[0].split("=") # делим по "="
                    parameter[0] = parameter[0].strip() # убираем пробелы по бокам
                    parameter[1] = parameter[1].strip().strip('"') # убираем пробелы и "..." по бокам

                    if parameter[1].find("True") != -1: # если есть параметр со словом True, обрабатываем его
                        parameter[1] = True # присвоем значение "True"

                    elif parameter[1].find("False") != -1 or parameter[1].strip() == "": # если есть параметр со словом False или "", обрабатываем его
                        parameter[1] = False # присвоем значение "False"

                    elif parameter[1].find(";") != -1: # если есть параметр с ";", обрабатываем его
                        parameter[1] = parameter[1].split(";") # разделяем параметр по ";", создаёться список

                    try: # пытаемся добавить параметры в словарь
                        parameters[parameter[0]] = [parameter[1], line[1]] # добавляем в словарь параметры

                    except NameError: # если нет словаря создаём его и добавляем параметры
                        parameters = {} # создаём словарь с параметрами
                        parameters[parameter[0]] = [parameter[1], line[1]] # добавляем в словарь параметры

            except:
                Message("Проверте правильность записи файла: \n\"" + Path + "\"\nИли удалите его, новый будет создан автоматически.") # сообщение, поверх всех окон с автоматическим закрытием
                exit() # выходим из програмы

    def Сreate_settings_file(name_txt_file): # создать txt файл с записью в него значений

        txt_file = open(name_txt_file, "w+", encoding = "utf-8") # открываем файл записи (w+), для чтения (r), (невидимый режим)

        txt = """check_update = "True" # проверять обновление программы ("True" - да; "False" или "" - нет)
beta = "False" # скачивать бета версии программы ("True" - да; "False" или "" - нет)

only_new_topics = "False" # показывать только новые (только что созданные) темы ("True" - да; "False" или "" - нет)

my_topics = "False" # показывать только интересующие темы через ";" ((пример: "Макрос "Уведомления о новых сообщениях на форуме"; Компас v21; Программа сохранения в PDF"); "False" или "" - выводит новые сообщения со всех тем)
blacklist_of_topics = "False" # перечисление не интересующих тем через ";" ((пример: "Трубопроводы, сваренные из гнутого листа. Накладки на стыки; Электрика: мощность резистора ПЭВР-50, как она изменяется при регулировании."); "False" или "" - выводит новые сообщения со всех тем)

first_msg = "False" # показывать первое прочитанное сообщение (непосредственно после запуска приложения) ("True" - да; "False" или "" - нет)

icon_in_notifications = "False" # показывать иконку в уведомлении, ("True" - да (влезает меньше текста в уведомлении); "False" или "" - нет)

update_msg = "55; 100" # частота обновления сообщений, случайное значение от n до m секунд (нижняя граница не меньше 20 сек, верхняя граница не меньше 40 сек)
error_time = "30; 100" # время ожидания между ошибками, случайное значение от n до m секунд (после 10 ошибок подряд выдаёт сообщение о прекращении работы)
""" # текст записываемый в .txt файл

        txt_file.write(txt) # записываем текст в файл
        txt_file.close() # закрываем файл

        os.startfile(name_txt_file) # открываем файл в системе
        Message("Введите необходимые значения! \nИ запустите приложение повторно.") # сообщение с названием файла
        exit() # выходим

    name_txt_file = os.path.join(program_directory, title + ".txt") # название текстового файла

    if os.path.exists(name_txt_file): # если есть txt файл использовать его

        txt_file = open(name_txt_file, encoding = "utf-8") # открываем файл записи (w+), для чтения (r), (невидимый режим)
        lines = txt_file.readlines()  # прочитать все строки
        txt_file.close() # закрываем файл

        Text_processing(lines, name_txt_file) # обработка текста (строки текста, путь к файлу)

        Parameters() # присвоене значений прочитаных параметров

    else: # если нет файла
        Сreate_settings_file(name_txt_file) # создать txt файл с записью в него значений (путь к txt файлу)

def Parameters(): # присвоене значений прочитаных параметров

    global check_update # значение делаем глобальным
    global beta # значение делаем глобальным

    global only_new_topics # значение делаем глобальным

    global my_topics # значение делаем глобальным
    global blacklist_of_topics # значение делаем глобальным

    global first_msg # значение делаем глобальным

    global icon_in_notifications # значение делаем глобальным

    global update_msg # значение делаем глобальным
    global error_time # значение делаем глобальным

    check_update = parameters.setdefault("check_update", check_update)[0] # опция проверки обновления программы
    beta = parameters.setdefault("beta", beta)[0] # опция скачивания бета версии программы

    only_new_topics = parameters.setdefault("only_new_topics", only_new_topics)[0] # опция показывать ли только новые темы

    my_topics = parameters.setdefault("my_topics", my_topics)[0] # опция перечисления интересующих тем через
    blacklist_of_topics = parameters.setdefault("blacklist_of_topics", blacklist_of_topics)[0] # опция перечисление не интересующих тем

    first_msg = parameters.setdefault("first_msg", first_msg)[0] # опция показывать ли первое прочитанное сообщение

    icon_in_notifications = parameters.setdefault("icon_in_notifications", icon_in_notifications)[0] # опция показывать ли иконку в уведомлении

    update_msg = parameters.setdefault("update_msg", update_msg)[0] # опция частоты обновления сообщений
    error_time = parameters.setdefault("error_time", error_time)[0] # опция времени ожидания между ошибками

    for parameter, val in parameters.items(): # для каждой строки производим обработку
        print(f"{parameter} = {val[0]}") # выводим прочитание параметры

def ASCON(): # уведомление от ASCONa

    def site_processing(site): # обработка сайта

        response = urllib.request.urlopen(site) # открываем сайт
        html = response.read().decode("utf-8") # считываем с него значения
        response.close() # закрываем модуль

        return html # возвращаем считаные строки сайта

    def notification_message(mask, html): # поиск и вывод значений из html (маска поиска, текст где искать)

        z = 0 # номер поиска сообщения

        text = re.findall(mask, html)[z] # ищем название темы

        return text # возвращаем найденые значения

    html = site_processing("https://forum.ascon.ru/index.php?action=recent") # обработка сайта

    topic = notification_message("rel=\"nofollow\" title=\"(.+)\"", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    autor = notification_message("Последний ответ от <.+>\<a.+\"\>(.+)\<\/a\>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    msg = notification_message("<div class=\"list_posts\">(.+)<\/div>", html) # поиск и вывод значений из html (маска поиска, текст где искать)
    launch = notification_message("\/ <a href=\"(.+)\" rel=\"nofollow\"", html) # поиск и вывод пути к теме сообщения из html (маска поиска, текст где искать)

    topic = topic.split("Re: ") # делим текст темы на "Re: "

    if len(topic) > 1: # если поделилось, используем 2-ю часть
        if only_new_topics == False: # если выключена опция только новые темы
            topic = topic[1] # 2-я часть списка
            Message_processing(topic, autor, msg, launch) # обработка сообщения (тема, автор, сообщение, ссылка на сообщение)

    else: # не делилось на "Re: "
        topic = "🆕 " + topic[0] # к началу темы добавляем значёк "🆕"
        Message_processing(topic, autor, msg, launch) # обработка сообщения (тема, автор, сообщение, ссылка на сообщение)

def Message_processing(topic, autor, msg, launch): # обработка сообщения (тема, автор, сообщение, ссылка на сообщение)

    global ASCON_message # значение делаем глобальным

    def blacklist_of_topic(topic): # проверка на не интересующие темы (название темы)

        if blacklist_of_topics != False: # если введены не интересующие темы и не пусто

            if type(blacklist_of_topics) == list: # если значение параметра список, обработать каждое значение

                for blacklist_of_topic in blacklist_of_topics: # для каждой темы производим обработку
                    blacklist_of_topic = blacklist_of_topic.strip() # убираем пробелы по бокам
                    if blacklist_of_topic == topic: # если не интересующая тема и новая темы совпали
                        print("Не интересующая тема:", blacklist_of_topic)
                        return False # выводим False (не продолжаем обработку текста)

                return True # выводим True (продолжаем обработку текста)

            else: # не список

                blacklist_of_topic = blacklist_of_topics.strip() # убираем пробелы по бокам
                if blacklist_of_topic == topic: # если не интересующая тема и новая темы совпали
                    print("Не интересующая тема:", blacklist_of_topic)
                    return False # выводим False (не продолжаем обработку текста)

                else: # темы не совпали
                    return True # выводим True (продолжаем обработку текста)

        else: # не введены не интересующие темы
            return True # выводим True (продолжаем обработку текста)

    def my_topic(topic): # проверка на интересующие темы (название темы)

        if my_topics != False: # если введены интересующие темы

            if type(my_topics) == list: # если значение параметра список, обработать каждое значение

                for my_topic in my_topics: # для каждой темы производим обработку
                    my_topic = my_topic.strip() # убираем пробелы по бокам
                    if my_topic == topic: # если интересующая тема и новая темы совпали
                        print("Интересующая тема:", my_topic)
                        return True # выводим True (продолжаем обработку текста)

                return False # выводим False (не продолжаем обработку текста)

            else: # не список

                my_topic = my_topics.strip() # убираем пробелы по бокам
                if my_topic == topic: # если интересующая тема и новая темы совпали
                    print("Интересующая тема:", my_topic)
                    return True # выводим True (продолжаем обработку текста)

                else: # темы не совпали
                    return False # выводим False (не продолжаем обработку текста)

        else: # не введены интересующие темы
            return True # выводим True (продолжаем обработку текста)

    def dictionary_processing(text): # обработка текста по словарю

        dictionary = {r"&nbsp;":" ", # словарь замен
            r"&quot;":"\"",
            r"&amp;":"&",
            r"\<blockquote class=[^\>]+\>":'\n"',
            r"\<br\>\</blockquote\>":'"\n',
            r"</blockquote\>":'"\n',
            r"</a></cite>" : " ",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/smiley.gif\" alt=\"&#58;&#41;\" title=\"Smiley\" class=\"smiley\">":"😄",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/wink.gif\" alt=\";&#41;\" title=\"Wink\" class=\"smiley\">":"😉",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shocked.gif\" alt=\"&#58;o\" title=\"Shocked\" class=\"smiley\">":"😱",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/sad.gif\" alt=\"&#58;&#40;\" title=\"Sad\" class=\"smiley\">":"😔",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/blink.gif\" alt=\"8-&#41;\" title=\"\" class=\"smiley\">":"😉",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/cry.gif\" alt=\"&#58;`&#40;\" title=\"Cry\" class=\"smiley\">":"😭",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/mad.gif\" alt=\"&gt;&#58;&#40;\" title=\"Mad\" class=\"smiley\">":"🤬",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/shuffle.gif\" alt=\"&#58;shu&#58;\" title=\"Shuffle\" class=\"smiley\">":"=/",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/angel.gif\" alt=\"&#58;angel&#58;\" title=\"angel\" class=\"smiley\">":"😇",
            r"<img src=\"https://forum.ascon.ru/Smileys/fugue/rolleyes.gif\" alt=\"&#58;&#58;&#41;\" title=\"Roll Eyes\" class=\"smiley\">":"🙄",
            r"<br>":"\n",
            r"(<[^>]+?>)":"",
            r"&gt;":">",
            r"&#39;": "'"}

        for key in dictionary: # обрабатываем каждую замену из словаря
            text = re.sub(key, dictionary[key], text) # меняем найденые значения

        return text

    if blacklist_of_topic(topic): # проверка на не интересующие темы (название темы)

        if my_topic(topic): # проверка на интересующие темы (название темы)

            topic = dictionary_processing(topic) # обработка текста по словарю
            topic = re.sub("\"", "''", topic) # меняем " => '' т.к. не выдаёт сообщение если в заголовке "

            msg = dictionary_processing(msg) # обработка текста по словарю

            if ASCON_message == "": # если нет сообщения присвоить ему текст

                if first_msg: # показывать первое прочитанное сообщение (непосредственно после запуска приложения, актуально при параметре my_topics = "False")
                    print("Первое сообщение!")
                    print(topic + "\nОт " + autor + ":\n" + msg)
                    Windows_msg("Первое уведомление с форума ASCON", topic, "От " + autor + ": " + msg, "short", "", launch) # сообщение Windows (наименование уведомления, заголовок, сообщение, длительность отображения, путь к иконке, ссылка при нажатии уведомления)

                ASCON_message = msg # прочитанное сообщение

            else: # попытаться сравнить предыдущее сообщение

                if msg != ASCON_message:
                    print(topic + "\nОт " + autor + ":\n" + msg)
                    Windows_msg(title, topic, "От " + autor + ": " + msg, "short", "", launch) # сообщение Windows (наименование уведомления, заголовок, сообщение, длительность отображения, путь к иконке, ссылка при нажатии уведомления)
                    ASCON_message = msg # прочитанное сообщение

                else:
                    print("Новых сообщений нет!")

        else: # нет интересующих тем

            ASCON_message = msg # прочитанное сообщение
            print("Нет интересующих тем!")

    else: # тема в чёрном списке

        ASCON_message = msg # прочитанное сообщение
        print("Тема в чёрном списке!")

def Windows_msg_New(Name_app = "Уведомление", title = "Заголовок", msg = "Сообщение", duration = "short", icon = "", on_click = ""): # сообщение Windows (наименование уведомления, заголовок, сообщение, длительность отображения, путь к иконке, ссылка при нажатии уведомления)

##    from win11toast import toast # библиотека уведомлений в Windows

    if icon_in_notifications: # показывать иконку в уведомлении
        if icon == "": # если путь к иконки не задан
            icon = "cat.ico" # использовать рядом расположеную иконку

    icon = {"src": Resource_path(icon), # иконка
    "placement": "appLogoOverride"} # форма иконки

    toast(title, # заголовок
          msg, # сообщение
          app_id = Name_app, # название программы
          icon = icon, # полный путь к иконке
          duration = duration, # время отображения ("short" или "long")
          dialogue = "", # озвучка сообщения
          audio = "ms-winsoundevent:Notification.SMS", # звук сообщения
          on_click = on_click, # что открывать при нажатии на уведомление
          ) # что открывать при нажатии на уведомление

def Windows_msg(Name_app = "Уведомление", title = "Заголовок", msg = "Сообщение", duration = "short", icon = "", launch = ""): # сообщение Windows (наименование уведомления, заголовок, сообщение, длительность отображения, полный путь к иконки, ссылка при нажатии уведомления)

    if icon_in_notifications: # показывать иконку в уведомлении
        if icon == "": # если путь к иконки не задан
            icon = "cat.ico" # использовать рядом расположеную иконку

    toast = Notification(app_id = Name_app, # название программы
                         title = title, # заголовок
                         msg = msg, # сообщение
                         duration = duration, # время отображения ("short" или "long")
                         icon = Resource_path(icon), # полный путь к иконке
                         launch = launch) # что открывать при нажатии на уведомление

    toast.set_audio(audio.Default, loop = False) # звук сообщения

##    toast.add_actions(label = "Ссылка", launch = "https://github.com/versa-syahptr/winotify/") # кнопка в сообщении

    toast.show() # запустить

def Sleep(update_msg): # остановка на случайное число от n до m секунд

    n = int(update_msg[0]) # число n
    m = int(update_msg[1]) # число m

    if n < 20: # если нижний порог меньше 20 сек присвоить ему 20 сек (что бы не DDosить)
        n = 20 # 20 сек нижний порог

    if m < 40: # если верхний порог меньше 40 сек присвоить ему 40 сек (что бы не DDosить)
        m = 40 # 40 сек верхний порог

    if n > m: # если первое число больше второго сравнять их
        n = m # приравниваем значения

    randomN = random.randint(n, m) # случайное целое число от n до m

    time.sleep(randomN) # остановка на n секунд

def Error(e = "Ошибка!"): # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)

    from sys import exit # для выхода из приложения без ошибки

    global err # счётчик ошибок (для чтения вне функции)

    print("Ошибка" , err, ":", e)

    if err <= 10: # если ошибок меньше задонного числа

        err += 1 # добавляем значение к счётчику ошибок

        try: # попытаться сделать паузу
            Sleep(update_msg) # остановка на случайное от n до m секунд

        except:
            Message("Проверте правильность записи параметра: " + "error_time" + "\"\nИли удалите файл, новый будет создан автоматически.", 8) # сообщение, поверх всех окон и с автоматическим закрытием
            exit() # выходим из програмы

    else:
        Windows_msg(Name_app = "Уведомление с форума ASCON", title = "Отслеживание сообщений прекращено!", msg = "Последняя ошибка: " + "\"" + str(e) + "\"", duration = "short", icon = "", launch = "") # сообщение Windows (наименование уведомления, заголовок, сообщение, длительность отображения, полный путь к иконки, ссылка при нажатии уведомления)
        exit() # выходим из програмы

#-------------------------------------------------------------------------------

ASCON_message = "" # первое сообщение для сравнения
err = 0 # счётчик ошибок

DoubleExe() # проверка на уже запущеное приложение

Message("Приложение запущено!") # сообщение, поверх всех окон и с автоматическим закрытием

WindowsVer("7;8;8.1") # проверка версии Windows ("7;8;8.1")

Txt_file() # считываем значения из txt файла

CheckUpdate() # проверить обновление приложение

while 1: # цикл обработки сообщений

    try: # попытаться выполнить программу

        ASCON() # уведомление от ASCONa

        Sleep(update_msg) # остановка на случайное число от n до m секунд

        err = 0 # сбрасываем счётчик ошибок

    except Exception as e: # ловим любые ошибки

        Error(e) # в случае ошибки пытаеться 10 повторить выполнение программы (имя ошибки)