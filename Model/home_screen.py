from kivy.properties import ObjectProperty

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
import secrets
import pathlib
from pathlib import Path
from kivy.logger import Logger
from os.path import dirname, abspath
from Utility.google_sheets import authorize_gsheets, get_g_sheet
import time
import calendar


class HomeScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.home_screen.HomeScreen.HomeScreenView` class.
    """
    json_storage_path = pathlib.Path("assets", "data").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited, app abs data path: {self.json_storage_path}")

    def start_list_sessions(self, state):
        Logger.info(f"{__name__}: Started listing sessions, state={state}")
        for observer in self._observers:
            if observer.name == "list sessions screen":
                if state == "completed":
                    observer.start_completed_sessions()
                elif state == "incomplete":
                    observer.start_incomplete_sessions()

    def start_new_session(self, session_name, date):
        current_gmt = time.gmtime()
        ts = calendar.timegm(current_gmt)
        unique_id = str(ts)  # before it was secrets.token_urlsafe(2)
        new_session_json_name = f"{session_name}_{unique_id}"
        path_to_new_session_json = self.json_storage_path.joinpath(new_session_json_name + '.json')
        Logger.info(f"{__name__}: started new session: {path_to_new_session_json}")

        self.create_new_session_json(session_name=session_name,
                                     sid=unique_id,
                                     date=date)

        self.send_session_json_path_to_session_screen(path_to_new_session_json)

    def create_new_session_json(self, session_name, sid, date):
        new_session_json = JsonStore(self.json_storage_path.joinpath(f"{session_name}_{sid}" + '.json'), indent=4)
        session_json_keys = {
            'session_name': session_name,
            'date': date,
            'sid': sid,
            'state': 'incomplete',
        }

        new_session_json.put("info", **session_json_keys)
        new_session_json.put("data", records=[])

    def send_session_json_path_to_session_screen(self, session_path: Path) -> None:
        for observer in self._observers:
            if observer.name == 'session screen':
                observer.model.receive_session_json_path_from_screen(session_path, "home screen")





