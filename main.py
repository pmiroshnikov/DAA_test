# Приложение ежедневник с применением методик Глеба Архангельского.
# Назначение: планирование задач на день, неделю.

# Импорт необходимых библиотек
import tkinter as tk
import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import pickle
import tkinter.font
import locale
import tkcalendar
import webbrowser

locale.setlocale(category=locale.LC_TIME, locale="Russian")  # Устанавливаем время на Русском языке

# глобальные переменные, необходимые для работы
window_title="DiaryArkhApp"
period_dict = {  # Словарь с содержанием вкладок
    "День": [],
    "Неделя": [],
    "Стратегическая картонка": [],
    "О программе": []
}  # ****************Словарь с содержанием вкладок

frame_tab_dict = {}  # словарь для хранения названий фрэймов табов окон

day_header_list = ['С привязкой ко времени', 'Гибкие задачи'] # список с заголовками типов задач на день

time_code_visual_dict = {}  # словарь для хранения виджетов приложения (чек-боксов, лэйблов тайм-кодов, полей ввода текстов)
time_code_tasks_dict = {}  # Словарь для хранения данных о задачах на день (для записи в файл и загрузки)
date_dict = {}  # Словарь для хранения дней-словарей по ключу дата

week_goals_visual_dict = {} # Словарь для хранения визуализаторов недельного планирования по ключу квадранта (по умолчанию каждая из задач - пустой список)
week_goals_visual_dict['1']=[]
week_goals_visual_dict['2']=[]
week_goals_visual_dict['3']=[]
week_goals_visual_dict['4']=[]
week_goals_dict = {} # Словарь для хранения задач недельного планирования по ключу квадранта (по умолчанию каждая из задач - пустой список)
week_goals_dict['1']=[]
week_goals_dict['2']=[]
week_goals_dict['3']=[]
week_goals_dict['4']=[]

princip_goal_visual_list = [] # Список для хранения лэйблов стратегической картонки
princip_goal_list = [] # Список для хранения данных стратегической картонки (для записи в файл)
day_string = ''  # строка для хранения даты и дня недели
#*************************************************

# имена индексов внутренних списков основных словарей
cbi_TT_i = 0  # для НЕПОСРЕДСТВЕННО индекса чек-бокса с привязкой ко времени
tc_cb_i = 1  # для чек-бокса с привязкой ко времени
tc_l_i = 2  # для лэйбла маркировки времени
TT_t_ent_i = 3  # для поля ввода задач с привязкой ко времени
t_ent_i = 4  # для поля ввода задач без привязки ко времени
cbi_nTT_i = 5  # для НЕПОСРЕДСТВЕННО индекса чек-бокса без привязки ко времени
ntc_cb_i = 6  # для чек-бокса без привязки ко времени
TT_tsk_txt_i = 7  # для переменной изменения текста
data_sl_TT_t_i = 0  # для сохранения/загрузки задач с привязкой ко времени
data_sl_t_i = 1  # для сохранения/загрузки задач без привязки ко времени
data_cb_i_TT_t_i = 2  # для сохранения/загрузки индекса чек-бокса для задач с привязкой ко времени
data_cb_i_t_i = 3  # для сохранения/загрузки индекса чек-бокса для задач без привязки ко времени

number_of_strat_goals = 10
# **********************************************************************************************

# Размеры областей вкладок и подписи
window_geometry='1000x900'
tab_width = 1000 # ширина рабочего окна
tab_height = 850 # высота рабочего окна
strat_place_x0=50 # Левый верхний угол **
strat_place_y0=50 # **стратегической картонки
week_canvas_x0=30 # Левый верхний угол **
week_canvas_y0=150 #** недельного планирования
week_canvas_width=750 # Параметры поля отрисовки**
week_canvas_height=650 # **квадрантов планирования недели
task_entry_width = 40 # стандартная ширина полей ввода
about_width = 130 # ширина листинга "о программе"
#*************************************************

# Тексты для используемых в программе лэйблов
tab_descr_lbl_prefix = "Планируем на "  # Лэйбл для краткого пояснения сути вкладок
strat_board_title = "Введите и добавьте свои основные жизненные принципы и соответствующие им глобальные цели"
week_label_text = "Запишите свои цели на неделю, распределив их по четырём квадрантам: \n I - Важные и Срочные \n II - Важные и Несрочные \n III - Неважные и Срочные \n IV - Неважные и Несрочные"
about_label_text_1 = "Данная программа представляет собой электронную версию ежедневника по мотивам методов Глеба Алексеевича Архангельского. \n "
about_label_text_2 = "Официальный сайт: https://glebarhangelsky.ru"
about_label_link = "https://glebarhangelsky.ru"
about_label_text_3 = "Планируйте свой день: \n  -в левой части записывайте задачи с жёсткой привязкой ко времени; \n  -справа вносите гибкие задачи; \n  -вычёркивайте выполненные задачи с помощью чек-боксов; \n  -переносите гибкие невыполненные задачи на следующий день; \n  -выносите наверх ваше самое важное дело дня; \n  -'съеште лягушку' - запишите на следующий день и незамедлительно выполните мелкое, но неприятное дело; \n  -'режьте слона на бифштексы' - разделите крупную задачу на несколько маленьких и выполните в день одну маленькую часть."
about_label_text_4 = "Составьте план на неделю: \n  -продумайте задачи, которые предстоит выполнить на грядущей неделе; \n  -запишите их, разделив на четыре квадранта по принципу: СРОЧНЫЕ/ВАЖНЫЕ, НЕСРОЧНЫЕ/ВАЖНЫЕ, СРОЧНЫЕ/НЕВАЖНЫЕ, НЕСРОЧНЫЕ/НЕВАЖНЫЕ; \n  -действуйте во втором квадранте, - старайтесь отдавать предпочтения делам ВАЖНЫМ."
about_label_text_5 = "Заполните стратегическую картонку: \n  -подумайте о своих базовых жизненных принципах и главных вещах; \n  -запишите несколько из них (от 5 до 10); \n  -в соответствии с каждым принципа запишите долгосрочную цель и стремитесь к её выполнению."
#*************************************************

# ВременнЫе переменные для работы
START_TIME = timedelta(hours=8)  # Время, с которого начинается планирование дня
END_TIME = timedelta(hours=20)  # Время, когда когда заканчивается планирование дня
TIME_DELTA = timedelta(minutes=30)  # Промежуток между временнЫми участками планирования
#***************************************************************************************

