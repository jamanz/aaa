from kivy.logger import Logger

from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from functools import partial
from kivymd.uix.recycleview import MDRecycleView
import os
from kivy.core.window import Window


class SessionItem(OneLineListItem):
    session_name = StringProperty()
    session_sid = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, item):
        session_json_name = f"{self.session_name}_{self.session_sid}.json"
        list_sessions_view = self.parent.parent.parent.parent

        if list_sessions_view.current_sessions_list_type == 'incomplete':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.incomplete_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')

        elif list_sessions_view.current_sessions_list_type == 'completed':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.completed_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')


class SessionsPage(MDRecycleView):
    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sessions_list = None

    def update_sessions(self, session_type):
        if session_type == 'completed':
            self.sessions_list = self.completed_path.glob("*.json")
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1]} for session in self.sessions_list]
        elif session_type == 'incomplete':
            self.sessions_list = self.incomplete_path.glob("*.json")
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1]} for session in self.sessions_list]


class ListSessionsScreenView(BaseScreenView):
    app_bar_title = StringProperty('Default Title')
    current_sessions_list_type = StringProperty()

    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def on_pre_enter(self, *args):
        self.ids.sessions_page.update_sessions(self.current_sessions_list_type)

    def start_incomplete_sessions(self):
        Logger.info(f"{__name__}: started incomplete sessions")
        self.current_sessions_list_type = 'incomplete'
        self.app_bar_title = "Incomplete sessions"
        self.ids.sessions_page.update_sessions('incomplete')

    def start_completed_sessions(self):
        Logger.info(f"{__name__}: started completed sessions")
        self.current_sessions_list_type = 'completed'
        self.app_bar_title = "Completed sessions"
        self.ids.sessions_page.update_sessions('completed')

    def send_path_to_session_screen(self, path):
        self.model.send_path_to_session_screen(path)