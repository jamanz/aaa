from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, StringProperty
from pathlib import Path
import os
from kivy.logger import Logger
from Utility.google_sheets import (next_available_row, features_name_to_sheets_columns_map,
                                   get_g_sheet_client, get_g_sheet_client_sheet_list)
from kivy.clock import Clock


class SessionScreenModel(BaseScreenModel):
    session_json = None
    session_json_path = None
    g_sheet_client = None
    chosen_worksheet = None

    def __init__(self):
        #schedule connection to Google Sheets
        Clock.schedule_once(self.init_g_sheet_client, 3)
        self.chosen_worksheet = StringProperty('worksheet1')
        Logger.info(f"{__name__}: Inited")

    def init_g_sheet_client(self, dt):
        self.g_sheet_client = get_g_sheet_client()
        Logger.info(f"{__name__}: async Google sheets inited")
        #return True

    def list_available_worksheets(self):
        return get_g_sheet_client_sheet_list(self.g_sheet_client)

    def set_chosen_worksheet(self, worksheet_title):
        print(f"getted: {worksheet_title}, with type: {type(worksheet_title)}")
        self.chosen_worksheet = worksheet_title

    def upload_records_to_sheet(self, records):
        Logger.info(f"{__name__}: current GSheet client: {self.g_sheet_client}")
        free_row_i = next_available_row(self.g_sheet_client.worksheet(self.chosen_worksheet))
        Logger.info(f"{__name__}: first free row at index: {free_row_i}")
        batch = []

        for record in records:
            values = []
            for feature in features_name_to_sheets_columns_map.keys():
                feature_val = record.get(feature)
                if feature_val:
                    values.append(feature_val)
                else:
                    values.append('NONE')

            batch.append(
                {
                    'range': f'A{free_row_i}:F{free_row_i}',
                    'values': [values]
                }
            )
            free_row_i += 1

        self.g_sheet_client.worksheet(self.chosen_worksheet).batch_update(batch)
        Logger.info(f"{__name__}: Batch sent to Google Sheet")

    def delete_record_in_tree_items(self, index):
        self.session_json = JsonStore(self.session_json_path)
        records = self.session_json.get('data')['records']
        removed = records.pop(index)
        Logger.info(f"{__name__}: item {removed} with index {index} was deleted from JsonStore")
        self.session_json.put('data', records=records)

    def upload_session(self, session_path: Path):
        self.session_json = JsonStore(session_path, indent=4)
        info = self.session_json.get("info")
        info['state'] = "completed"
        self.session_json.put("info", **info)

        session_name = session_path.stem
        session_records = self.session_json.get('data')['records']
        self.upload_records_to_sheet(session_records)

        # move to completed directory
        new_path = Path(session_path.parent, "completed", session_path.name)
        os.rename(session_path, new_path)
        Logger.info(f"{__name__}: session {session_path.name} uploaded ")

    def receive_session_json_path_from_screen(self, session_path: Path, from_screen: str):
        Logger.info(f"{__name__}: json path: {self.session_json_path}, received from {from_screen}")

        self.session_json_path = session_path
        self.session_json = JsonStore(session_path)

        self.send_session_json_path_to_session_screen_view(session_path)
        self.send_session_json_path_to_add_data_screen_model(session_path)

    def send_session_json_path_to_session_screen_view(self, session_path):
        for observer in self._observers:
            if observer.name == "session screen":
                observer.receive_session_json_path(session_path)

    def send_session_json_path_to_add_data_screen_model(self, session_path):
        for observer in self._observers:
            if observer.name == "add data screen":
                observer.model.receive_session_json_path(session_path)
