from kivy.properties import ObjectProperty

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
import secrets
import pathlib
from pathlib import Path
from kivy.logger import Logger
from os.path import dirname, abspath


class HomeScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.home_screen.HomeScreen.HomeScreenView` class.
    """

    # new_session_json = ObjectProperty()

    # todo: must be not empty, add error handling,
    # link: https://stackoverflow.com/questions/42513056/how-to-get-absolute-path-of-a-pathlib-path-object
    json_storage_path = pathlib.Path("assets", "data").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Initializing, app abs data path: {self.json_storage_path}")

    def start_list_sessions(self, state):
        Logger.info(f"{__name__}: Started listing sessions, state={state}")
        for observer in self._observers:
            if observer.name == "list sessions screen":
                if state == "completed":
                    observer.model.start_completed_sessions()
                elif state == "incomplete":
                    observer.model.start_incomplete_sessions()

    def start_new_session(self, session_name, date):


        self.unique_id = secrets.token_urlsafe(2)
        self.session_name = f"{session_name}_{self.unique_id}"

        Logger.info(f"{__name__}: started new session: {self.session_name}")
        self.create_new_session_json(session_name=self.session_name,
                                     sid=self.unique_id,
                                     date=date)

        path_to_json = self.json_storage_path.joinpath(self.session_name + '.json')
        self.send_session_json_path_to_models(path_to_json, "session screen")
        # self.send_session_json_path_to_models(path_to_json, "add data screen")

    def create_new_session_json(self, session_name, sid, date):
        # print("PATH: ", self.json_storage_path.joinpath(session_name + '.json'))
        self.new_session_json = JsonStore(self.json_storage_path.joinpath(session_name + '.json'))
        session_json_keys = {
            'session_name': session_name,
            'date': date,
            'sid': sid,
            'state': 'incomplete',
        }

        self.new_session_json.put("info", **session_json_keys)
        self.new_session_json.put(session_name, records=[])

    def send_session_json_path_to_models(self, session_path: Path, name_screen: str) -> None:
        for observer in self._observers:
            if observer.name == name_screen:
                observer.model.receive_session_json_path_from_screen_model(session_path, "home screen")