# Для виджетов отображения времени
HALF_AN_HOUR = 1800 # полчаса в секундах
number_of_time_rows = int((END_TIME.seconds - START_TIME.seconds) / HALF_AN_HOUR)  # Количество рядов для отражения временных интервалов
CHECKBOX_COLUMN = 0 # Номер столбца чекбоксов привязки ко времени
START_TIME_GRID_ROW = 5  # Ряд, с которого начинаются интервалы планирования времени
START_TIME_GRID_COLUMN = 1  # Столбец, с которого начинаются интервалы планирования времени
TT_TASK_GRID_COLUMN = 2  # Столбец, с которого начинаются задачи с привязкой ко времени
TASK_GRID_COLUMN = 3  # Столбец, с которого начинаются задачи с без временЫх привязок
TYPICAL_PADX = 5  # Систематический отступ по горизонтали
TYPICAL_PADY = 0  # Систематический отступ по вертикали
BUTTON_WIDTH = 10  # Ширина кнопок
START_PROGRAMM_FLAG = True  # индикатор начала работы программы
#***************************************************************************************

# Цвета оформления:
time_code_txt_color = 'Black' # основной цвет текста
time_code_txt_color_TT = "#DC143C" # цет текста задач с привязкой ко временеи
header_txt_color = '#0000FF' # текст заголовков
strat_color_1 = '#0000FF' # Тексты стратегической картонки
strat_color_2 = '#EFA208' # картонки
week_urgent_color="#E8A1A1" #** Квадранты
week_urgent_unimportant_color="#84CDF7"# матрицы
week_important_color="#FABB63"                 #Кови
week_other_color="#B2F5AC"                         # недельного планирования
about_bg_color='White' # фон листинга "О программе"
week_canvas_bg='White' # фон квадрантов матрицы Кови
#***************************************************************************************

# шрифты оформления:
standard_font = "TkDefaultFont" # стандартный шрифт
font_size_typical = 9 # стандартный размер шрифта
#***************************************************************************************

# файлы для сохранения и загрузки:
file_for_day = 'tasks_data.txt' # для хранения данных о планировки на день
file_for_strat_board = 'strat_data.txt' # для хранения данных для стратегической картонки
file_for_week = 'week_data.txt' # для хранения данных о планировки на неделю
#***************************************************************************************
#***************************************************************************************
# КОНЕЦ - глобальные переменные, необходимые для работы
#***************************************************************************************
#***************************************************************************************

# Класс для работы с диалоговым окном календаря*************
class CalendarDialog(tkinter.simpledialog.Dialog):
    # Запуск диалогового окна выбора даты
    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()
        self.result = self.result.strftime("%d.%m.%Y %A") # возврат в формате "день.месяц.год день недели"
# *************************************************

# Используемые в работе функции:

# Открытие ссылки в окне About **********
def arkh_url(event):
    webbrowser.open_new(about_label_link)
#****************************************


# Функция - обработчик записи целей на неделю по кнопке
def on_record_week_goal():
    global week_goals_visual_dict
    global week_goals_dict

    quad_flag=quad_var.get() # получаем флажок-номер квадранта , в который будет производиться запись
    week_goal_text = week_task_txt.get() # получаем текст из поля для записи
    goal_label = Label(master=frame_tab_dict["Неделя"], text=week_goal_text)  # оформляем пустой лэйбл для целей
    # проверяем флажок и выбираем точку, в которую будет размещена цель
    if quad_flag==1:
        goal_X=10 * TYPICAL_PADX
        goal_Y=35 * TYPICAL_PADX + len(week_goals_dict[str(quad_flag)])*TYPICAL_PADX*5

    if quad_flag==2:
        goal_X=85 * TYPICAL_PADX
        goal_Y=35 * TYPICAL_PADX + len(week_goals_dict[str(quad_flag)])*TYPICAL_PADX*5

    if quad_flag==3:
        goal_X=10 * TYPICAL_PADX
        goal_Y=100 * TYPICAL_PADX + len(week_goals_dict[str(quad_flag)])*TYPICAL_PADX*5

    if quad_flag==4:
        goal_X=85 * TYPICAL_PADX
        goal_Y=100 * TYPICAL_PADX + len(week_goals_dict[str(quad_flag)])*TYPICAL_PADX*5

    week_goals_visual_dict[str(quad_flag)].append(goal_label) # добавляем лэйбл с задачей на неделю  в словарь с визуализаторами недели
    week_goals_visual_dict[str(quad_flag)][len(week_goals_visual_dict[str(quad_flag)])-1].place(x=goal_X, y=goal_Y) # и располагаем этот лэйбл на экране

    week_goals_dict[str(quad_flag)].append([week_goal_text, goal_X, goal_Y]) # в словарь хранения задач добавляем текст задачи и координаты для вывода на экран

    with open(file_for_week, 'wb') as file_to_save:  # Открываем файл для записи в него целей на неделю
        pickle.dump(week_goals_dict, file_to_save)  # Запись словаря в файл
    file_to_save.close()  # Закрываем файл после чтения
# КОНЕЦ - Функция - обработчик записи целей на неделю по кнопке


# Функция - загрузка из файла записей с целями на неделю при открытии вкладки "неделя"
def on_load_week_goals():
    global week_goals_visual_dict
    global week_goals_dict

    try:
        with open(file_for_week, 'rb') as file_to_load:  # открываем файл для загрузки
            week_goals_dict = pickle.load(file_to_load)  # загружаем список из файла
        file_to_load.close()  # Закрываем файл после чтения
    except IOError:
        return

    for quad_key in week_goals_dict: # проходим по словарю квадрантов
        for goal_index in range(len(week_goals_dict[quad_key])): # проходим по списку целей и заполняем переменные для визуализатора
            week_goal_text = week_goals_dict[quad_key][goal_index][0]
            goal_X = week_goals_dict[quad_key][goal_index][1]
            goal_Y = week_goals_dict[quad_key][goal_index][2]

            goal_label = Label(master=frame_tab_dict["Неделя"], text=week_goal_text)  # оформляем лэйбл для целей
            week_goals_visual_dict[quad_key].append(goal_label) # записываем в словарь-визуализатор
            week_goals_visual_dict[quad_key][goal_index].place(x=goal_X, y=goal_Y) # и размещаем лэйбл на экран

# КОНЕЦ - Функция - загрузка из файла записей с целями на неделю при открытии вкладки "неделя"


