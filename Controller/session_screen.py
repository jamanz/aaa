import importlib

import View.SessionScreen.session_screen

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.SessionScreen.session_screen)




class SessionScreenController:
    """
    The `SessionScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.session_screen.SessionScreenModel
        self.view = View.SessionScreen.session_screen.SessionScreenView(controller=self, model=self.model)

    def get_view(self) -> View.SessionScreen.session_screen:
        return self.view

    def upload_session(self, session_path):
        self.model.upload_session(session_path)


