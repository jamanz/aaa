import importlib
from kivy.storage.jsonstore import JsonStore
import secrets

import View.HomeScreen.home_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.HomeScreen.home_screen)




class HomeScreenController:
    """
    The `HomeScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        print("HS Controller")
        self.model = model  # Model.home_screen.HomeScreenModel
        self.view = View.HomeScreen.home_screen.HomeScreenView(controller=self, model=self.model)


    def get_view(self) -> View.HomeScreen.home_screen:
        return self.view

    def start_new_session(self, session_name, date):
        self.model.start_new_session(session_name, date)