# Функция - обработчик очистка целей на неделю
def on_clean_week_goals():
    global week_goals_visual_dict
    global week_goals_dict

    for quad_key in week_goals_dict: # проходим по квадранта, удаляем текст из лэйблов, удаляем сами лэйблы
        for goal_index in range(len(week_goals_dict[quad_key])):
            week_goals_visual_dict[quad_key][goal_index].place_forget()
        week_goals_dict[quad_key].clear()
        week_goals_visual_dict[quad_key].clear()

    with open(file_for_week, 'wb') as file_to_save:  # Открываем файл для записи в него "целей" на неделю после очистки
        pickle.dump(week_goals_dict, file_to_save)  # Запись словаря в файл
    file_to_save.close()  # Закрываем файл после чтения
# КОНЕЦ - Функция - обработчик очистка целей на неделю


# Функция - обработчик записи принципов и глобальных целей по кнопке в стратегическую картонку
def on_record_goal():
    global princip_goal_visual_list
    global princip_goal_list
    goal_number=1
    while princip_goal_visual_list[goal_number-1][0]['text']!='': # Находим первый пустой лэйбл
        goal_number+=1

    princip_goal_visual_list[goal_number-1][0]['text'] = str(goal_number)+'. '+principle_txt.get() # Заносим на лэйблы информацию
    princip_goal_visual_list[goal_number-1][1]['text'] = str(goal_number)+'. '+goal_txt.get()      # из полей принципов и глобальных целей

    princip_goal_list.append([princip_goal_visual_list[goal_number-1][0]['text'], princip_goal_visual_list[goal_number - 1][1]['text']])


    with open(file_for_strat_board, 'wb') as file_to_save:  # Открываем файл для записи в него списка с принципами и целями
        pickle.dump(princip_goal_list, file_to_save)  # Запись словаря в файл
    file_to_save.close()  # Закрываем файл после чтения
# КОНЕЦ - Функция - обработчик записи принципов и глобальных целей по кнопке в стратегическую картонку


# Функция - обработчик загрузки принципов и глобальных целей по кнопке в стратегическую картонку
def on_load_goals():
    global princip_goal_visual_list
    global princip_goal_list
    try:
        with open(file_for_strat_board, 'rb') as file_to_load:  # открываем файл для загрузки
            princip_goal_list = pickle.load(file_to_load)  # загружаем список из файла
        file_to_load.close()  # Закрываем файл после чтения
    except IOError:
        return
    goal_index=0
    while goal_index < int(len(princip_goal_list)):
        princip_goal_visual_list[goal_index][0]['text'] = princip_goal_list[goal_index][0]
        princip_goal_visual_list[goal_index][1]['text'] = princip_goal_list[goal_index][1]
        goal_index+=1
# КОНЕЦ - Функция - обработчик загрузки принципов и глобальных целей по кнопке в стратегическую картонку


# Функция очистки полей стратегической картонки
def on_clean_goals():
    goal_number = 0
    while princip_goal_visual_list[goal_number][0]['text'] != '':
        princip_goal_visual_list[goal_number][0]['text']=''
        princip_goal_visual_list[goal_number][1]['text']=''
        princip_goal_list[goal_number][0] = ''
        princip_goal_list[goal_number][1] = ''
        goal_number+=1
    with open(file_for_strat_board, 'wb') as file_to_save:  # Открываем файл для записи в него "целей" стратегической картонки после очистки
        pickle.dump(princip_goal_list, file_to_save)  # Запись списка в файл
    file_to_save.close()  # Закрываем файл после чтения
# КОНЕЦ - Функция очистки полей стратегической картонки


# Функция - обработчик выбора конкретной даты для просмотра заданий
def on_load_date_click():
    global date_in_use_str
    cd = CalendarDialog(window) # вызов диалогового окна с календарём
    date_in_use_str = cd.result # вызов функции класса
    current_date_label.configure(text=date_in_use_str) # запись в лэйбл-индикатор рассматриваемой даты
    on_clean_fields()  # очистка полей
    on_load_tasks()  # загрузка полей
# КОНЕЦ - Функция - обработчик выбора конкретной даты для просмотра заданий


# Функция подкраски тайм-кодов при наличии задач с привязкой ко времени
def TT_tasks_color_change():
    for time_code_key in time_code_visual_dict:  # Проходим по словарю с виджетами и смотрим, были ли изменения в полях временнЫх задач
        if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня": # У "лягушек", "слонов" и "дела дня" одно поле для ввода, поэтому они обрабатываются отдельно
            if time_code_visual_dict[time_code_key][TT_tsk_txt_i].get() != '':  # если поле временнОй задачи заполнено, подкрашиваем тайм-код
                time_code_visual_dict[time_code_key][tc_l_i]['fg'] = time_code_txt_color_TT
            if time_code_visual_dict[time_code_key][TT_tsk_txt_i].get() == '':  # если поле временнОй задачи пусто, оставляем стандартную подкраску тайм-кода
                time_code_visual_dict[time_code_key][tc_l_i]['fg'] = time_code_txt_color
# КОНЕЦ - Функция подкраски тайм-кодов при наличии задач с привязкой ко времени


# Функция, которая реагирует на изменение в чекбоксах и перекрашивает лэйблы времени в красный, если стоит галочка
def time_code_check_box_onClick():
    for time_code_key in time_code_visual_dict:  # проходим по словарю, где хранятся индексы чек-боксов, сами чек-боксы, тайм-код лэйблы, поля ввода задач
        if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня": # У "лягушек", "слонов" и "дела дня" одно поле для ввода, поэтому они обрабатываются отдельно
            time_flag = time_code_visual_dict[time_code_key][cbi_TT_i].get()  # смотрим наличие галочки в чек-боксе
            if time_flag == True:  # Проверяем флажок и зачёркиваем в текстовом поле выполненную задачу, если флажок есть
                overstrike_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=True)
                time_code_visual_dict[time_code_key][TT_t_ent_i].configure(font=overstrike_font)
            else:
                normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
                time_code_visual_dict[time_code_key][TT_t_ent_i].configure(font=normal_font)
# КОНЕЦ - Функция, которая реагирует на изменение в чекбоксах и перекрашивает лэйблы времени в красный, если стоит галочка


