from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, StringProperty
from pathlib import Path
import os
from kivy.logger import Logger
from Utility.google_sheets import next_available_row, get_g_sheet
from collections import OrderedDict


features_name_to_sheets_columns_map = OrderedDict({
    'Tree Number': 'A',
    'Tree specie': 'B',
    'Stem number': 'C',
    'Tree diameter': 'D',
    'Crown diameter': 'E',
    'Height': 'F'
})




class SessionScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.session_screen.SessionScreen.SessionScreenView` class.
    """

    #_session_json_path = ObjectProperty()

    def __init__(self):
        self.session_json_path = None
        self.g_sheet = get_g_sheet()

    def upload_records_to_sheet(self, records):
        Logger.info(f"{__name__}: current worksheet: {self.g_sheet}")
        free_row_i = next_available_row(self.g_sheet)
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

        self.g_sheet.batch_update(batch)
        Logger.info(f"{__name__}: Batch sent to Google Sheet")


    def upload_session(self, session_path: Path):
        self.session_json = JsonStore(session_path)
        self.session_json.put("info", state="completed")

        session_name = session_path.stem
        session_records = self.session_json.get(session_name)['records']
        self.upload_records_to_sheet(session_records)

        # move to completed directory
        new_path = Path(session_path.parent, "completed", session_path.name)
        os.rename(session_path, new_path)
        Logger.info(f"{__name__}: session {session_path.name} uploaded ")

    def get_session_state(self, session_path):
        return self.session_json['info']['state']

    def receive_session_json_path_from_screen_model(self, session_path: Path, from_screen: str):
        Logger.info(f"{__name__}: recieved from {from_screen} json path: {self.session_json_path} ")
        self.session_json_path = session_path
        self.session_json = JsonStore(session_path)
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
        Logger.info(f"{__name__}: passed signal to session screen view successfully")

    def send_session_json_path_to_models(self, session_path: Path, name_screen: str) -> None:
        for observer in self._observers:
            if observer.name == name_screen:
                print('path to json: ', session_path)
                observer.model.receive_session_json_path(session_path)
        Logger.info(f'{__name__}: sent json path to {name_screen} model')




