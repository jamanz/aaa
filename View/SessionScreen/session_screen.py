from kivy.storage.jsonstore import JsonStore

from View.base_screen import BaseScreenView
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, OneLineAvatarIconListItem
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

from kivy.weakproxy import WeakProxy

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



class TreeItem(OneLineAvatarIconListItem):
    id = NumericProperty()
    tree_page = ObjectProperty()
    can_delete = BooleanProperty(True)
    record_data = DictProperty()
    item = ObjectProperty()

    def show_tree_preview(self, item):
        def close_dialog(event):
            print('Cancel Edit Rec')
            self.preview_record_dialog.dismiss()

        def edit_dialog(event):
            print(f"Edit dialog env, {self.tree_page.session_screen_view}")
            self.tree_page.session_screen_view.start_record_editing(item)
            self.preview_record_dialog.dismiss()

        self.item = item
        self.tree_page = self.parent.parent
        Logger.info(f"{__name__}: item pressed: {item.text}, tree page: {self.tree_page}")

        close_btn = MDFlatButton(text="Cancel", on_release=close_dialog)
        edit_btn = MDFlatButton(text="Edit", on_release=edit_dialog)

        ok_btn = MDFlatButton(text="OK", on_release=close_dialog)

        if self.tree_page.session_screen_view.current_session_state == 'incomplete':
            self.preview_record_dialog = MDDialog(title='Recorded Tree Values',
                                                   size_hint=(.7, None),
                                                   type="custom",
                                                   content_cls=PreviewRecordedTreeContent(),
                                                   buttons=(close_btn, edit_btn)
                                                   )
        else:
            self.preview_record_dialog = MDDialog(title='Recorded Tree Values',
                                                  size_hint=(.7, None),
                                                  type="custom",
                                                  content_cls=PreviewRecordedTreeContent(),
                                                  buttons=([ok_btn])
                                                  )
        self.preview_record_dialog.content_cls.update_values(item.record_data)
        self.preview_record_dialog.open()


    def delete_item(self, item):
        self.tree_page = self.parent.parent
        Logger.info(f"{__name__}: item: {item}, id: {item.id} gonna be deleted")
        self.tree_page.delete_item(item.id)


class TreeItemsPage(MDRecycleView):
    tree_items_list = ListProperty()
    session_screen_view = ObjectProperty()


    def delete_item(self, index):
        self.session_screen_view = self.parent.parent
        self.tree_items_list.pop(index)
        self.update_items()
        self.session_screen_view.delete_record_in_tree_items(index)

    def update_items(self, can_delete=True):
        Logger.info(f"{__name__}: items updated")
        self.data = [
            #'text': f"#{record.get('Tree Number')} with {len(record)} points"
            {'text': f"#{record.get('Tree Number')}",
             'id': int(i),
             'record_data': record,
             'can_delete': can_delete}
            for i, record in enumerate(self.tree_items_list)]


class SessionScreenView(BaseScreenView):
    path_to_json = ObjectProperty()
    current_session_json = None
    current_session_state = "incomplete"

    total_session_records = NumericProperty()

    app_bar_title = StringProperty()
    show_buttons = BooleanProperty(True)

    chosen_worksheet_title = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def start_record_editing(self, tree_item: TreeItem):
        Logger.info(f"{__name__}: data of tree item to edit - {tree_item.record_data}")
        tree_num = tree_item.record_data.get('Tree Number')
        if tree_num:
            self.model.start_record_editing(tree_num)
            self.go_to_add_data_screen()

    def start_upload_dialog(self):
        def close_dialog(event):
            self.upload_dialog.dismiss()

        def confirm_dialog(event):
            Logger.info(f"{__name__}: Chosen worksheet: {self.chosen_worksheet_title}")
            self.upload_session()
            self.upload_dialog.dismiss()
            self.app.go_prev_screen()

        close_btn = MDFlatButton(text="Cancel", on_release=close_dialog)
        confirm_btn = MDFlatButton(text="Confirm", on_release=confirm_dialog)

        content_cls = PreUploadDialogContent()
        content_cls.screen_view = self

        num_of_session_rec = self.total_session_records

        if self.model.chosen_worksheet is None:
            self.model.get_util_worksheet()

        worksheetname = self.model.worksheet_title
        session_name = self.path_to_json.stem.split('_')[0]

        content_cls.set_values(worksheetname, num_of_session_rec)

        self.upload_dialog = MDDialog(title=f'Upload Session: {session_name}',
                               #size_hint=(.6, .5),
                               #height="300dp",
                               type="custom",
                               content_cls=content_cls,
                               buttons=(close_btn, confirm_btn)
                               )
        self.ids['upload_dialog'] = weakref.ref(self.upload_dialog.content_cls)
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
        session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = session_name
        self.show_buttons = False

        records = self.current_session_json['data'].get('records')
        self.total_session_records = len(records)

        self.ids.tree_items_page.tree_items_list = records
        self.ids.tree_items_page.update_items(can_delete=False)
        self.ids.tree_items_page.session_screen_view = self

        Logger.info(f"{__name__}: ended to add widgets for completed session")

    def add_incomplete_sessions_widgets(self):
        Logger.info(f"{__name__}: starting to add widget for incomplete session")
        session_name = self.path_to_json.stem.split('_')[0]
        self.app_bar_title = session_name
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

