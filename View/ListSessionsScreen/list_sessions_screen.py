from kivy.logger import Logger

from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.clock import Clock
from functools import partial
from kivymd.uix.recycleview import MDRecycleView
import os
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

class SessionItem(OneLineAvatarIconListItem):
    session_name = StringProperty()
    session_sid = StringProperty()

    can_delete = BooleanProperty(False)
    page_id = NumericProperty()
    sessions_page = ObjectProperty()


    def callback(self, item):
        session_json_name = f"{self.session_name}_{self.session_sid}.json"
        list_sessions_view = self.parent.parent.parent.parent

        if list_sessions_view.current_sessions_list_type == 'incomplete':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.incomplete_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')

        elif list_sessions_view.current_sessions_list_type == 'completed':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.completed_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')


    def delete_session(self, session):
        self.sessions_page = self.parent.parent
        Logger.info(f"{__name__}: session: {session},  gonna be deleted")
        self.sessions_page.delete_session(session)


class SessionsPage(MDRecycleView):
    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()
    sessions_list = ListProperty()

    list_sessions_view = ObjectProperty()

    delete_session_index = NumericProperty()
    delete_session_name = StringProperty()
    delete_session_sid = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        close_delete_dialog_btn = MDFlatButton(text="Cancel", on_release=self.close_delete_session_dialog)
        confirm_delete_dialog_btn = MDFlatButton(text="Confirm", on_release=self.confirm_delete_session_dialog)
        self.delete_session_dialog = MDDialog(title="Delete",
                                      type="alert",
                                      buttons=(close_delete_dialog_btn, confirm_delete_dialog_btn)
                                      )

    def close_delete_session_dialog(self, event):
        self.delete_session_dialog.dismiss()

    def confirm_delete_session_dialog(self, event):
        self.sessions_list.pop(self.delete_session_index)
        self.list_sessions_view.delete_session(self.delete_session_sid)
        self.update_sessions('incomplete')
        self.delete_session_dialog.dismiss()

    def delete_session(self, session):
        self.delete_session_index = session.page_id
        self.delete_session_name = session.session_name
        self.delete_session_sid = session.session_sid
        ses_path = self.incomplete_path.joinpath(f'{session.session_name}_{session.session_sid}.json')
        ses_num_of_records = len(JsonStore(ses_path).get('data').get('records'))

        self.delete_session_dialog.title = "Delete Session"
        self.delete_session_dialog.text = f"You sure you want delete [b]{self.delete_session_name}[/b] with [b]{ses_num_of_records}[/b] records?"
        self.delete_session_dialog.open()

    def update_sessions(self, session_type):
        if session_type == 'completed':
            self.sessions_list = list(self.completed_path.glob("*.json"))
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1],

                 'can_delete': False,
                 'page_id': i}
                for i, session in enumerate(self.sessions_list)
            ]

        elif session_type == 'incomplete':
            self.sessions_list = list(self.incomplete_path.glob("*.json"))
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1],

                 'can_delete': True,
                 'page_id': i}
                for i, session in enumerate(self.sessions_list)
            ]



class ListSessionsScreenView(BaseScreenView):
    app_bar_title = StringProperty('Default Title')
    current_sessions_list_type = StringProperty()

    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()

    def delete_session(self, session_sid: str):
        self.model.delete_session(session_sid)

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
        self.ids.sessions_page.list_sessions_view = self


    def start_completed_sessions(self):
        Logger.info(f"{__name__}: started completed sessions")
        self.current_sessions_list_type = 'completed'
        self.app_bar_title = "Completed sessions"
        self.ids.sessions_page.update_sessions('completed')
        self.ids.sessions_page.list_sessions_view = self



    def send_path_to_session_screen(self, path):
        self.model.send_path_to_session_screen(path)