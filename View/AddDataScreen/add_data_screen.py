from View.base_screen import BaseScreenView
from View.AddDataScreen.components.addDataCard import addDataCard
# from main import logger
from kivy.logger import Logger
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import weakref
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField
from kivy.uix.camera import Camera



class PreviewContent(MDBoxLayout):
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


class SubmitRecordContent(MDBoxLayout):
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

    comment = StringProperty()
    add_data_view = ObjectProperty()

    def set_comment(self, comment_str):
        self.comment = comment_str
        self.add_data_view.get_input_feature_value('Comment', comment_str)

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

        self.comment = record.get('Comment', '')



class AddDataScreenView(BaseScreenView):
    app_bar_title = StringProperty('New Tree')
    suggestion_is_selected = BooleanProperty(False)
    feature_value_len = NumericProperty(0)

    def make_photo_for_tree(self):
        self.app.go_next_screen("add data screen", "photo screen")

    def show_submit_record_dialog(self):

        def close_dialog(event):
            self.submit_dialog.dismiss()

        def ok_dialog(event):
            self.ids.submit_record.set_comment(self.ids.submit_record.ids.comments_id.text)
            # self.get_input_feature_value('Comment', self.ids.submit_record.ids.comments_id.text)
            self.save_record_and_back_to_session_screen()
            self.submit_dialog.dismiss()

        close_btn = MDFlatButton(text="Back", on_release=close_dialog)
        ok_btn = MDFlatButton(text="Ok", on_release=ok_dialog)

        self.submit_dialog = MDDialog(title='Submit record',
                               size_hint=(.7, None),
                               md_bg_color=self.app.theme_cls.accent_color,
                               type="custom",
                               content_cls=SubmitRecordContent(),
                               buttons=(close_btn, ok_btn)
                               )
        self.ids['submit_record'] = weakref.ref(self.submit_dialog.content_cls)
        self.ids.submit_record.add_data_view = self
        self.ids.submit_record.update_values(self.controller.get_record())
        self.submit_dialog.open()


    def show_preview(self):

        def close_dialog(event):
            self.dialog.dismiss()

        def ok_dialog(event):
            self.dialog.dismiss()

        close_btn = MDFlatButton(text="Back", on_release=close_dialog)
        ok_btn = MDFlatButton(text="Ok", on_release=ok_dialog)

        self.dialog = MDDialog(title='Preview',
                               size_hint=(.7, None),
                               md_bg_color=self.app.theme_cls.accent_color,
                               type="custom",
                               content_cls=PreviewContent(),
                               buttons=(close_btn, ok_btn)
                               )
        self.ids['preview_dialog'] = weakref.ref(self.dialog.content_cls)
        self.ids.preview_dialog.update_values(self.controller.get_record())
        self.dialog.open()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

        self.dataCard = addDataCard()
        self.dataCard.add_data_view = self
        self.ids.box_layout.add_widget(self.dataCard)

        self.suggestion_menu = MDDropdownMenu(
            caller=self.dataCard.ids.input_field_id,
            background_color=self.app.theme_cls.accent_color,
            position="bottom",
            width_mult=5,
        )

    def cancel_record(self):
        self.controller.clear_record()
        self.app.go_prev_screen()

    def save_record_and_back_to_session_screen(self):
        self.controller.write_record_to_json()
        self.app.go_prev_screen()

    def show_suggestions(self, list_of_suggestions: list[str]):
        self.suggestion_menu.items = []
        menu_items = [
            {
                "text": f"{sugg}",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=f"{sugg}": self.suggestion_menu_callback(x),
            } for sugg in list_of_suggestions
        ]
        self.suggestion_menu.items = menu_items
        # if not self.suggestion_is_selected:
        self.suggestion_menu.open()

    def suggestion_menu_callback(self, text_item):
        self.dataCard.ids.input_field_id.text = text_item
        print("text in field seted in menu callback")
        # self.dataCard.ids.input_field_id.on_text_validate('Tree specie', text_item)
        self.get_input_feature_value('Tree specie', text_item)
        self.suggestion_is_selected = True
        self.suggestion_menu.dismiss()
        print('menu dissmised in callback')

    def get_input_feature_value(self, feature_key, feature_value):
        if feature_key == 'Tree Number':
            self.model.send_tree_number_to_photoscreen(feature_value)
        self.controller.get_input_feature_value(feature_key, feature_value)

    def initiate_suggestions(self, feature_key, feature_value):
        self.suggestion_menu.dismiss()
        if feature_key == 'Tree specie' and len(feature_value) > 2:
            #if in Text field was inserted text
            if len(feature_value) - self.feature_value_len > 1:
                self.suggestion_menu.dismiss()
            else:
                suggests = self.controller.find_suggestions(feature_value)
                if len(suggests) < 1:
                    suggests.append(feature_value)
                self.show_suggestions(suggests)

        self.feature_value_len = len(feature_value)

    def on_pre_enter(self, *args):
        self.feature_value_len = 0
        self.dataCard.ids.input_field_id.text = ''
        self.dataCard.ids.input_field_id.hint_text = "Chose feature to input"
        Logger.info(f"{__name__}: on_pre_enter fired ,ids: {self.ids.box_layout.ids}")