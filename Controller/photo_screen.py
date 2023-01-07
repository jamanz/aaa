import View.PhotoScreen.photo_screen
from kivy.logger import Logger


class PhotoScreenController:
    def __init__(self, model):
        Logger.info(f"{__name__}: Inited")
        self.model = model  # Model.home_screen.HomeScreenModel
        self.view = View.PhotoScreen.photo_screen.PhotoScreenView(controller=self, model=self.model)

    def get_view(self) -> View.PhotoScreen.photo_screen:
        return self.view