# Функция, которая реагирует на изменение в чекбоксах с правой стороны и перечёркивает задачу в поле ввода при отметке о выполнении
def not_time_code_check_box_onClick():
    for time_code_key in time_code_visual_dict:  # проходим по словарю, где хранятся индексы чек-боксов, сами чек-боксы, тайм-код лэйблы, поля ввода задач
        if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня": # У "лягушек", "слонов" и "дела дня" одно поле для ввода, поэтому они обрабатываются отдельно
            time_flag = time_code_visual_dict[time_code_key][cbi_nTT_i].get()  # смотрим наличие галочки в чек-боксе
            if time_flag == True:  # Проверяем флажок и меняем, при необходимости, зачёркиваем задачу, если флажок есть
                overstrike_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=True)
                time_code_visual_dict[time_code_key][t_ent_i].configure(font=overstrike_font)
            else:
                normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
                time_code_visual_dict[time_code_key][t_ent_i].configure(font=normal_font)
# КОНЕЦ - Функция, которая реагирует на изменение в чекбоксах с правой стороны и перечёркивает задачу в поле ввода при отметке о выполнении


# Функция переноса задач на следующий день
def on_reschedule():
    global date_dict
    global date_in_use
    global date_in_use_str
    date_to_reschedule = date_in_use + timedelta(days=1) # переходим на дату, последующую текущей отображаемой
    date_to_reschedule_str = get_day_string(date_to_reschedule) # переводим дату в строку

    if date_in_use_str in date_dict: # Если есть планы на текущую дату,
        if date_dict[date_in_use_str]!='': # не пусто
            # Если на последующую дату нет никаких записей, создаём для неё пустой словарь
            if date_to_reschedule_str not in date_dict:
                date_dict[date_to_reschedule_str] = {}
                for temp_time_code in date_dict[date_in_use_str]:
                    if temp_time_code != "Дело дня" and temp_time_code != "Лягушка" and temp_time_code != "Слон":
                        date_dict[date_to_reschedule_str][temp_time_code] = ['', '', False, False] # по тайм-коду заполняем пустые строчки задач и непомеченные галочки о выполнении
                    else:
                        date_dict[date_to_reschedule_str][temp_time_code]=''

            for time_code_key in date_dict[date_in_use_str]: # проходим по всем тайм-кодам текущей даты
                # Выбираем задачи без привязки ко времени, которые ещё не зачёркнуты
                if time_code_key!="Дело дня" and time_code_key!="Лягушка" and time_code_key!="Слон" and date_dict[date_in_use_str][time_code_key][data_sl_t_i]!='' and date_dict[date_in_use_str][time_code_key][data_cb_i_t_i]!=True:
                    # Если нет такой же задачи на следующий день, делаем перенос в соответствующий тайм-код
                    time_code_reschedule_key=time_code_key
                    if date_dict[date_in_use_str][time_code_key][data_sl_t_i] not in date_dict[date_to_reschedule_str][time_code_key][data_sl_t_i]:
                        # Если по текущему тайм-коду есть запись, смотрим ближайшее пустое поле для перезаписи
                        if date_dict[date_to_reschedule_str][time_code_key][data_sl_t_i]!='':
                            time_code_keys_list = list(date_dict[date_to_reschedule_str].keys()) # Формируем список ключей тайм-кодов

                            for key_index in range(len(time_code_keys_list)): # перебираем список тайм-кодов
                                if time_code_keys_list[key_index] == time_code_key: # как только наткнулись на текущий, (в котором есть запись)
                                    while date_dict[date_to_reschedule_str][time_code_keys_list[key_index]][data_sl_t_i]!='': # пробегаемся по тайм-кодам даты для переноса, ища первую пустую запись без привязки ко времени
                                        key_index+=1
                                        if key_index>=len(time_code_keys_list): # если в конце списка пустых полей не нашлось,
                                            key_index=3                         # переходим на начало
                                        time_code_reschedule_key = time_code_keys_list[key_index] # фиксируем первый попавшийся тайм-код с пустой записью
                                    break

                        date_dict[date_to_reschedule_str][time_code_reschedule_key][data_sl_t_i]=date_dict[date_in_use_str][time_code_key][data_sl_t_i] # Перенос задачи с выбранного дня на следующий

    on_save_to_file() # после переноса сохраняем изменения в файл
#КОНЕЦ - Функция переноса задач на следующий день


# Фунция записи в файл материалов страницы планирования дня:
def on_save_to_file():
    global date_dict
    day_key = date_in_use_str

    time_code_dict_local_temp = {}  # создаём промежуточный пустой словарь для последующей записи в основной словарь с данными
    for time_code_key in time_code_visual_dict:  # проходим по словарю таймкодов для выцепления задач из полей ввода и их записи в собственный словарь задач
        tasks_list_local_temp = []  # создаём промежуточный пустой список для задач для последующей записи в основной словарь с данными
        if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня":  # обрабатываем основные тайм-коды
            tasks_list_local_temp.append(time_code_visual_dict[time_code_key][TT_t_ent_i].get())  # добавляем в словарь временнУю задачу
            tasks_list_local_temp.append(time_code_visual_dict[time_code_key][t_ent_i].get())  # добавляем в словарь простую задачу
            tasks_list_local_temp.append(time_code_visual_dict[time_code_key][cbi_TT_i].get())  # добавляем в словарь индексы чекбокса для хранения информации о выполненных задачах
            tasks_list_local_temp.append(time_code_visual_dict[time_code_key][cbi_nTT_i].get())  # добавляем в словарь индексы чекбокса для хранения информации о выполненных задачах
            time_code_dict_local_temp[time_code_key] = tasks_list_local_temp
        else:  # обрабатываем поля "Слон", "Лягушка", "Дело дня"
            time_code_dict_local_temp[time_code_key] = time_code_visual_dict[time_code_key][cbi_TT_i].get()
    # заполняем словарь для хранения по ключу дата (содержимое - словари-дни)
    date_dict[day_key] = time_code_dict_local_temp

    with open(file_for_day, 'wb') as file_to_save:  # Открываем файл для записи в него словаря с задачами
        pickle.dump(date_dict, file_to_save)  # Запись словаря в файл
    file_to_save.close()  # Закрываем файл после чтения
# КОНЕЦ - Фунция записи в файл материалов страницы


