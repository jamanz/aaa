from kivy.utils import platform

from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty, ListProperty, DictProperty
from pathlib import Path
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDFillRoundFlatButton
from kivy import Logger
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
import weakref
from kivymd.uix.list import IRightBodyTouch
from kivy.weakproxy import WeakProxy
from kivy.metrics import dp
from View.PhotoScreen.components.toast import Toast
import os


class PreviewRecordedTreeContent(MDBoxLayout):
    tree_number = StringProperty()
    tree_specie = StringProperty()
    stem_number = StringProperty()
    tree_diameter = StringProperty()
    crown_diameter = StringProperty()
    tree_height = StringProperty()

    health_condition = StringProperty()
    tree_location = StringProperty('X')
    crown_cone = StringProperty()
    crown_value = StringProperty()
    specie_value = StringProperty()

    def update_values(self, record):
        self.tree_number = str(record.get('Tree Number'))
        self.tree_specie = str(record.get('Tree specie'))
        self.stem_number = str(record.get('Stem number'))
        self.tree_diameter = str(record.get('Tree diameter'))
        self.crown_diameter = str(record.get('Crown diameter'))
        self.tree_height = str(record.get('Tree height'))

        self.health_condition = str(record.get('Health condition'))
        self.tree_location = str(record.get('Tree location'))
        self.crown_cone = str(record.get('Crown cone'))
        self.crown_value = str(record.get('Crown value'))
        self.specie_value = str(record.get('Specie value'))


class PreUploadDialogContent(MDBoxLayout):
    chosen_worksheet_title = StringProperty()
    number_of_records = NumericProperty(0)
    screen_view = ObjectProperty()

    def set_values(self, title: str, number_of_records: int):
        self.chosen_worksheet_title = title
        self.number_of_records = number_of_records


class TreeItemIconsContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class TreeItem(TwoLineAvatarIconListItem):
    id = NumericProperty()
    tree_page = ObjectProperty()
    can_delete = BooleanProperty(True)
    record_data = DictProperty()
    item = ObjectProperty()
    tree_name = StringProperty()
    preview_record_dialog = ObjectProperty()

    def show_tree_preview(self, item):
        self.item = item
        self.tree_page = self.parent.parent
        self.tree_page.chosen_item = item

        Logger.info(f"{__name__}: item pressed: {item.text}, tree page: {self.tree_page}")

        if self.tree_page.session_screen_view.current_session_state == 'incomplete':
            self.preview_record_dialog = self.tree_page.preview_record_dialog
            self.tree_page.preview_record_dialog.buttons = (self.tree_page.tree_preview_close_btn,
                                                            self.tree_page.tree_preview_edit_btn)

            self.tree_page.preview_record_dialog.ids.button_box.clear_widgets()
            #self.tree_page.preview_record_dialog.ids.button_box.padding = "20dp"
            self.tree_page.preview_record_dialog.create_buttons()

        else:
            self.preview_record_dialog = self.tree_page.preview_record_dialog
            self.tree_page.preview_record_dialog.buttons = ([self.tree_page.tree_preview_ok_btn])

            self.tree_page.preview_record_dialog.ids.button_box.clear_widgets()
            #self.tree_page.preview_record_dialog.ids.button_box.padding = "20dp"
            self.tree_page.preview_record_dialog.create_buttons()

        self.tree_page.preview_record_dialog.content_cls.update_values(self.item.record_data)
        self.tree_page.preview_record_dialog.open()

    def make_photo_for_tree(self, tree_item):
        print("Got: ", tree_item.tree_name)
        self.tree_page = self.parent.parent
        self.tree_page.session_screen_view.start_photo_for_tree(tree_item.tree_name)


    def delete_item(self, item):
        self.tree_page = self.parent.parent
        Logger.info(f"{__name__}: item: {item}, id: {item.id} gonna be deleted")
        self.tree_page.delete_item(item)


class TreeItemsPage(MDRecycleView):
    tree_items_list = ListProperty()
    session_screen_view = ObjectProperty()
    current_session_name = StringProperty()
    chosen_item = ObjectProperty()

    delete_item_index = NumericProperty()
    delete_item_title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: inited")

        self.tree_preview_close_btn = MDFlatButton(text="Cancel", on_release=self.close_dialog)
        self.tree_preview_edit_btn = MDFlatButton(text="Edit", on_release=self.edit_dialog)
        self.tree_preview_ok_btn = MDFlatButton(text="OK", on_release=self.close_dialog)

        self.preview_record_dialog = MDDialog(title='Recorded Tree Values',
                                              size_hint=(.7, None),
                                              type="custom",
                                              content_cls=PreviewRecordedTreeContent(),
                                              buttons=[self.tree_preview_ok_btn]
                                              )

        close_delete_dialog_btn = MDFlatButton(text="Cancel", on_release=self.close_delete_dialog)
        confirm_delete_dialog_btn = MDFlatButton(text="Confirm", on_release=self.confirm_delete_dialog)
        self.delete_dialog = MDDialog(title="Delete",
                                      type="alert",
                                      buttons=(close_delete_dialog_btn, confirm_delete_dialog_btn)
                                      )

    def close_delete_dialog(self, event):
        self.delete_dialog.dismiss()

    def confirm_delete_dialog(self, event):
        self.tree_items_list.pop(self.delete_item_index)
        self.update_items()
        self.session_screen_view.delete_record_in_tree_items(self.delete_item_index)
        self.delete_item_index = -1
        self.delete_dialog.dismiss()

    def close_dialog(self, event):
        print('Cancel Edit Rec')
        self.preview_record_dialog.dismiss()

    def edit_dialog(self, event):
        self.session_screen_view.start_record_editing(self.chosen_item)
        self.preview_record_dialog.dismiss()

    def delete_item(self, item):
        self.delete_item_index = item.id
        self.delete_item_title = item.text
        self.delete_dialog.title = f"Delete tree {self.delete_item_title}?"
        self.delete_dialog.open()

    def update_items(self, can_delete=True):
        Logger.info(f"{__name__}: items updated")
        self.data = [
            {'text': f"#{record.get('Tree Number')}",
             'tree_name': record.get('Tree Number'),
             #'secondary_text': "Photos [b]0/2[/b]",
             'secondary_text': f"{record.get('Tree specie')}",
             'id': int(i),
             #'_height': dp(30),

             'record_data': record,
             'can_delete': can_delete}
            for i, record in enumerate(self.tree_items_list)
        ]


