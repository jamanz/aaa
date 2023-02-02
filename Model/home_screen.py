import gspread
from kivy.properties import ObjectProperty

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
import secrets
import pathlib
from pathlib import Path
from kivy.logger import Logger
from os.path import dirname, abspath
from kivy.properties import StringProperty
#from Utility.google_sheets import authorize_gsheets
import time
import calendar
from Utility.google_sheets import (next_available_row, features_name_to_sheets_columns_map,
                                   auth_in_gsheets, receive_client_sheet_by_id, get_g_sheet_client_sheet_list,
                                   make_oauth, get_worksheet)
from kivy.clock import Clock

class HomeScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.home_screen.HomeScreen.HomeScreenView` class.
    """
    json_storage_path = pathlib.Path("assets", "data").resolve()

    # Instances for uploading to GSheets
    g_sheet_client = None
    chosen_worksheet = None
    google_client = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Default for upload if user don't done choice about worksheet
        self.chosen_worksheet = StringProperty('worksheet1')
        Logger.info(f"{__name__}: Inited")
        # Clock.schedule_once(self.authorize_g_sheet_client, 1)

    def get_worksheet(self):
        if self.google_client is None:
            self.auth_in_google()
        self.chosen_worksheet = get_worksheet(self.google_client)
        return self.chosen_worksheet

    def send_first_worksheet_instance_to_session_screen_model(self):
        for observer in self._observers:
            if observer.name == "session screen":
                self.get_worksheet()
                observer.model.receive_worksheet(self.chosen_worksheet)

    def auth_in_google(self):
        self.google_client = make_oauth()
        self.send_g_client_to_session_screen_model(self.google_client)

    def send_g_client_to_session_screen_model(self, g_client: gspread.Client):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.model.receive_g_client_from_home_screen_model(g_client)

    def send_worksheet_instance_to_session_screen_model(self, worksheet_title: str):
        for observer in self._observers:
            if observer.name == "session screen":
                worksheet = self.g_sheet_client.worksheet(worksheet_title)
                observer.model.receive_client_and_worksheet_from_home_screen_model(worksheet)

    def get_list_of_available_worksheets_to_view(self):
        return [ws.title for ws in self.list_available_worksheets()]

    def authorize_g_sheet_client(self, dt):
        self.g_sheet_client = receive_client_sheet_by_id()
        Logger.info(f"{__name__}: async Google sheets inited")

    def list_available_worksheets(self):
        return get_g_sheet_client_sheet_list(self.g_sheet_client)

    def set_chosen_worksheet(self, worksheet_title):
        Logger.info(f"{__name__}: retrieved from View worksheet with title : {worksheet_title}")
        self.send_worksheet_instance_to_session_screen_model(worksheet_title)


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





