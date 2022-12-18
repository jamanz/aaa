from kivy.logger import Logger

from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty
from kivy.clock import Clock
from functools import partial

class ListSessionsScreenView(BaseScreenView):

    back_screen = StringProperty()
    app_bar_title = StringProperty()
    current_sessions_list_type = StringProperty()

    incomplete_path = Path("assets", "data")
    completed_path = Path("assets", "data", "completed")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, item):
        print("item pressed: ", item.text)
        if self.current_sessions_list_type == 'incomplete':
            self.send_path_to_session_screen(Path(self.incomplete_path, item.text))
        elif self.current_sessions_list_type == 'completed':
            self.send_path_to_session_screen(Path(self.completed_path, item.text))
        self.app.manager_screens.current = "session screen"


    def on_enter(self, *args):
        Logger.info(f"{__name__}: on_enter fired")
        self.ids.session_list.clear_widgets()

        def add_session_item(session, *args):
            self.ids.session_list.add_widget(
                OneLineListItem(
                    text=str(session.name),
                    on_press=self.callback
                )
            )


        Logger.info(f"{__name__}: items gonna be added to list")
        sessions_num = 0

        if self.current_sessions_list_type == "incomplete":
            incomplete_sessions = self.incomplete_path.glob("*.json")
            for i, session in enumerate(incomplete_sessions):
                sessions_num += 1
                Clock.schedule_once(partial(add_session_item, session), i*0.03)

        elif self.current_sessions_list_type == "completed":
            completed_sessions = self.completed_path.glob("*.json")
            for i, session in enumerate(completed_sessions):
                sessions_num += 1
                Clock.schedule_once(partial(add_session_item, session), i*0.03)

        Logger.info(f"{__name__}: Clock scheduled, {sessions_num} items added to list")
        sessions_num = 0

    def __init__(self, **kwargs):
        super(ListSessionsScreenView, self).__init__(**kwargs)

    def back_to_screen(self, screen):
        self.ids.session_list.clear_widgets()
        self.app.manager_screens.current = screen

    def add_app_toolbar(self, bar_title: str, back_screen: str):
        self.ids.app_bar.add_widget(
            MDTopAppBar(title=bar_title,
                        type_height="medium",
                        headline_text="Headline",
                        left_action_items=
                        [["arrow-left", lambda x: self.back_to_screen(back_screen)]]
                        )
        )
        Logger.info(f"{__name__}: toolbar added successfully")

    def start_incomplete_sessions(self):
        Logger.info(f"{__name__}: started incomplete sessions")
        self.on_enter()
        self.add_app_toolbar("Incomplete sessions", "home screen")

    def start_completed_sessions(self):
        Logger.info(f"{__name__}: started completed sessions")
        self.on_enter()
        self.add_app_toolbar("Completed sessions", "home screen")


    def send_path_to_session_screen(self, path):
        self.model.send_path_to_session_screen(path)

