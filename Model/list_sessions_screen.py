from Model.base_model import BaseScreenModel
from pathlib import Path
from kivy import Logger

class ListSessionsScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.list_sessions_screen.ListSessionsScreen.ListSessionsScreenView` class.
    """

    def start_incomplete_sessions(self):
        Logger.info(f"{__name__}: start_incomplete_sessions")
        for observer in self._observers:
            if observer.name == "list sessions screen":
                observer.current_sessions_list_type = 'incomplete'
                observer.start_incomplete_sessions()

    def start_completed_sessions(self):
        for observer in self._observers:
            if observer.name == "list sessions screen":
                observer.current_sessions_list_type = 'completed'
                observer.start_completed_sessions()

    def send_path_to_session_screen(self, path):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.model.receive_session_json_path_from_screen_model(path, "list sessions screen")
                # observer.add_completed_session_widgets()