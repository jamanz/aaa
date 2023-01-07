# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.home_screen import HomeScreenModel
from Controller.home_screen import HomeScreenController
from Model.session_screen import SessionScreenModel
from Controller.session_screen import SessionScreenController
from Model.add_data_screen import AddDataScreenModel
from Controller.add_data_screen import AddDataScreenController
from Model.list_sessions_screen import ListSessionsScreenModel
from Controller.list_sessions_screen import ListSessionsScreenController
from Model.photo_screen import PhotoScreenModel
from Controller.photo_screen import PhotoScreenController

screens = {
    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },

    "session screen": {
        "model": SessionScreenModel,
        "controller": SessionScreenController,
    },

    "add data screen": {
        "model": AddDataScreenModel,
        "controller": AddDataScreenController,
    },

    "list sessions screen": {
        "model": ListSessionsScreenModel,
        "controller": ListSessionsScreenController,
    },

    "photo screen": {
        "model": PhotoScreenModel,
        "controller": PhotoScreenController,
    }
}