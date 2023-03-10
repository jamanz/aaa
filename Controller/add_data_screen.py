import importlib

import View.AddDataScreen.add_data_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
# importlib.reload(View.AddDataScreen.add_data_screen)
import pandas as pd
import pathlib
# import csv
# from collections import defaultdict


class AddDataScreenController:
    """
    The `AddDataScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """
    tree_values_path = pathlib.Path("assets", "tree_values.csv").resolve()
    tree_suggestions_df = pd.read_csv(tree_values_path, index_col=False)[['value', 'latin_name', 'heb_name']]
    # columns = defaultdict(list)
    # tree_suggestions = None
    is_record_edited = False

    def __init__(self, model):
        self.model = model  # Model.add_data_screen.AddDataScreenModel
        self.view = View.AddDataScreen.add_data_screen.AddDataScreenView(controller=self, model=self.model)
        self.new_record_dict = {}

    def clear_record(self):
        self.new_record_dict.clear()

    def get_record(self):
        return self.new_record_dict

    def update_record(self, new_record: dict):
        self.new_record_dict = new_record
        self.is_record_edited = True

    def get_input_feature_value(self, feature_key, feature_value):
        self.new_record_dict[feature_key] = feature_value
        if self.new_record_dict.get('Crown cone') and self.new_record_dict.get('Crown diameter'):

            self.new_record_dict['Crown value'] = \
                self.calculate_crown_value(self.new_record_dict['Crown cone'], self.new_record_dict['Crown diameter'])
        if self.new_record_dict.get('Tree specie') and not self.new_record_dict.get('Specie value'):
            specie = self.new_record_dict.get('Tree specie')
            if specie in self.tree_suggestions_df['latin_name'].values:
                tree_specie_value_df = self.tree_suggestions_df.loc[self.tree_suggestions_df['latin_name'] == specie]
                tree_specie_value = tree_specie_value_df['value'].tolist()[0]
                self.new_record_dict['Specie value'] = tree_specie_value
            else:
                pass

    def calculate_crown_value(self, crown_cone: str, crown_diameter: str):
        value = 0
        if float(crown_diameter) > 12:
            value = 5
        elif 8 < float(crown_diameter) <= 12:
            value = 4 if crown_cone == 'No' else 5
        elif 4 < float(crown_diameter) <= 8:
            value = 3 if crown_cone == 'No' else 5
        elif 2 < float(crown_diameter) <= 4:
            value = 2 if crown_cone == 'No' else 4
        elif float(crown_diameter) <= 2:
            value = 1 if crown_cone == 'No' else 3
        else:
            value = -1
        return value

    def find_eng_suggestions(self, text: str)->list[str]:
        out_df = self.tree_suggestions_df[self.tree_suggestions_df['latin_name'].str.contains(text)]
        # print("out df: ", out_df['latin_name'].tolist())
        # return list(filter(lambda sugg: sugg.lower().startswith(text.lower()), self.tree_suggestions_df))
        return out_df['latin_name'].tolist()

    def find_heb_suggestions(self, text: str)->list[str]:
        out_df = self.tree_suggestions_df[self.tree_suggestions_df['heb_name'].str.contains(text)]
        # print("out df: ", out_df['latin_name'].tolist())
        # return list(filter(lambda sugg: sugg.lower().startswith(text.lower()), self.tree_suggestions_df))
        return out_df['heb_name'].tolist()


    def write_record_to_json(self):
        self.model.write_record_to_json(self, self.new_record_dict, record_edited=self.is_record_edited)
        self.new_record_dict.clear()
        self.is_record_edited = False

    def get_suggestions_for_input(self, feature_value: str) -> list[str]:
        pass

    def get_view(self) -> View.AddDataScreen.add_data_screen:
        return self.view
