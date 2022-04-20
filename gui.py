import dearpygui.dearpygui as dpg
import Handler
import os

WIDTH = 1200
HEIGHT = 720

def main():

    dpg.create_context()

    # Выключение остальных радиокнопок
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

    def Start():
        dpg.delete_item('f_window')

        with dpg.window(label="", tag='loading_window', width=WIDTH, height=HEIGHT, modal=True, no_move=True,
                        no_collapse=True, no_close=True, no_title_bar=True):
            dpg.add_loading_indicator(label='loading', pos=[int(WIDTH/2) - 30, int(HEIGHT/2) - 30], radius=15.0)

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

        #Handler.Timelaps()
        dpg.delete_item('loading_window')
        Second_window()

    def Check_Path():
        path = dpg.get_value('string_value')
        """
            Проверка правильности пути
        """
        try:
            dpg.delete_item('Checked_window')
            try:
                os.mkdir(str(path))  # "C:\\test"
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)
                dpg.add_text("Folder created", tag='checked_text', parent='Checked_window')
            except:
                print("Папка не создана")
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)
                dpg.add_text("Folder NOT created", tag='checked_text', parent='Checked_window')
        except:
            try:
                os.mkdir(str(path))  # "C:\\test"
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)
                dpg.add_text("Folder created", tag='checked_text', parent='Checked_window')
            except:
                print("Папка не создана")
                dpg.add_window(tag='Checked_window', autosize=True, popup=True)
                dpg.add_text("Folder NOT created", tag='checked_text', parent='Checked_window')


    def Save():
        path = dpg.get_value('string_value')
        # Перемещение файлов в новосозданную директорию
        for i in range(13):
            os.system("MOVE .\\Cloud_" + str(i) + ".png, " + str(path))# C:\\Users\\A\\PycharmProjects\\PI\\Cloud_" + str(i) + ".png, " + str(path)
        os.system("MOVE C:\\Users\\A\\PycharmProjects\\PI\\POST_habr.csv, " + str(path))# C:\\test")
        os.system("MOVE C:\\Users\\A\\PycharmProjects\\PI\\POST_proglib.csv, " + str(path))# C:\\test")
        os.system("MOVE C:\\Users\\A\\PycharmProjects\\PI\\POST_NAME_habr.csv, " + str(path))# C:\\test")
        os.system("MOVE C:\\Users\\A\\PycharmProjects\\PI\\POST_NAME_proglib.csv, " + str(path))# C:\\test")

        # Вывод сообщения о сохранении
        with dpg.window(tag='saved_window', autosize=True, pos=[400, 300]):
            dpg.add_text("Seved", tag='text_saved')
        width, height, channels, data = dpg.load_image("Save.png")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width, height, data, tag="save")
        with dpg.window(tag='save_window', autosize=True, pos=[300]):
            dpg.add_image("save")

    with dpg.value_registry():
        dpg.add_bool_value(default_value=True, tag="bool_value_1")
        dpg.add_bool_value(default_value=False, tag="bool_value_2")
        dpg.add_bool_value(default_value=False, tag="bool_value_3")
        dpg.add_bool_value(default_value=False, tag="bool_value_4")
        dpg.add_string_value(default_value="Enter the path to save the archive", tag="string_value")

    with dpg.window(label="Select topic", tag='f_window', width=WIDTH, height=HEIGHT):
        dpg.add_checkbox(label="Develop", source="bool_value_1", callback=lambda: Off_Except_1())
        dpg.add_checkbox(label="Admin", source="bool_value_2", callback=lambda: Off_Except_2())
        dpg.add_checkbox(label="Design", source="bool_value_3", callback=lambda: Off_Except_3())
        dpg.add_checkbox(label="Marketing", source="bool_value_4", callback=lambda: Off_Except_4())

        dpg.add_input_text(label="Save path", source="string_value")
        dpg.add_button(label='Create folder', width=100, height=50, callback=lambda: Check_Path())
        dpg.add_button(label='Start', width=100, height=50, callback=lambda: Start())

    def Second_window():
        # test_gui
        def Load():
            dpg.delete_item('cloud')
            dpg.delete_item('window')
            width, height, channels, data = dpg.load_image("Cloud_" + str(dpg.get_value('slider_value_1')) + ".png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(width, height, data, tag="cloud")
            with dpg.window(tag='window', autosize=True, pos=[300]):
                dpg.add_image("cloud")
        """if (dpg.get_value('slider_value_1') == 0):
                print(0)
                dpg.delete_item('cloud')
                dpg.delete_item('window')
                width, height, channels, data = dpg.load_image("Cloud_1.png")
                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width, height, data, tag="cloud")
            if (dpg.get_value('slider_value_1') == 1):
                print(1)
                dpg.delete_item('cloud')
                dpg.delete_item('window')
                width, height, channels, data = dpg.load_image("Cloud_2.png")
                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width, height, data, tag="cloud")
            if (dpg.get_value('slider_value_1') == 2):
                print(2)
                dpg.delete_item('cloud')
                dpg.delete_item('window')
                width, height, channels, data = dpg.load_image("Cloud_3.png")
                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width, height, data, tag="cloud")
            if (dpg.get_value('slider_value_1') == 3):
                print(2)
                dpg.delete_item('cloud')
                dpg.delete_item('window')
                width, height, channels, data = dpg.load_image("cat2.jpg")
                with dpg.texture_registry(show=False):
                    dpg.add_static_texture(width, height, data, tag="cloud")

            with dpg.window(tag='window', autosize=True, pos=[300]):
                dpg.add_image("cloud")"""

        # Дефолт пpи ошибки парса
        width, height, channels, data = dpg.load_image("cat1.jpg")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width, height, data, tag="cloud")
        with dpg.window(tag='window', autosize=True, pos=[300]):
            dpg.add_image("cloud")

        with dpg.value_registry():
            dpg.add_int_value(default_value=0, tag='slider_value_1')

        with dpg.window(pos=[300, 600], width=640, height=10):
            dpg.add_slider_int(source='slider_value_1', default_value=1, min_value=1, max_value=12,
                               callback=lambda: Load(), width=640, height=5)
            dpg.add_button(label='Save', width=100, height=50, callback= lambda: Save())

        # end test_gui

    dpg.create_viewport(title='Custom Title', width=WIDTH, height=HEIGHT)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()