# Функция загрузки задач из файла
def on_load_tasks():
    global date_dict
    global date_in_use_str
    try:
        with open(file_for_day, 'rb') as file_to_load:  # открываем файл для загрузки
            date_dict = pickle.load(file_to_load)  # загружаем словарь из файла
    except IOError:
        return

    file_to_load.close()  # Закрываем файл после чтения
    date_key = date_in_use_str

    if date_key in date_dict:  # если дата есть в сохранённом словаре в виде ключа, то будем прогружать информацию из него
        for time_code_key in time_code_visual_dict:  # проходим по словарю с виджетами для загрузки задач из словаря-хранилища данных в поля ввода
            if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня":  # обрабатываем основные тайм-коды
                time_code_visual_dict[time_code_key][cbi_TT_i].set(date_dict[date_key][time_code_key][data_cb_i_TT_t_i])  # загружаем индексы для чек-боксов временнЫх задач
                time_code_visual_dict[time_code_key][cbi_nTT_i].set(date_dict[date_key][time_code_key][data_cb_i_t_i])  # загружаем индексы для чек-боксов остальных задач
                time_code_visual_dict[time_code_key][TT_t_ent_i].insert(0, date_dict[date_key][time_code_key][data_sl_TT_t_i])  # загружаем в поля ввода данные временнЫх задач
                time_code_visual_dict[time_code_key][t_ent_i].insert(0, date_dict[date_key][time_code_key][data_sl_t_i])  # загружаем в поля ввода данные остальных задач
                time_code_check_box_onClick()  # прогружаем чек-боксы для оформления зачёркиваний
                not_time_code_check_box_onClick()  # прогружаем чек-боксы для оформления зачёркиваний
            else:  # Визуализируем "Дело дня", "Лягушку", "Слона"
                time_code_visual_dict[time_code_key][cbi_TT_i].insert(0, date_dict[date_key][time_code_key])
    if date_key not in date_dict:  # если даты нет в сохранённом словаре, просто очищаем поля визуализатора:
        on_clean_fields()
# КОНЕЦ - Функция загрузки задач из файла


# Функция очистки полей от текста
def on_clean_fields():
    for time_code_key in time_code_visual_dict:  # проходим по словарю, где хранятся индексы чек-боксов, сами чек-боксы, тайм-код лэйблы, поля ввода задач
        if time_code_key != "Слон" and time_code_key != "Лягушка" and time_code_key != "Дело дня":
            time_code_visual_dict[time_code_key][TT_t_ent_i].delete(0, tk.END)
            time_code_visual_dict[time_code_key][t_ent_i].delete(0, tk.END)
            time_code_visual_dict[time_code_key][cbi_TT_i].set(False)
            time_code_visual_dict[time_code_key][cbi_nTT_i].set(False)
        else:
            time_code_visual_dict["Дело дня"][cbi_TT_i].delete(0, tk.END)
            time_code_visual_dict["Лягушка"][cbi_TT_i].delete(0, tk.END)
            time_code_visual_dict["Слон"][cbi_TT_i].delete(0, tk.END)
# КОНЕЦ - Функция очистки полей от текста


# Функция закрытия приложения
def on_exit():
    window.destroy()
# КОНЕЦ - Функция закрытия приложения


# Функция обработчик кнопки прокрутки на следующую дату
def on_change_tomorrow():
    global date_in_use
    global date_in_use_str
    date_in_use = date_in_use + timedelta(days=1)  # получаем завтрашнюю дату
    date_in_use_str = get_day_string(date_in_use)  # Дату в строчку
    current_date_label.configure(text=date_in_use_str)
    on_clean_fields()  # очистка полей
    on_load_tasks()  # загрузка полей
# КОНЕЦ - Функция обработчик кнопки прокрутки на следующую дату


# Функция обработчик кнопки прокрутки на предыдущую дату
def on_change_yesterday():
    global date_in_use
    global date_in_use_str
    date_in_use = date_in_use - timedelta(days=1)  # получаем вчерашнюю дату
    date_in_use_str = get_day_string(date_in_use)  # Дату в строчку
    current_date_label.configure(text=date_in_use_str)
    on_clean_fields()  # очистка полей
    on_load_tasks()  # загрузка полей
# КОНЕЦ - Функция обработчик кнопки прокрутки на предыдущую дату


# Функция обработчик кнопки перехода на сегодняшнюю дату
def on_change_today():
    global date_in_use
    global date_in_use_str
    date_in_use = datetime.now()  # получаем текущую дату
    date_in_use_str = get_day_string(date_in_use)  # Дату в строчку
    current_date_label.configure(text=date_in_use_str)
    on_clean_fields()  # очистка полей
    on_load_tasks()  # загрузка полей
# КОНЕЦ - Функция обработчик кнопки перехода на сегодняшнюю дату


# Функция по получению и возвращению отформатированной строки "ДАТА+ДЕНЬ НЕДЕЛИ"
def get_day_string(datetime_to_process):
    string_to_return = datetime_to_process.strftime(
        "%d.%m.%Y %A")  # Записываем строку с датой и днём недели в нужном формате
    return string_to_return
# КОНЕЦ -Функция по получению и возвращению отформатированной строки "ДАТА+ДЕНЬ НЕДЕЛИ"


# КОНЕЦ - Используемые в работе функции

# Переключение между окнами день/неделя/месяц/"стратегическая картонка" осуществляется через вкладки в приложении
# задаём параметры окна приложения
window = tk.Tk()
window.title(window_title)
window.geometry(window_geometry)
window.resizable(width=False, height=False)
# окно создано


