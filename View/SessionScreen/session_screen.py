from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, OneLineAvatarIconListItem
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty, ListProperty
from pathlib import Path
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFillRoundFlatButton
from kivy import Logger
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
import weakref

from kivy.weakproxy import WeakProxy

class CustomWorkSheetListItem(MDRectangleFlatIconButton):
    item_id = StringProperty()
    icon_name = StringProperty()
    # parent = ObjectProperty()


class DialogForUploadContent(MDBoxLayout):
    chosen_worksheet = StringProperty()
    last_picked_id = StringProperty()
    screen_view = ObjectProperty()
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.populate_with_available_ws_buttons()

    def pick_worksheet(self, instance):
        print(f"last picked id: {self.last_picked_id}")
        # if self.last_picked_id:
        #     self.ids[self.last_picked_id].icon_name = ''
        #     self.ids[instance.id].icon_name = 'arrow-left-bottom'
        #     self.last_picked_id = instance.id
        # else:
        #     self.last_picked_id = instance.id
        #     self.ids[instance.id].icon_name = 'arrow-left-bottom'
        if self.last_picked_id:
            self.ids[self.last_picked_id].icon_color = 'white'
            self.ids[instance.id].icon_color = 'green'
            self.last_picked_id = instance.id
        else:
            self.last_picked_id = instance.id
            self.ids[instance.id].icon_color = 'green'
        self.screen_view.worksheet_to_upload = instance.text

    def populate_with_available_ws_buttons(self):
        available_ws = self.screen_view.get_list_of_available_ws()
        print(f"Available WS: {available_ws}")
        for i, ws in enumerate(available_ws):
            ws_button = CustomWorkSheetListItem(
                    text=f'{ws.title}',
                    id=ws.title,
                    on_release=self.pick_worksheet
                )
            self.ids[ws_button.id] = WeakProxy(ws_button)
            self.ids.ws_buttons_layout.add_widget(
                ws_button
            )




class TreeItem(OneLineAvatarIconListItem):
    id = NumericProperty()
    tree_page = ObjectProperty()
    can_delete = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def callback(self, item):
        Logger.info(f"{__name__}: item pressed: {item.text}")

    def delete_item(self, item):
        self.tree_page = self.parent.parent
        Logger.info(f"{__name__}: item: {item}, id: {item.id} gonna be deleted")
        self.tree_page.delete_item(item.id)


class TreeItemsPage(MDRecycleView):
    tree_items_list = ListProperty()
    session_screen_view = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_item(self, index):
        self.session_screen_view = self.parent.parent
        self.tree_items_list.pop(index)
        self.update_items()
        self.session_screen_view.delete_record_in_tree_items(index)

    def update_items(self, can_delete=True):
        Logger.info(f"{__name__}: items updated")
        self.data = [
            {'text': str(record),
             'id': int(i),
             'can_delete': can_delete}
            for i, record in enumerate(self.tree_items_list)]


class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session_json = None
    current_session_state = "incomplete"

    app_bar_title = StringProperty()
    show_buttons = BooleanProperty(True)

    worksheet_to_upload = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def start_upload_dialog(self):
        def close_dialog(event):
            self.upload_dialog.dismiss()

        def confirm_dialog(event):
            Logger.info(f"{__name__}: Chosen worksheet: {self.worksheet_to_upload}")
            if self.worksheet_to_upload == '':
                self.upload_session()
            else:
                self.set_worksheet_in_model(self.worksheet_to_upload)
                self.upload_session()
                self.upload_dialog.dismiss()
                self.app.go_prev_screen()

        close_btn = MDFlatButton(text="Cancel", on_release=close_dialog)
        confirm_btn = MDFlatButton(text="Confirm", on_release=confirm_dialog)
        content_cls = DialogForUploadContent()
        content_cls.screen_view = self
        content_cls.populate_with_available_ws_buttons()
        self.upload_dialog = MDDialog(title='Choose Google worksheet to upload',
                               size_hint=(.6, .5),
                               type="custom",
                               content_cls=content_cls,
                               buttons=(close_btn, confirm_btn)
                               )
        self.ids['upload_dialog'] = weakref.ref(self.upload_dialog.content_cls)
        self.upload_dialog.open()

    def set_worksheet_in_model(self, worksheet_title):
        self.model.set_chosen_worksheet(worksheet_title)

    def get_list_of_available_ws(self):
        return self.model.list_available_worksheets()

    def receive_session_json_path(self, session_path: Path):
        Logger.info(f"{__name__}: retrieved json path")
        self.path_to_json = session_path
        self.current_session_json = JsonStore(session_path)

        self.current_session_state = self.current_session_json.get('info')['state']

        if self.current_session_state == 'completed':
            self.add_completed_sessions_widgets()
        elif self.current_session_state == 'incomplete':
            self.add_incomplete_sessions_widgets()

    def add_completed_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widgets for completed session")
        # self.ids.buttons_grid.clear_widgets()
        session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = session_name
        self.show_buttons = False

        records = self.current_session_json['data'].get('records')

        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items(can_delete=False)

        Logger.info(f"{__name__}: ended to add widgets for completed session")

    def add_incomplete_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widget for incomplete session")
        session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = session_name
        self.show_buttons = True
        records = self.current_session_json['data'].get('records')

        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items()

        Logger.info(f"{__name__}: ended to add widgets for incomplete session")

    def upload_session(self):
        self.controller.upload_session(self.path_to_json)
        # self.app.go_prev_screen()

    def go_to_add_data_screen(self):
        self.app.go_next_screen("session screen", "add data screen")

    def update_records_in_tree_items(self):
        self.current_session_json = JsonStore(self.path_to_json)
        records = self.current_session_json['data'].get('records')
        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items()
        self.ids.tree_items_page.refresh_from_data()

    def delete_record_in_tree_items(self, index):
        self.model.delete_record_in_tree_items(index)

