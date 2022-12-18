from View.base_screen import BaseScreenView
from kivy.storage.jsonstore import JsonStore
import secrets
from kivy.properties import StringProperty
from kivy import Logger
class HomeScreenView(BaseScreenView):

    session_json_path = StringProperty()

    def __init__(self, **kwargs):
        super(HomeScreenView, self).__init__(**kwargs)
        Logger.info(f"{__name__}: Initializing, trying to acces id: {self.ids}")

    def start_new_session(self, session_name='session_name', date='11.12.2022'):
        self.controller.start_new_session(session_name, date)

    def start_recorded_sessions(self):
        self.model.start_list_sessions("completed")

    def start_incomplete_sessions(self):
        self.model.start_list_sessions("incomplete")

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