# Создание вкладок-разделов приложения
period_tabs = ttk.Notebook(master=window, width=tab_width, height=tab_height, padding=10)  # создаём вкладки
for tab_title in period_dict:  # Проходим по словарю названия вкладок
    frame_tab = Frame(master=period_tabs)  # Предварительно создаём фрэйм для каждого таба
    period_tabs.add(frame_tab, text=tab_title, underline=0, sticky=tk.NE + tk.SW)  # Оформление вкладок (табов)
    frame_tab_dict[tab_title] = frame_tab  # Заполняем словарь с названием фрэймов

    # Заполнение вкладки "День"
    if tab_title == "День":
        if START_PROGRAMM_FLAG == True:  # если программа только запущена, выбираем дату текущая
            START_PROGRAMM_FLAG = False  # Программа запущена
            global date_in_use
            date_in_use = datetime.now()  # получаем текущую дату
            date_in_use_str = get_day_string(date_in_use)  # форматируем дату в строку

        current_date_label = Label(master=frame_tab_dict["День"], text=date_in_use_str, width=18)  # оформляем лэйбл с датой и днём недели
        current_date_label.grid(row=START_TIME_GRID_ROW - 3, column=START_TIME_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.SW)

        # Кнопки переключения дней
        tomorrow_btn = tk.Button(master=frame_tab_dict["День"], text="\N{BLACK RIGHT-POINTING TRIANGLE}", command=on_change_tomorrow)
        yesterday_btn = tk.Button(master=frame_tab_dict["День"], text="\N{BLACK LEFT-POINTING TRIANGLE}", command=on_change_yesterday)
        today_btn = tk.Button(master=frame_tab_dict["День"], text="На сегодня", command=on_change_today)
        tomorrow_btn.grid(row=START_TIME_GRID_ROW - 2, column=START_TIME_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.E)
        yesterday_btn.grid(row=START_TIME_GRID_ROW - 2, column=START_TIME_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.W)
        today_btn.grid(row=START_TIME_GRID_ROW - 2, column=START_TIME_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY)

        # Оформляем "Дело дня"
        exclamation_img = PhotoImage(file='exclamation_point1.gif')  # загружаем картинки и оформляем лэйбл с картинкой
        important_task_label = Label(master=frame_tab_dict["День"],  image=exclamation_img)
        important_task_entry = Entry(master=frame_tab_dict["День"], width=task_entry_width)  # создаём поле ввода задачи
        important_task_label.grid(row=START_TIME_GRID_ROW - 4, column=START_TIME_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.E)
        important_task_entry.grid(row=START_TIME_GRID_ROW - 4, column=START_TIME_GRID_COLUMN + 2, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
        normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
        important_task_entry.configure(font=normal_font)
        time_code_visual_dict["Дело дня"] = [important_task_entry]  # Добавляем в словарь для визуализации "Дело дня"
        # Оформляем "Лягушку"
        frog_img = PhotoImage(file='frog1.gif')  # загружаем картинку
        frog_label = Label(master=frame_tab_dict["День"], image=frog_img)  # оформляем лэйбл с картинкой
        frog_entry = Entry(master=frame_tab_dict["День"], width=task_entry_width)  # создаём поле ввода задачи
        normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
        frog_entry.configure(font=normal_font)
        time_code_visual_dict["Лягушка"] = [frog_entry]  # Добавляем в словарь для визуализации "лягушку"
        # располагаем картинку и поле ввода
        frog_label.grid(row=START_TIME_GRID_ROW - 3, column=START_TIME_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.E)
        frog_entry.grid(row=START_TIME_GRID_ROW - 3, column=START_TIME_GRID_COLUMN + 2, padx=TYPICAL_PADX, pady=TYPICAL_PADY)

        # Оформляем "Слона на бифштексы"
        elephant_img = PhotoImage(file='elephant1.gif')  # загружаем картинку
        elephant_label = Label(master=frame_tab_dict["День"], image=elephant_img)  # оформляем лэйбл с картинкой
        elephant_entry = Entry(master=frame_tab_dict["День"], width=task_entry_width)  # создаём поле ввода задачи
        normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
        elephant_entry.configure(font=normal_font)
        time_code_visual_dict["Слон"] = [elephant_entry]  # Добавляем в словарь для визуализации "слона"
        # располагаем картинку и поле ввода
        elephant_label.grid(row=START_TIME_GRID_ROW - 2, column=START_TIME_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY, sticky=tk.E)
        elephant_entry.grid(row=START_TIME_GRID_ROW - 2, column=START_TIME_GRID_COLUMN + 2, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
        # Заголовки временнОй сетки
        task_header_lbl_lft = Label(master=frame_tab_dict["День"], text=day_header_list[0], foreground=header_txt_color)
        task_header_lbl_rht = Label(master=frame_tab_dict["День"], text=day_header_list[1], foreground=header_txt_color)
        task_header_lbl_lft.grid(row=START_TIME_GRID_ROW - 1, column=START_TIME_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
        task_header_lbl_rht.grid(row=START_TIME_GRID_ROW - 1, column=START_TIME_GRID_COLUMN + 2, padx=TYPICAL_PADX, pady=TYPICAL_PADY)

        # Расписываем временнУю сетку с разметкой во вкладке "День"
        time_to_show = START_TIME  # задаём начальное время для отображения
        row_to_reflect = START_TIME_GRID_ROW  # выбираем ряд для старта

        for time_row_ind in range(number_of_time_rows + 1):  # проходим по всем рядам и размещаем объекты в рядах

            time_to_show_string = str(time_to_show)[:-3]  # то, что будет выводиться в качестве времени

            # Создаём чек-боксы для пометки задач, привязанных ко времени
            check_box_index = BooleanVar()
            check_box_index.set(0)
            time_code_check_box = Checkbutton(
                master=frame_tab_dict["День"],
                text="выполнено", variable=check_box_index,
                onvalue=True, offvalue=False,
                command=time_code_check_box_onClick
            )

            # Создаём чек-боксы для пометки задач, без привязки ко времени
            check_box_index_not_TT = BooleanVar()
            check_box_index_not_TT.set(0)
            not_time_code_check_box = Checkbutton(
                master=frame_tab_dict["День"],
                text="выполнено", variable=check_box_index_not_TT,
                onvalue=True, offvalue=False,
                command=not_time_code_check_box_onClick
            )

            time_code_lbl = Label(master=frame_tab_dict["День"], text=time_to_show_string,
                                  foreground=time_code_txt_color)  # тайм-коды в формате "ЧАС:МИНУТЫ"
            # Создаём поля для ввода задач, привязанных ко времени
            TT_task_txt = StringVar()
            TT_task_entry = Entry(master=frame_tab_dict["День"], width=task_entry_width, textvariable=TT_task_txt)
            # Реакция на изменение в текстовом поле
            TT_task_txt.trace("w", lambda name, index, mode, TT_task_txt=TT_task_txt: TT_tasks_color_change())
            normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
            TT_task_entry.configure(font=normal_font)
            # Создаём поля для ввода важных задач, без привязки ко времени
            task_entry = Entry(master=frame_tab_dict["День"], width=task_entry_width)
            normal_font = tkinter.font.Font(family=standard_font, size=font_size_typical, overstrike=False)
            task_entry.configure(font=normal_font)

            # **************************************************************************************************************************************************************
            # !!! Заносим в словарь тайм-кодов флажок чек-бокса, чек-бокс, лэйбл, поля ввода задач********************************
            time_code_visual_dict[time_to_show_string] = [check_box_index, time_code_check_box, time_code_lbl,
                                                          TT_task_entry, task_entry, check_box_index_not_TT,
                                                          not_time_code_check_box, TT_task_txt]
            # **Основной словарь программы заполнен!*******************************************************************************
            # **************************************************************************************************************************************************************

            time_to_show += TIME_DELTA  # переходим на следующий временной интервал
            # Располагаем в "сетке окна" чек-боксы, лэйбл с тайм-кодами, поля вводов
            time_code_check_box.grid(row=row_to_reflect, column=CHECKBOX_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
            time_code_lbl.grid(row=row_to_reflect, column=START_TIME_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
            TT_task_entry.grid(row=row_to_reflect, column=TT_TASK_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
            task_entry.grid(row=row_to_reflect, column=TASK_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY)
            not_time_code_check_box.grid(row=row_to_reflect, column=TASK_GRID_COLUMN + 1, padx=TYPICAL_PADX,
                                         pady=TYPICAL_PADY)

            row_to_reflect += 1  # Следующий ряд

        # Кнопки записи, загрузки, очистки и выхода (создаём и располагаем в "сетке окна")
        save_btn = tk.Button(master=frame_tab_dict["День"], text="Сохранить", width=BUTTON_WIDTH,
                             command=on_save_to_file)
        save_btn.grid(row=START_TIME_GRID_ROW - 4, column=TASK_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY,
                      sticky=tk.E)
        load_btn = tk.Button(master=frame_tab_dict["День"], text="Другой день", width=BUTTON_WIDTH,
                             command=on_load_date_click)
        load_btn.grid(row=START_TIME_GRID_ROW - 3, column=TASK_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY,
                      sticky=tk.E)
        clean_btn = tk.Button(master=frame_tab_dict["День"], text="Очистить", width=BUTTON_WIDTH,
                              command=on_clean_fields)
        clean_btn.grid(row=START_TIME_GRID_ROW - 2, column=TASK_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY,
                       sticky=tk.E)
        exit_btn = tk.Button(master=frame_tab_dict["День"], text="Выход", width=BUTTON_WIDTH, command=on_exit)
        exit_btn.grid(row=START_TIME_GRID_ROW - 1, column=TASK_GRID_COLUMN + 1, padx=TYPICAL_PADX, pady=TYPICAL_PADY,
                      sticky=tk.E)
        reschedule_btn = tk.Button(master=frame_tab_dict["День"], text="Перенести невыполненные на следующий день", width=4*BUTTON_WIDTH, command=on_reschedule)
        reschedule_btn.grid(row=row_to_reflect, column=TASK_GRID_COLUMN, padx=TYPICAL_PADX, pady=TYPICAL_PADY,
                      sticky=tk.E)
        # ***************************************************************************************************************
        on_load_tasks()  # грузим из файла задачи, поставленные на текущий день
    # КОНЕЦ - Расписываем временнУю сетку с разметкой во вкладке "День"

    # Окно "Стратегическая картонка"*****************************************************************************************
    #************************************************************************************************************************
    if tab_title == "Стратегическая картонка":
        title_label = Label(master=frame_tab_dict["Стратегическая картонка"], text=strat_board_title, )  # оформляем лэйбл с датой и днём недели
        title_label.place(x=10, y=10)

        save_btn = tk.Button(master=frame_tab_dict["Стратегическая картонка"], text="Добавить ценность и цель",
                             command=on_record_goal)
        save_btn.place(x=strat_place_x0, y=strat_place_y0)
        clean_btn = tk.Button(master=frame_tab_dict["Стратегическая картонка"], text="Очистить картонку",
                             command=on_clean_goals)
        clean_btn.place(x= 4*strat_place_x0+10*TYPICAL_PADX, y=strat_place_y0)
        exit_btn = tk.Button(master=frame_tab_dict["Стратегическая картонка"], text="Выход",
                             command=on_exit)
        exit_btn.place(x=6 * strat_place_x0+22*TYPICAL_PADX, y=strat_place_y0)

        principle_label_header = Label(master=frame_tab_dict["Стратегическая картонка"], text="Жизненные ценности", )  # оформляем лэйбл с датой и днём недели
        principle_label_header.place(x=strat_place_x0, y=2*strat_place_y0)

        goal_label_header = Label(master=frame_tab_dict["Стратегическая картонка"], text="Глобальные цели", )  # оформляем лэйбл с датой и днём недели
        goal_label_header.place(x=7*strat_place_x0, y=2 * strat_place_y0)

        principle_txt = StringVar()
        principle_entry = Entry(master=frame_tab_dict["Стратегическая картонка"], width=task_entry_width, textvariable=principle_txt)
        principle_entry.place(x=strat_place_x0, y=3*strat_place_y0)

        goal_txt = StringVar()
        goal_entry = Entry(master=frame_tab_dict["Стратегическая картонка"], width=task_entry_width*2, textvariable=goal_txt)
        goal_entry.place(x=7*strat_place_x0, y=3*strat_place_y0)
        goal_label_row=4

        goals_font = tkinter.font.Font(family=standard_font, size=font_size_typical+2, overstrike=False)

        for goal_number in range(number_of_strat_goals):

            principle_label = Label(master=frame_tab_dict["Стратегическая картонка"], text="", )  # оформляем пустой лэйбл для принципов
            principle_label.configure(font=goals_font, fg=strat_color_1)
            principle_label.place(x=strat_place_x0, y=4*strat_place_y0+goal_number*50)

            goal_label = Label(master=frame_tab_dict["Стратегическая картонка"], text="", )  # оформляем пустой лэйбл для целей
            goal_label.configure(font=goals_font, fg=strat_color_2)
            goal_label.place(x=7*strat_place_x0, y=4*strat_place_y0+goal_number*50)

            princip_goal_visual_list.append([principle_label, goal_label])

        on_load_goals() # после прорисовки загружаем из файла цеености и цели, если они уже записаны
    # КОНЕЦ - Окно "Стратегическая картонка"
    # ************************************************************************************************************************
    # Окно "неделя"
    if tab_title == "Неделя":
        # Добавляем кнопки записи задач, очистки квадрантов и выхода из программы
        save_btn = tk.Button(master=frame_tab_dict["Неделя"], text="Добавить задачу", command=on_record_week_goal)
        save_btn.place(x=week_canvas_x0, y=week_canvas_y0/10)
        clean_btn = tk.Button(master=frame_tab_dict["Неделя"], text="Стереть задачи", command=on_clean_week_goals)
        clean_btn.place(x=week_canvas_x0 + 25 * TYPICAL_PADX, y=week_canvas_y0/10)
        exit_btn = tk.Button(master=frame_tab_dict["Неделя"], text="Выход", command=on_exit)
        exit_btn.place(x=week_canvas_x0 + 50 * TYPICAL_PADX, y=week_canvas_y0/10)

        week_label_header = Label(master=frame_tab_dict["Неделя"],text=week_label_text, justify=LEFT)  # оформляем лэйбл с пояснением к работе
        week_label_header.place(x=week_canvas_x0, y=10*TYPICAL_PADX)

        # Рисуем поле для прорисовке квадрантов Матрицы Кови и сами квадранты
        canvas = Canvas(master=frame_tab_dict["Неделя"], width=week_canvas_width, height=week_canvas_height, bg=week_canvas_bg)
        canvas.place (x=week_canvas_x0, y=week_canvas_y0)

        canvas.create_rectangle(TYPICAL_PADX, TYPICAL_PADX , week_canvas_width/2-TYPICAL_PADX, week_canvas_height/2, fill=week_urgent_color, outline=time_code_txt_color)
        canvas.create_text(2*TYPICAL_PADX, 3*TYPICAL_PADX, text="I", font="Verdana 13", justify=LEFT, fill=time_code_txt_color)
        canvas.create_rectangle(TYPICAL_PADX, week_canvas_height/2+TYPICAL_PADX , week_canvas_width/2-TYPICAL_PADX, week_canvas_height-TYPICAL_PADX, fill=week_urgent_unimportant_color, outline=time_code_txt_color)
        canvas.create_text(4*TYPICAL_PADX, week_canvas_height/2+3*TYPICAL_PADX, text="III", font="Verdana 13", justify=LEFT, fill=time_code_txt_color)
        canvas.create_rectangle(week_canvas_width/2+2*TYPICAL_PADX, TYPICAL_PADX , week_canvas_width-TYPICAL_PADX, week_canvas_height/2, fill=week_important_color, outline=time_code_txt_color)
        canvas.create_text(week_canvas_width/2+4*TYPICAL_PADX, 3*TYPICAL_PADX, text="II", font="Verdana 13", justify=LEFT, fill=time_code_txt_color)
        canvas.create_rectangle(week_canvas_width/2+2*TYPICAL_PADX, week_canvas_height/2+TYPICAL_PADX, week_canvas_width - TYPICAL_PADX, week_canvas_height-TYPICAL_PADX, fill=week_other_color, outline=time_code_txt_color)
        canvas.create_text(week_canvas_width / 2 + 4 * TYPICAL_PADX, week_canvas_height/2+3*TYPICAL_PADX, text="IV", font="Verdana 13", justify=LEFT, fill=time_code_txt_color)
        # нарисовали матрицу Ковви
        #Создаём радиобаттоны для переключения важности и срочности задач, которые занесём в матрицу Кови
        quad_var = IntVar()
        quad_var.set(1)
        quad_1_rb = Radiobutton(master=frame_tab_dict["Неделя"], text="I", variable=quad_var, value=1)
        quad_2_rb = Radiobutton(master=frame_tab_dict["Неделя"], text="II", variable=quad_var, value=2)
        quad_3_rb = Radiobutton(master=frame_tab_dict["Неделя"], text="III", variable=quad_var, value=3)
        quad_4_rb = Radiobutton(master=frame_tab_dict["Неделя"], text="IV", variable=quad_var, value=4)
        quad_1_rb.place(x=25*week_canvas_x0, y=10*TYPICAL_PADX)
        quad_2_rb.place(x=27 * week_canvas_x0, y=10 * TYPICAL_PADX)
        quad_3_rb.place(x=25 * week_canvas_x0, y=15 * TYPICAL_PADX)
        quad_4_rb.place(x=27 * week_canvas_x0, y=15 * TYPICAL_PADX)

        week_task_txt = StringVar() # Подготовка переменной и оформление поля ввода задачи на неделю
        week_task_entry = Entry(master=frame_tab_dict["Неделя"], width=task_entry_width, textvariable=week_task_txt)
        week_task_entry.place(x=16*week_canvas_x0, y=13*TYPICAL_PADX)

        on_load_week_goals() # после прорисовки загружаем из файла цели, если они уже записаны
    # КОНЕЦ - Окно "неделя"
    # ************************************************************************************************************************
    # Окно "О программе"
    if tab_title == "О программе":
        about_label_header_1 = Label(master=frame_tab_dict["О программе"], width = about_width, bg=about_bg_color, text=about_label_text_1)  # оформляем лэйбл с пояснением к работе
        about_label_header_1.place(x=week_canvas_x0, y=10 * TYPICAL_PADX)
        about_label_header_2 = Label(master=frame_tab_dict["О программе"], width = about_width, bg=about_bg_color, text=about_label_text_2, fg="blue", cursor="hand2")  # оформляем лэйбл с сылкой на сайт Глеба Архангельского
        about_label_header_2.place(x=week_canvas_x0, y=15 * TYPICAL_PADX)
        about_label_header_2.bind("<Button-1>", arkh_url)
        about_label_header_3 = Label(master=frame_tab_dict["О программе"], width=about_width, bg=about_bg_color, text=about_label_text_3, fg="black", anchor="w", justify=LEFT)  # оформляем лэйбл с пояснением к работе
        about_label_header_3.place(x=week_canvas_x0, y=25 * TYPICAL_PADX)
        about_label_header_4 = Label(master=frame_tab_dict["О программе"], width=about_width, bg=about_bg_color, text=about_label_text_4, fg="black", anchor="w",justify=LEFT)  # оформляем лэйбл с пояснением к работе
        about_label_header_4.place(x=week_canvas_x0, y=55 * TYPICAL_PADX)
        about_label_header_5 = Label(master=frame_tab_dict["О программе"], width=about_width, bg=about_bg_color, text=about_label_text_5, fg="black", anchor="w", justify=LEFT)  # оформляем лэйбл с пояснением к работе
        about_label_header_5.place(x=week_canvas_x0, y=73 * TYPICAL_PADX)

# загружаем вкладки
period_tabs.pack()
period_tabs.enable_traversal()

# КОНЕЦ - прорисовка окна приложения
#*****************************************************************************************************************
#*****************************************************************************************************************
#*****************************************************************************************************************
#*****************************************************************************************************************
# Перспективы развития программы:
# Создать аналог для мобильного приложения
# Сделать оповещения о приближении временнЫх задач (сообщение, звуковой сигнал, вибрация для мобильного)
# Возможность смены дизайна окна приложения: картинка на заднем плане, цвет окошек, текста, фона
# Сделать англоязычную версию

# Запуск приложения
window.mainloop()

