from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
import json
import secrets
from kivy.properties import ObjectProperty, StringProperty
from pathlib import Path
import os
from kivy.logger import Logger

class SessionScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.session_screen.SessionScreen.SessionScreenView` class.
    """

    #_session_json_path = ObjectProperty()

    def __init__(self):
        print(f"{__name__} Inited")
        self.session_json_path =None

    def upload_session(self, session_path: Path):
        self.session_json = JsonStore(session_path)
        self.session_json.put("info", state="completed")
        new_path = Path(session_path.parent, "completed", session_path.name)
        os.rename(session_path, new_path)
        Logger.info(f"{__name__}: session {session_path.name} uploaded ")

    def get_session_state(self, session_path):
        return self.session_json['info']['state']

    def receive_session_json_path_from_screen_model(self, session_path: Path, from_screen: str):
        self.session_json_path = session_path
        self.session_json = JsonStore(session_path)
        print(f"{__name__} recieved json path: {self.session_json_path} ")
        self.send_session_json_path_to_session_screen_view(session_path, from_screen, "session screen")
        self.send_session_json_path_to_models(session_path, "add data screen")

    def send_session_json_path_to_session_screen_view(self, session_path, back_screen, name_screen):
        for observer in self._observers:
            if observer.name == name_screen:
                observer.receive_session_json_path(session_path)
                state = self.get_session_state(session_path)
                if state == "completed":
                    observer.add_completed_sessions_widgets()
                elif state == "incomplete":
                    observer.add_incomplete_sessions_widgets(back_screen)

    def send_session_json_path_to_models(self, session_path: Path, name_screen: str) -> None:
        for observer in self._observers:
            if observer.name == name_screen:
                print('path to json: ', session_path)
                observer.model.receive_session_json_path(session_path)





