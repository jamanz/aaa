from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, ObjectProperty
from pathlib import Path
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFillRoundFlatButton
from kivy import Logger


class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session = None
    back_screen = StringProperty()
    app_bar_title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Initializing, kv ids: {self.ids}")

    def upload_session(self, event):
        self.app.manager_screens.current = "list sessions screen"
        self.controller.upload_session(self.path_to_json)

    def add_completed_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widget for completed session")
        self.ids.buttons_grid.clear_widgets()
        session_name = self.path_to_json.stem

        records = self.current_session[session_name].get('records')
        self.add_app_toolbar("list sessions screen")
        # self.app_bar_title = self.path_to_json.stem
        # self.back_screen = "list sessions screen"

        self.ids.item_grid.clear_widgets()
        for item in records:
            self.ids.item_grid.add_widget(
                OneLineListItem(text=str(item))
            )
        Logger.info(f"{__name__}: ended to add widgets for completed session")

    def add_incomplete_sessions_widgets(self, default_backscreen="home screen"):
        Logger.info(f"{__name__}: starting to add widget for incomplete session")
        session_name = self.path_to_json.stem
        records = self.current_session[session_name].get('records')
        # self.app_bar_title = self.path_to_json.stem
        # self.back_screen = "list sessions screen"
        self.add_app_toolbar(default_backscreen)
        self.add_buttons()

        self.ids.item_grid.clear_widgets()
        for item in records:
            self.ids.item_grid.add_widget(
                OneLineListItem(text=str(item))
            )
        Logger.info(f"{__name__}: ended to add widgets for incomplete session")

    def receive_session_json_path(self, session_path: Path):
        Logger.info(f"{__name__}: retrieved json path")
        self.path_to_json = session_path
        self.current_session = JsonStore(session_path)
        Logger.info(f"{__name__}: created JsonStore")

    def back_to_screen(self, screen):
        self.app.manager_screens.current = screen
        self.ids.app_bar.clear_widgets()
        Logger.info(f"{__name__}: user backed to {screen}")

    def add_app_toolbar(self, back_screen: str):
        Logger.info(f"{__name__}: app toolbar started with back_screen: {back_screen}")
        self.ids.app_bar.clear_widgets()
        self.ids.app_bar.add_widget(
            MDTopAppBar(title = self.path_to_json.stem,
                        type_height= "medium",
                        headline_text = "Headline",
                        left_action_items=
                            [["arrow-left", lambda x: self.back_to_screen(back_screen)]]
                        )
            )
        Logger.info(f"{__name__}: app toolbar done with back_screen: {back_screen}")

    def add_buttons(self):
        self.ids.buttons_grid.clear_widgets()
        self.ids.buttons_grid.add_widget(
            MDFillRoundFlatButton(
                text="New Record",
                size_hint=[.4, .8],
                on_release=self.go_to_add_data_screen
            )
        )

        self.ids.buttons_grid.add_widget(
            MDFillRoundFlatButton(
                text="Upload Session",
                size_hint=[.4, .8],
                on_release=self.upload_session
            )
        )
        Logger.info(f"{__name__}: buttons for new rec and upload added")

    def go_to_add_data_screen(self, event):
        # print("OPER BUTTON PRESSED: ", event)
        self.app.manager_screens.current = "add data screen"

    def update_records_in_session_view(self):
        Logger.info(f"{__name__}: update records func started")
        self.ids.item_grid.clear_widgets()
        session_name = self.path_to_json.stem
        self.current_session = JsonStore(self.path_to_json)
        records = self.current_session[session_name].get('records')

        for item in records:
            self.ids.item_grid.add_widget(
                OneLineListItem(text=str(item))
            )
        Logger.info(f"{__name__}: update records func ended, {len(records)} items added")

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
