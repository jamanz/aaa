from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, ObjectProperty
from pathlib import Path
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFillRoundFlatButton


class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session = None
    back_screen = StringProperty()
    app_bar_title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"{__name__} inited")

    def upload_session(self, event):
        self.app.manager_screens.current = "list sessions screen"
        self.controller.upload_session(self.path_to_json)

    def add_completed_sessions_widgets(self):
        self.ids.buttons_grid.clear_widgets()
        session_name = self.path_to_json.stem
        print("adding completed sessions state: ", self.current_session["info"]["state"])
        records = self.current_session[session_name].get('records')
        self.add_app_toolbar("list sessions screen")
        # self.app_bar_title = self.path_to_json.stem
        # self.back_screen = "list sessions screen"

        self.ids.item_grid.clear_widgets()
        for item in records:
            self.ids.item_grid.add_widget(
                OneLineListItem(text=str(item))
            )

    def add_incomplete_sessions_widgets(self, default_backscreen="home screen"):
        print("adding incompleted sessions, state: ", self.current_session["info"]["state"])
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

    def receive_session_json_path(self, session_path: Path):
        self.path_to_json = session_path
        self.current_session = JsonStore(session_path)

    def back_to_screen(self, screen):
        self.app.manager_screens.current = screen
        self.ids.app_bar.clear_widgets()

    def add_app_toolbar(self, back_screen: str):

        self.ids.app_bar.clear_widgets()
        self.ids.app_bar.add_widget(
            MDTopAppBar(title = self.path_to_json.stem,
                        type_height= "medium",
                        headline_text = "Headline",
                        left_action_items=
                            [["arrow-left", lambda x: self.back_to_screen(back_screen)]]
                        )
            )

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

    def go_to_add_data_screen(self, event):
        print("OPER BUTTON PRESSED: ", event)
        self.app.manager_screens.current = "add data screen"

    def update_records_in_session_view(self):
        self.ids.item_grid.clear_widgets()
        session_name = self.path_to_json.stem
        self.current_session = JsonStore(self.path_to_json)
        records = self.current_session[session_name].get('records')
        print('records in SessScreenView: ', records)
        for item in records:
            self.ids.item_grid.add_widget(
                OneLineListItem(text=str(item))
            )

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
