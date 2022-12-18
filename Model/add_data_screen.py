from pathlib import Path

from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
import json
from kivy.logger import Logger

"""
sessions_json = {
    "finished": ["session_id1.json", "session_id2.json"],
    "unfinished": ["session_id1.json", "session_id2.json"]
    }

session_id1_json = {
            "name": "user session name",
            "date": "date",
            "sid": "session_id",
            "state": "finished",
            "records": [
                {
                    "tree_number": "number",
                    "tree_specie": "specie",
                    # ......
                    "complete": True
                },
                {},
                {}
            ]
        }
"""


class AddDataScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.add_data_screen.AddDataScreen.AddDataScreenView` class.
    """

    #session_json_path = ObjectProperty()

    session_json_path = None

    def write_record_to_json(self, event, recod_dict: dict):
        self.session_json = JsonStore(self.session_json_path)
        session_name = self.session_json_path.stem
        updated_recs = self.session_json.get(session_name)['records'] + [recod_dict]
        Logger.info(f"{__name__}: session recs before: {self.session_json[session_name]['records']}")
        self.session_json.put(session_name, records=updated_recs)
        Logger.info(f"{__name__}: session recs after: {self.session_json[session_name]['records']}")

        del updated_recs
        self.update_records_in_session_view()

    def update_records_in_session_view(self):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.update_records_in_session_view()

    def receive_session_json_path(self, session_path: Path):
        self.session_json_path = session_path

        Logger.info(f"{__name__}: recieved json path: {self.session_json_path} ")

        # self.send_session_json_path_to_view(session_path, "add data screen")

