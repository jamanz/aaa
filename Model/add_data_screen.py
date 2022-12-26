from pathlib import Path

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
import json
from kivy.logger import Logger


class AddDataScreenModel(BaseScreenModel):
    session_json_path = None
    session_json = None

    def write_record_to_json(self, event, recod_dict: dict):
        self.session_json = JsonStore(self.session_json_path)
        session_name = self.session_json_path.stem
        updated_recs = [recod_dict] + self.session_json.get(session_name)['records']
        self.session_json.put(session_name, records=updated_recs)

        self.update_records_in_session_screen_view()

    def update_records_in_session_screen_view(self):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.update_records_in_tree_items()

    def receive_session_json_path(self, session_path: Path):
        self.session_json_path = session_path
