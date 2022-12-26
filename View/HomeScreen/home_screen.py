from View.base_screen import BaseScreenView
from kivy.storage.jsonstore import JsonStore
import secrets
from kivy.properties import StringProperty
from kivy import Logger


class HomeScreenView(BaseScreenView):

    # session_json_path = StringProperty()

    def __init__(self, **kwargs):
        super(HomeScreenView, self).__init__(**kwargs)

    def start_new_session(self, session_name='session_name', date='11.12.2022'):
        self.controller.start_new_session(session_name, date)
        self.app.go_next_screen('home screen', 'session screen')

    def start_recorded_sessions(self):
        self.model.start_list_sessions("completed")
        self.app.go_next_screen('home screen', 'list sessions screen')

    def start_incomplete_sessions(self):
        self.model.start_list_sessions("incomplete")
        self.app.go_next_screen('home screen', 'list sessions screen')

