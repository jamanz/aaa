from pathlib import Path

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
import json
from kivy.logger import Logger


class AddDataScreenModel(BaseScreenModel):
    session_json_path = None
    session_json = None

    def write_record_to_json(self, event, recod_dict: dict, record_edited=False):
        self.session_json = JsonStore(self.session_json_path)
        prev_records = self.session_json.get('data')['records']
        # remove from store old record
        if record_edited:
            remove_rec_name = recod_dict.get('Tree Number')
            for ind, rec in enumerate(prev_records):
                if rec.get('Tree Number') == remove_rec_name:
                    prev_records.pop(ind)
        updated_recs = [recod_dict] + prev_records
        self.session_json.put('data', records=updated_recs)

        self.update_records_in_session_screen_view()

    def update_records_in_session_screen_view(self):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.update_records_in_tree_items()

    def receive_session_json_path(self, session_path: Path):
        self.session_json_path = session_path

    def send_tree_number_to_photoscreen(self, tree_num):
        for observer in self._observers:
            if observer.name == "photo screen":
                observer.set_tree_name(tree_num)

    def get_record_for_edit_from_json_by_name(self, record_name: str):
        self.session_json = JsonStore(self.session_json_path)
        recs = self.session_json.get('data')['records']
        for ind, record in enumerate(recs):
            if record['Tree Number'] == record_name:
                edit_rec = recs.pop(ind)
                return edit_rec

