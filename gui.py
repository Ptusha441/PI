import dearpygui.dearpygui as dpg   # Библиотека для GUI
import Handler
import os   # Библиотека для системных команд Windows

# Параметры экрана
WIDTH = 1500
HEIGHT = 800

def main():

    dpg.create_context()    # Начало настройки графического окна

    # Выключение радиокнопок, которые не используются (защита от множественного выбора тем)
    def Off_Except_1():
        if (dpg.get_value("bool_value_1")):
            dpg.set_value("bool_value_2", False)
            dpg.set_value("bool_value_3", False)
            dpg.set_value("bool_value_4", False)

    def Off_Except_2():
        if (dpg.get_value("bool_value_2")):
            dpg.set_value("bool_value_1", False)
            dpg.set_value("bool_value_3", False)
            dpg.set_value("bool_value_4", False)

    def Off_Except_3():
        if (dpg.get_value("bool_value_3")):
            dpg.set_value("bool_value_1", False)
            dpg.set_value("bool_value_2", False)
            dpg.set_value("bool_value_4", False)

    def Off_Except_4():
        if (dpg.get_value("bool_value_4")):
            dpg.set_value("bool_value_1", False)
            dpg.set_value("bool_value_2", False)
            dpg.set_value("bool_value_3", False)

    # Функция перехода между окнами
    def Transition():
        dpg.delete_item('f_window') # Удаление первого окна

        with dpg.window(tag='loading_window', width=1920, height=1080, modal=True, no_move=True,    # Настройка параметров окна загрузки
                        no_collapse=True, no_close=True, no_title_bar=True):
            dpg.add_loading_indicator(label='loading', width=1920, height=1080,                     # Настройка индикатора загрузки
                                      pos=[int(WIDTH/2) - 70, int(HEIGHT/2) - 50], radius=15.0)
        # Выборка темы с помощью радиокнопок
        if (dpg.get_value("bool_value_1")):
            Handler.Start(int(1))
            print(1)
        elif (dpg.get_value("bool_value_2")):
            Handler.Start(int(2))
            print(2)
        elif (dpg.get_value("bool_value_3")):
            Handler.Start(int(3))
            print(3)
        elif (dpg.get_value("bool_value_4")):
            Handler.Start(int(4))
            print(4)

        dpg.delete_item('loading_window')   # Удаление окна загрузки
        Second_window() # Запуск функции отрисовки второго окна

    # Функция проверки правильность пути создания папки
    def Check_Path():
        path = dpg.get_value('string_value')    # Считывание введеного пути
        try:
            dpg.delete_item('Checked_window')
            try:
                os.mkdir(str(path))  # "C:\\test"
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)                 # Настройка окна
                dpg.add_text("Folder created", tag='checked_text', parent='Checked_window')     # сообщения о создании папки
            except:
                print("Папка не создана")
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)                 # Настройка окна
                dpg.add_text("Folder NOT created", tag='checked_text', parent='Checked_window') # сообщения, что папка не создана
        except:
            try:
                os.mkdir(str(path))  # "C:\\test"
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)                 # Настройка окна
                dpg.add_text("Folder created", tag='checked_text', parent='Checked_window')     # сообщения о создании папки
            except:
                print("Папка не создана")
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)                 # Настройка окна
                dpg.add_text("Folder NOT created", tag='checked_text', parent='Checked_window') # сообщения, что папка не создана

    # Функция сохранения всех файлов в указанную папку
    def Save():
        path = dpg.get_value('string_value')    # Получение пути до папки
        # Перемещение файлов в новосозданную директорию
        for i in range(13):
            os.system("MOVE .\\Cloud_" + str(i) + ".png, " + str(path))
        os.system("MOVE .\\POST_habr.csv, " + str(path))
        os.system("MOVE .\\POST_proglib.csv, " + str(path))
        os.system("MOVE .\\POST_NAME_habr.csv, " + str(path))
        os.system("MOVE .\\POST_NAME_proglib.csv, " + str(path))

        # Удаление всех окон
        dpg.delete_item('cloud')
        dpg.delete_item('window')
        dpg.delete_item('slider_window')

        # Вывод сообщения об успешном сохранении
        width, height, channels, data = dpg.load_image("Save.png")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width, height, data, tag="save")
        with dpg.window(label='Saved', tag='save_window', autosize=True, pos=[int(WIDTH/2)-int(width), 0], popup=True):
            dpg.add_image("save")

    # Реализация переключения радиокнопок и строки ввода
    with dpg.value_registry():
        dpg.add_bool_value(default_value=True, tag="bool_value_1")
        dpg.add_bool_value(default_value=False, tag="bool_value_2")
        dpg.add_bool_value(default_value=False, tag="bool_value_3")
        dpg.add_bool_value(default_value=False, tag="bool_value_4")
        dpg.add_string_value(default_value="Enter the path to save the archive", tag="string_value")

    # Добавление элементов в окно
    with dpg.window(label="Select topic", tag='f_window', width=WIDTH, height=HEIGHT):
        # Добавление радиокнопок
        dpg.add_checkbox(label="Develop", source="bool_value_1", callback=lambda: Off_Except_1())
        dpg.add_checkbox(label="Admin", source="bool_value_2", callback=lambda: Off_Except_2())
        dpg.add_checkbox(label="Design", source="bool_value_3", callback=lambda: Off_Except_3())
        dpg.add_checkbox(label="Marketing", source="bool_value_4", callback=lambda: Off_Except_4())
        # Добавление строки ввода
        dpg.add_input_text(label="Save path", source="string_value")
        # Добавление кнопок
        dpg.add_button(label='Create folder', width=100, height=50, callback=lambda: Check_Path())
        dpg.add_button(label='Start', width=100, height=50, callback=lambda: Transition())

    # Функция отрисовки второго окна
    def Second_window():
        # Функция отрисовки таймлапса
        def Load():
            dpg.delete_item('cloud')    # Удаление отрисованных окон
            dpg.delete_item('window')
            width, height, channels, data = dpg.load_image("Cloud_" + str(dpg.get_value('slider_value_1')) + ".png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(width, height, data, tag="cloud")    # Настройка нового изображения
            with dpg.window(tag='window', autosize=True, pos=[int(WIDTH/2)-int(width), 0]):
                dpg.add_image("cloud")  # Отрисовка нового изображения

        # Начальное изображения
        width, height, channels, data = dpg.load_image("Cloud_1.png")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width, height, data, tag="cloud")
        with dpg.window(tag='window', autosize=True, pos=[int(WIDTH/2)-int(width), 0]):
            dpg.add_image("cloud")

        # Реализация работы слайдера
        with dpg.value_registry():
            dpg.add_int_value(default_value=0, tag='slider_value_1')

        # Добавление окна управления таймлапсом
        with dpg.window(tag='slider_window', pos=[int(WIDTH/2)-int(645), 600], width=645, height=10):
            # Добаление слайдера и кнопки сохранения
            dpg.add_slider_int(source='slider_value_1', default_value=1, min_value=1, max_value=12,
                               callback=lambda: Load(), width=640, height=5)
            dpg.add_button(label='Save', width=100, height=50, callback= lambda: Save())

    # Отрисовка окна GUI
    dpg.create_viewport(title='Application', width=WIDTH, height=HEIGHT)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()