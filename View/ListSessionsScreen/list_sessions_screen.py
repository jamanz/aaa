from kivy.logger import Logger

from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from functools import partial
from kivy.uix.recycleview import RecycleView
import os
from kivy.core.window import Window


class SessionItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, item):
        Logger.info(f"{__name__}: item pressed: {item.text}")
        list_sessions_view = self.parent.parent.parent.parent

        if list_sessions_view.current_sessions_list_type == 'incomplete':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.incomplete_path, item.text))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')

        elif list_sessions_view.current_sessions_list_type == 'completed':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.completed_path, item.text))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')


class SessionsPage(RecycleView):
    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sessions_list = None

    def update_sessions(self, session_type):
        if session_type == 'completed':
            self.sessions_list = self.completed_path.glob("*.json")
            self.data = [{'text': str(session.name)} for session in self.sessions_list]
        elif session_type == 'incomplete':
            self.sessions_list = self.incomplete_path.glob("*.json")
            self.data = [{'text': str(session.name)} for session in self.sessions_list]


class ListSessionsScreenView(BaseScreenView):
    app_bar_title = StringProperty('Default Title')
    current_sessions_list_type = StringProperty()

    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.ids.sessions_page.update_sessions(self.current_sessions_list_type)
    # def on_pre_enter(self, *args):
    #     Logger.info(f"{__name__}: on_pre_enter fired")
    #     self.ids.session_list.clear_widgets()
    #
    #     def add_session_item(session, *args):
    #         self.ids.session_list.add_widget(
    #             OneLineListItem(
    #                 text=str(session.name),
    #                 on_press=self.callback
    #             )
    #         )
    #
    #     Logger.info(f"{__name__}: items gonna be added to list")
    #     sessions_num = 0
    #
    #     if self.current_sessions_list_type == "incomplete":
    #         incomplete_sessions = self.incomplete_path.glob("*.json")
    #         for i, session in enumerate(incomplete_sessions):
    #             sessions_num += 1
    #             Clock.schedule_once(partial(add_session_item, session), i*0.03)
    #
    #     elif self.current_sessions_list_type == "completed":
    #         completed_sessions = self.completed_path.glob("*.json")
    #         # self.completed_sessions_prop = os.listdir(self.completed_path)
    #         for i, session in enumerate(completed_sessions):
    #             sessions_num += 1
    #             Clock.schedule_once(partial(add_session_item, session), i*0.03)
    #
    #     Logger.info(f"{__name__}: Clock scheduled, {sessions_num} items added to list")
    #     sessions_num = 0

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

        # MDAnchorLayout:
        # size_hint: 1, 0.1
        # anchor_y: 'top'
        # id: app_bar
        # md_bg_color: utils.get_color_from_hex('#75c72f')

        # MDStackLayout:
        #     #md_bg_color: utils.get_color_from_hex('#F05F40')
        #     size_hint: 1, 0.9
        #     #pos_hint: {"center_x": .5, "center_y": .5}
        #     orientation: 'rl-tb'
        #
        #     MDScrollView:
        #
        #         do_scroll_x: False
        #         do_scroll_y: True
        #         #MDGridLayout:
        #         MDList:
        #             id: session_list
        #             height: self.minimum_height
        #             #cols: 1
        #             size_hint: 1, None
        #             #orientation: 'rl-tb'