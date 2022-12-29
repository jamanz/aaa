
"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
DEBUG=1 python main.py
"""

# import importlib
# import os
#
# from kivy import Config
#
# from PIL import ImageGrab
# import logging
# from kivy import Logger
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
# print(f"started new logger {logger} with scope level {logger.level}")
# print(f"logger handlers: {logger.handlers}")
# print("Connected loggers:", *logging.Logger.manager.loggerDict.keys(), sep=", ")
#
# # TODO: You may know an easier way to get the size of a computer display.
# resolution = ImageGrab.grab().size
#
# # Change the values of the application window size as you need.
# Config.set("graphics", "height", "700")
# Config.set("graphics", "width", "400")
#
# from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
# Window.top = 0
# Window.left = resolution[0] - Window.width

# from kivymd.tools.hotreload.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager


# class agroApp3MVC(MDApp):
#     KV_DIRS = [os.path.join(os.getcwd(), "View")]
#
#     def build_app(self) -> MDScreenManager:
#         """
#         In this method, you don't need to change anything other than the
#         application theme.
#         """
#
#         import View.screens
#         logger.info(f"{__name__} build app called")
#         self.manager_screens = MDScreenManager()
#         Window.bind(on_key_down=self.on_keyboard_down)
#
#         # inportlib used
#         #It allows you to import modules which you do not know the name at coding time.
#         #For instance when my application starts,
#         # I walk through a directory structure and load the modules as I discover them.
#
#         importlib.reload(View.screens)
#         screens = View.screens.screens
#
#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)
#
#
#         logger.info(f"screen manager: {self.manager_screens.children}")
#         return self.manager_screens
#
#     def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
#         """
#         The method handles keyboard events.
#
#         By default, a forced restart of an application is tied to the
#         `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
#         """
#
#         if "meta" in modifiers or "ctrl" in modifiers and text == "r":
#             self.rebuild()
#
#
# agroApp3MVC().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

# """
# The entry point to the application.
# 
# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.
# 
# You can read more about this template at the links below:
# 
# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikip  edia.org/wiki/Model–view–controller
# """
#
from kivy import Logger
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
import os
from os.path import abspath, dirname
from pathlib import Path
from View.screens import screens
from kivy import user_home_dir, kivy_home_dir, kivy_base_dir, dirname
from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex





    # tree_sheet = client.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1


class agroApp3MVC(MDApp):
    app_folder = os.path.dirname(os.path.abspath(__file__))
    g_sheet = None
    list_of_prev_screens = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_cls.theme_style = "Dark"#"#53565A"
        self.theme_cls.primary_palette = 'Green'#get_color_from_hex("#628038")#"Orange"
        #self.theme_cls.
        # self.user_data_dir
        self.load_all_kv_files(self.directory)
        Logger.info(f"{__name__}: all KV files loaded in directory: {self.directory}")
        Window.bind(on_keyboard=self._key_handler)
        # Logger.info(f"{__name__}: script path: {script_path}")
        Logger.info(f"""{__name__}: APP INITED on platform: {platform} 
                    abs path for app: {self.app_folder}
                    kivy userhomedir: {user_home_dir}
                    kivy_home_dir: {kivy_home_dir}
                    kivy_base_dir: {kivy_base_dir} 
                    dirname: {dirname}""")
        # This is the screen manager that will contain all the screens of application.
        self.manager_screens = MDScreenManager()

    def go_next_screen(self, current_screen_name, next_screen_name):
        self.list_of_prev_screens.append(current_screen_name)
        self.manager_screens.transition.direction = 'left'
        self.manager_screens.current = next_screen_name

    def go_prev_screen(self):
        if self.list_of_prev_screens:
            self.manager_screens.transition.direction = 'right'
            self.manager_screens.current = self.list_of_prev_screens.pop()
            return True
        return False

    def _key_handler(self, instance, key, *args):
        if key is 27:
            return self.go_prev_screen()
        return False

    def build(self) -> MDScreenManager:
        self.generate_application_screens()
        # Logger.info(f"{__name__}: application screens loaded, SM: {self.manager_screens.screens}")
        return self.manager_screens

    def on_start(self):
        Logger.info(f"{__name__}: on_start fired")
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def on_pause(self):
        Logger.info(f"{__name__}: on_pause fired")
        return True

    def on_resume(self):
        Logger.info(f"{__name__}: resume fired")

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


agroApp3MVC().run()