class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session_json = None
    current_session_state = "incomplete"
    session_name = StringProperty()
    total_session_records = NumericProperty()

    app_bar_title = StringProperty()
    show_buttons = BooleanProperty(True)

    chosen_worksheet_title = StringProperty()

    def start_photo_for_tree(self, tree_name):
        self.model.send_tree_data_to_photo_screen(self.session_name, tree_name)
        Logger.info(f"{__name__}: platform {platform}")
        if platform == 'android':
            #Logger.info(f"{__name__}: andoid version {api_version}")
            from android import api_version
            if api_version < 29:
                Toast().show(f"Photo disabled.\nAndroid version is s{api_version}")
                Logger.info(f"{__name__}: Api version not enough - {api_version}, toast displayed")
            else:
                Toast().show("All cool")
                self.app.go_next_screen("session screen", "photo screen")
        else:
            self.app.go_next_screen("session screen", "photo screen")

    def close_upload_dialog(self, event):
        self.upload_dialog.dismiss()

    def confirm_upload_dialog(self, event):
        Logger.info(f"{__name__}: Chosen worksheet: {self.chosen_worksheet_title}")
        self.upload_session()
        self.upload_dialog.dismiss()
        self.app.go_prev_screen()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")
        Logger.info(f"{__name__}: Kivy pathes: "
                    f"KIVY_DATA_DIR: {os.environ.get('KIVY_DATA_DIR')}\n"
                    f"KIVY_MODULES_DIR: {os.environ.get('KIVY_MODULES_DIR')}\n"
                    f"KIVY_HOME: {os.environ.get('KIVY_HOME')}")

        # Prepare upload dialog
        close_btn = MDFlatButton(text="Cancel", on_release=self.close_upload_dialog)
        confirm_btn = MDFlatButton(text="Confirm", on_release=self.confirm_upload_dialog)
        self.upload_content_cls = PreUploadDialogContent()
        self.upload_content_cls.screen_view = self
        self.upload_dialog = MDDialog(title=f'Upload Session',
                                      anchor_x="center",
                                      type="custom",
                                      content_cls=self.upload_content_cls,
                                      buttons=(close_btn, confirm_btn)
                                      )
        self.ids['upload_dialog'] = weakref.ref(self.upload_dialog.content_cls)

    def start_record_editing(self, tree_item: TreeItem):
        Logger.info(f"{__name__}: data of tree item to edit - {tree_item.record_data}")
        tree_num = tree_item.record_data.get('Tree Number')
        if tree_num:
            self.model.start_record_editing(tree_num)
            self.go_to_add_data_screen()



    def start_upload_dialog(self):
        num_of_session_rec = self.total_session_records
        if self.model.chosen_worksheet is None:
            self.model.get_util_worksheet()


        self.session_name = self.path_to_json.stem.split('_')[0]
        ws_name = self.session_name
        self.upload_content_cls.set_values(ws_name, num_of_session_rec)
        self.upload_dialog.open()

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
        self.session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = self.session_name
        self.show_buttons = False

        records = self.current_session_json['data'].get('records')
        self.total_session_records = len(records)

        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items(can_delete=False)
        self.ids.tree_items_page.session_screen_view = self


        Logger.info(f"{__name__}: ended to add widgets for completed session")

    def add_incomplete_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widget for incomplete session")
        self.session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = self.session_name
        self.show_buttons = True
        records = self.current_session_json['data'].get('records')
        self.total_session_records = len(records)

        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items()
        self.ids.tree_items_page.session_screen_view = self

        Logger.info(f"{__name__}: ended to add widgets for incomplete session")

    def upload_session(self):
        self.controller.upload_session(self.path_to_json)
        # self.app.go_prev_screen()

    def go_to_add_data_screen(self):
        self.app.go_next_screen("session screen", "add data screen")

    def update_records_in_tree_items(self):
        self.current_session_json = JsonStore(self.path_to_json)
        records = self.current_session_json['data'].get('records')
        self.total_session_records = len(records)
        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items()
        self.ids.tree_items_page.refresh_from_data()

    def delete_record_in_tree_items(self, index):
        self.model.delete_record_in_tree_items(index)

