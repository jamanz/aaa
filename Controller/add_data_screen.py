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
    tree_suggestions_df = pd.read_csv(tree_values_path, index_col=False)[['value', 'latin_name']]
    # columns = defaultdict(list)
    # tree_suggestions = None


    def __init__(self, model):
        self.model = model  # Model.add_data_screen.AddDataScreenModel
        self.view = View.AddDataScreen.add_data_screen.AddDataScreenView(controller=self, model=self.model)

        # with open(self.tree_values_path) as f:
        #     reader = csv.DictReader(f)  # read rows into a dictionary format
        #     for row in reader:  # read a row as {column1: value1, column2: value2,...}
        #         for (k, v) in row.items():  # go over each column name and value
        #             self.columns[k].append(v)
        # self.tree_suggestions = self.columns['latin_name']

        self.new_record_dict = {}

    def clear_record(self):
        self.new_record_dict.clear()

    def get_record(self):
        return self.new_record_dict

    def get_input_feature_value(self, feature_key, feature_value):
        self.new_record_dict[feature_key] = feature_value

    def find_suggestions(self, text: str)->list[str]:
        out_df = self.tree_suggestions_df[self.tree_suggestions_df['latin_name'].str.contains(text)]
        # print("out df: ", out_df['latin_name'].tolist())
        # return list(filter(lambda sugg: sugg.lower().startswith(text.lower()), self.tree_suggestions_df))
        return out_df['latin_name'].tolist()


    def write_record_to_json(self):
        self.model.write_record_to_json(self, self.new_record_dict)
        self.new_record_dict.clear()

    def get_suggestions_for_input(self, feature_value: str) -> list[str]:
        pass

    def get_view(self) -> View.AddDataScreen.add_data_screen:
        return self.view
