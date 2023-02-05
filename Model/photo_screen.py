from Model.base_model import BaseScreenModel
from kivy.logger import Logger
from kivy.properties import StringProperty


class PhotoScreenModel(BaseScreenModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")
        self.session_name = StringProperty()
        self.tree_name = StringProperty()

    def receive_tree_data_from_session_screen(self, ses_name, tree_name):
        self.session_name = ses_name
        self.tree_name = tree_name
