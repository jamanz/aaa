from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from pathlib import Path
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFillRoundFlatButton
from kivy import Logger
from kivy.uix.recycleview import RecycleView


class TreeItem(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, item):
        Logger.info(f"{__name__}: item pressed: {item.text}")


class TreeItemsPage(RecycleView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tree_items_list = []

    def update_items(self, records: list[dict]):
        self.tree_items_list = records
        self.data = [{'text': str(record)} for record in records]



class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session_json = None
    current_session_state = "incomplete"
    app_bar_title = StringProperty()

    show_buttons = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def receive_session_json_path(self, session_path: Path):
        Logger.info(f"{__name__}: retrieved json path")
        self.path_to_json = session_path
        self.current_session_json = JsonStore(session_path)
        self.current_session_state = self.current_session_json['info']['state']

        if self.current_session_state == 'completed':
            self.add_completed_sessions_widgets()
        elif self.current_session_state == 'incomplete':
            self.add_incomplete_sessions_widgets()

    def add_completed_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widgets for completed session")
        # self.ids.buttons_grid.clear_widgets()
        session_name = self.path_to_json.stem
        self.app_bar_title = session_name
        self.show_buttons = False

        records = self.current_session_json[session_name].get('records')

        self.ids.tree_items_page.update_items(records)

        Logger.info(f"{__name__}: ended to add widgets for completed session")

    def add_incomplete_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widget for incomplete session")
        session_name = self.path_to_json.stem
        self.app_bar_title = session_name
        self.show_buttons = True
        records = self.current_session_json[session_name].get('records')

        self.ids.tree_items_page.update_items(records)

        Logger.info(f"{__name__}: ended to add widgets for incomplete session")

    def upload_session(self):
        self.controller.upload_session(self.path_to_json)
        self.app.go_prev_screen()

    def go_to_add_data_screen(self):
        self.app.go_next_screen("session screen", "add data screen")

    def update_records_in_tree_items(self):
        session_name = self.path_to_json.stem
        self.current_session_json = JsonStore(self.path_to_json)
        self.ids.tree_items_page.data = [{'text': str(record)} for record in self.current_session_json[session_name].get('records')]
        self.ids.tree_items_page.refresh_from_data()


