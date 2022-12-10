from Model.base_model import BaseScreenModel
from kivy.storage.jsonstore import JsonStore
import json

class AddDataScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.add_data_screen.AddDataScreen.AddDataScreenView` class.
    """
    new_record_json = JsonStore('new_record.json')

    def get_input_feature_value(self, feature_key, feature_value):
        # todo: виконати в контроллері перевірку і відправити далі моделі
        print(f"Model data recieved from Controller: {feature_key}, {feature_value}")

    def write_record_to_json(self, event, recod_dict: dict):
        print('RECORD adden to json store')
        self.new_record_json.put('new_rec', **recod_dict)

