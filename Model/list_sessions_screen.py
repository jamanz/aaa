from Model.base_model import BaseScreenModel
from kivy import Logger
from pathlib import Path
import os
import glob

# todo: remove hint text on enter addDataScreen

class ListSessionsScreenModel(BaseScreenModel):
    json_storage_path = Path("assets", "data").resolve()

    def delete_session(self, session_sid):

        print(list(self.json_storage_path.glob('*.json')))
        for session_path in self.json_storage_path.glob('*.json'):

            if session_sid in session_path.name:
                os.remove(session_path)

    def send_path_to_session_screen(self, path):
        Logger.info(f"{__name__}: path: {path} was sent to session screen model")
        for observer in self._observers:
            if observer.name == "session screen":
                observer.model.receive_session_json_path_from_screen(path, "list sessions screen")
