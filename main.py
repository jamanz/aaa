
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
from kivymd._version import __version__
Logger.info(f"{__name__}: app code enter, kivymd ver == {__version__}")

from pathlib import Path
# from kivy.config import Config
# Config.set('kivy', 'default_font', ['Arimo', './assets/fonts/Arimo-Regular.ttf',
#                                              './assets/fonts/Arimo-Italic.ttf',
#                                              './assets/fonts/Arimo-Bold.ttf',
#                                              './assets/fonts/Arimo-BoldItalic.ttf',
#                                             ])
# Config.write()

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
import os
from os.path import abspath, dirname

from View.screens import screens
from kivy import user_home_dir, kivy_home_dir, kivy_base_dir, kivy_data_dir

from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex

from android_permissions import AndroidPermissions

from dotenv import load_dotenv
# from Utility.google_auth import initialize_google, login_google, logout_google
# from Utility.google_auth_utils import login_providers, auto_login, stop_login
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivyauth.utils import stop_login
from kivyauth.utils import login_providers, auto_login


# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '740')
#Config.set('modules', 'monitor', '')

#load_dotenv()
from kivy.core.text import LabelBase

import gettext

he_home_screen = gettext.translation('home_screen', localedir='locales', languages=['he'])
# he_list_sessions_screen = gettext.translation('list_sessions_screen', localedir='locales', languages=['he'])
he_home_screen.install()
# he_list_sessions_screen.install()

import os



# Logger.info(f"{__name__} conf {Config.get('kivy', 'default_font')}")
# Config.write()

LabelBase.register(name="Arimo", fn_regular="assets/fonts/Arimo-Regular.ttf", fn_bold="assets/fonts/Arimo-Bold.ttf")
#print(f"!!!!! {LabelBase.get_system_fonts_dir()}")


if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    from android import mActivity

    View = autoclass('android.view.View')

    Toast = autoclass("android.widget.Toast")
    String = autoclass("java.lang.String")
    CharSequence = autoclass("java.lang.CharSequence")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    #NewRelic = autoclass("com.newrelic.agent.android.NewRelic")
    LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
    AndroidColor = autoclass("android.graphics.Color")

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    context = PythonActivity.mActivity

    @run_on_ui_thread
    def show_toast(text):
        t = Toast.makeText(
            context, cast(CharSequence, String(text)), Toast.LENGTH_SHORT
        )
        t.show()


    @run_on_ui_thread
    def set_statusbar_color():
        window = context.getWindow()
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(AndroidColor.TRANSPARENT)

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)



colors = {

    "Red": {
        "A200": "#AA4A44",
        "A500": "#AA4A44",
        "A700": "#AA4A44",
        "200": "#AA4A44",
        "500": "#AA4A44",
        "700": "#AA4A44",
    },


    "Green": {
        "A200": "#76944C",
        "A500": "#76944C",
        "A700": "#76944C",
        "200": "#76944C",
        "500": "#76944C",
        "700": "#76944C",
    },
    "Grey": {
        "A200": "#53565A",
        "A500": "#53565A",
        "A700": "#53565A",
        "200": "#53565A",
        "500": "#53565A",
        "700": "#53565A",
    },

    "BlueGray": {
        "A200": "#DBE2E9",
        "A500": "#DBE2E9",
        "A700": "#DBE2E9",
        "200": "#DBE2E9",
        "500": "#DBE2E9",
        "700": "#DBE2E9",
    },



    "Light": {
        "StatusBar": "#DBE2E9",
        "AppBar": "#628038",
        "Background": "#DBE2E9",

        "Dialog": "#DBE2E9",
        "FlatButtonDown": "#DBE2E9",
    },

    "Dark": {
        "StatusBar": "#DBE2E9",
        "AppBar": "#628038",
        "Background": "#DBE2E9",

        "Dialog": "#DBE2E9",
        "FlatButtonDown": "#DBE2E9",
    },

}


class agroApp3MVC(MDApp):
    app_folder = os.path.dirname(os.path.abspath(__file__))
    g_sheet = None
    list_of_prev_screens = []
    current_provider = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang = 'he'
        self.theme_cls.colors = colors
        self.theme_cls.theme_style = "Light"#"#53565A"

        self.theme_cls.primary_palette = 'Green'#get_color_from_hex("#628038")#"Orange"
        self.theme_cls.accent_palette = "BlueGray"
        self.theme_cls.material_style = "M3"



        print("type M: ", self.theme_cls.material_style)

        #self.theme_cls.font_styles =
        #self.theme_cls.
        # self.user_data_dir
        self.load_all_kv_files(self.directory)
        Logger.info(f"{__name__}: all KV files loaded in directory: {self.directory}")
        Window.bind(on_keyboard=self._key_handler)

        # Logger.info(f"{__name__}: script path: {script_path}")
        Logger.info(f"""{__name__}: APP INITED on platform: {platform} 
                    abs path for app: {self.app_folder}
                    kivy userhomedir: {user_home_dir}
                    user home dir contains: {os.listdir(user_home_dir)}
                    kivy_home_dir: {kivy_home_dir}
                    kivy_base_dir: {kivy_base_dir} 
                    kivy_data_dir: {kivy_data_dir}
                    data dir contains: {os.listdir(kivy_data_dir)}
                
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
        if key == 27:
            return self.go_prev_screen()
        return False

    def build(self) -> MDScreenManager:
        self.generate_application_screens()

        Logger.info(f"{__name__}: Start initializing google")
        # GOOGLE_CLIENT_ID = "845840319772-jc8oaudi9vhqdl5p1ansukeuu839ipj4.apps.googleusercontent.com"
        # GOOGLE_CLIENT_SECRET = "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"
        # new_s
        initialize_google(
            self.after_login,
            self.error_listener,
            # GOOGLE_CLIENT_ID,
            # GOOGLE_CLIENT_SECRET
            # os.getenv("GOOGLE_CLIENT_ID"),
            # os.getenv("GOOGLE_CLIENT_SECRET"),
        )
        #new_e

        Logger.info(f"{__name__}: End initializing google")

        # if platform == 'android':
        #     Window.bind(on_resize=hide_landscape_status_bar)
        #
        #     set_statusbar_color()

        Logger.info(f"{__name__}: application screens loaded, SM: {self.manager_screens.screens}")
        return self.manager_screens

    def on_start(self):
        Logger.info(f"{__name__}: on_start fired")
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE,
                                Permission.READ_EXTERNAL_STORAGE])
        # self.dont_gc = AndroidPermissions(self.start_app)

        # new
        # if platform == "android":
        #     if auto_login(login_providers.google):
        #         self.current_provider = login_providers.google
        #     primary_clr = [108 / 255, 52 / 255, 131 / 255]
        #     hex_color = '#%02x%02x%02x' % (
        #     int(primary_clr[0] * 200), int(primary_clr[1] * 200), int(primary_clr[2] * 200))
        #     set_statusbar_color()
        #Window.release_all_keyboards()

    #new_s
    def gl_login(self, *args):
        login_google()
        self.current_provider = login_providers.google

    def logout_(self):
        if self.current_provider == login_providers.google:
            logout_google(self.after_logout)

    def after_login(self, name, email, photo_uri):
        if platform == "android":
            show_toast("Logged in using {}".format(self.current_provider))
            print(f'name: {name}, email, {email}')

    def after_logout(self):
        self.current_provider = 'google'
        if platform == "android":
            show_toast(text="Logged out from {} login".format(self.current_provider))

    def error_listener(self):
        if platform == "android":
            show_toast("Error logging in.")

    #new_e

    def start_app(self):
        self.dont_gc = None
        self.enable_swipe = True


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
