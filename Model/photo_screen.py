from Model.base_model import BaseScreenModel
from kivy.logger import Logger

class PhotoScreenModel(BaseScreenModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")
