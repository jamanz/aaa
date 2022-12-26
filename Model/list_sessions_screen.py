from Model.base_model import BaseScreenModel
from kivy import Logger
from pathlib import Path


class ListSessionsScreenModel(BaseScreenModel):
    json_storage_path = Path("assets", "data").resolve()

    # def start_incomplete_sessions(self):
    #     Logger.info(f"{__name__}: start incomplete sessions")
    #     for observer in self._observers:
    #         if observer.name == "list sessions screen":
    #             observer.current_sessions_list_type = 'incomplete'
    #             observer.start_incomplete_sessions()
    #
    # def start_completed_sessions(self):
    #     Logger.info(f"{__name__}: start completed sessions")
    #     for observer in self._observers:
    #         if observer.name == "list sessions screen":
    #             observer.current_sessions_list_type = 'completed'
    #             observer.start_completed_sessions()

    def send_path_to_session_screen(self, path):
        Logger.info(f"{__name__}: path: {path} was sent to session screen model")
        for observer in self._observers:
            if observer.name == "session screen":
                observer.model.receive_session_json_path_from_screen(path, "list sessions screen")
