from View.base_screen import BaseScreenView
from View.AddDataScreen.components.addDataCard import addDataCard
# from main import logger
from kivy.logger import Logger
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
import weakref
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField
from kivy.uix.camera import Camera
from kivy.clock import Clock
from functools import partial
from kivy.core.window import Window


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
        Window.softinput_mode = ''

    def raise_window_for_comment(self, *args):
        Window.softinput_mode = 'pan'
        Logger.info(f'{__name__}: keyboard raised')

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


# todo: disable submit if tree num not set
class AddDataScreenView(BaseScreenView):
    app_bar_title = StringProperty('New Tree')
    suggestion_is_selected = BooleanProperty(False)
    feature_value_len = NumericProperty(0)
    data_card = ObjectProperty()

    is_new = BooleanProperty(True)

    def close_submit_dialog(self, event):
        self.submit_dialog.dismiss()
        Window.softinput_mode = ''

    def ok_submit_dialog(self, event):
        if self.ids.submit_record_dialog.ids.comments_id.text:
            self.ids.submit_record_dialog.set_comment(self.ids.submit_record_dialog.ids.comments_id.text)
        self.save_record_and_back_to_session_screen()
        self.submit_dialog.dismiss()

    def make_photo_for_tree(self):
        self.app.go_next_screen("add data screen", "photo screen")

    def show_submit_record_dialog(self):
        self.ids.submit_record_dialog.update_values(self.controller.get_record())
        Window.softinput_mode = 'pan'
        self.submit_dialog.open()

    def close_record_preview_dialog(self, event):
        self.record_preview_dialog.dismiss()


    def show_preview(self):
        self.ids.preview_dialog.update_values(self.controller.get_record())
        self.record_preview_dialog.open()

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
            elevation=2,
            ver_growth='down',
            radius=[0, 24, 24, 24],
            width_mult=4,
        )

        # Prepare record preview dialog
        close_preview_btn = MDFlatButton(text="Ok", on_release=self.close_record_preview_dialog)
        self.record_preview_dialog = MDDialog(title='Preview',
                                              size_hint=(.7, None),
                                              md_bg_color=self.app.theme_cls.accent_color,
                                              type="custom",
                                              content_cls=PreviewContent(),
                                              buttons=([close_preview_btn])
                                              )
        self.ids['preview_dialog'] = weakref.ref(self.record_preview_dialog.content_cls)


        # Prepare record submission dialog
        close_btn = MDFlatButton(text="Back", on_release=self.close_submit_dialog)
        ok_btn = MDRaisedButton(text="Ok", on_release=self.ok_submit_dialog, elevation=1)
        self.submit_dialog = MDDialog(title='Submit record',
                                 size_hint=(.7, None),
                                 md_bg_color=self.app.theme_cls.accent_color,
                                 type="custom",
                                 content_cls=SubmitRecordContent(),
                                 buttons=(close_btn, ok_btn),

                                 )

        self.ids['submit_record_dialog'] = weakref.ref(self.submit_dialog.content_cls)
        self.ids.submit_record_dialog.add_data_view = self

    def cancel_record(self):
        self.controller.clear_record()
        self.app.go_prev_screen()

        # reset color of feature buttons
        for k in self.dataCard.ids.keys():
            if '_btn' in k:
                self.dataCard.ids[k].md_bg_color = self.app.theme_cls.accent_color

    def save_record_and_back_to_session_screen(self):
        if self.controller.new_record_dict.get('Tree Number'):
            self.controller.write_record_to_json()
        self.controller.clear_record()
        self.app.go_prev_screen()


    def show_suggestions(self, list_of_suggestions: list[str]):
        self.suggestion_menu.items = []
        size = "14sp"
        menu_items = [
            {
                "text": f"[size={size}]{sugg}[/size]",
                "_txt_top_pad": "2dp",
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

        def run_anim(dt):
            if feature_key in self.feature_button_instance_map.keys():
                anim = Animation(md_bg_color=self.app.theme_cls.primary_color, duration=.3)
                anim.start(self.dataCard.chosen_feature_instance)

        if feature_key == 'Tree Number':
            self.model.send_tree_number_to_photoscreen(feature_value)

        if feature_key in self.feature_button_instance_map.keys():
            Clock.schedule_once(run_anim, .1)

        if feature_key == 'Tree specie':
            self.suggestion_menu.dismiss()

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
        Logger.info(f"{__name__}: on_pre_enter")
        self.dataCard.ids.input_field_id.disabled = True
        self.feature_value_len = 0
        Window.softinput_mode = ''
        self.dataCard.ids.input_field_id.text = ''
        self.dataCard.ids.input_field_id.hint_text = "Chose feature to input"
        self.dataCard.ids.input_field_id.helper_text = ''
        self.ids.submit_record_dialog.ids.comments_id.text = ''

        self.feature_button_instance_map = { 'Tree Number': None,
                                        'Tree specie': None,
                                        'Stem number': None,
                                        'Tree diameter': None,
                                        'Crown diameter': None,
                                        'Tree height': None}

        self.feature_segment_instance_map = {'Health condition': None,
                                        'Tree location': None,
                                        'Crown cone': None}

        # map features
        for k in self.dataCard.ids.keys():
            if '_btn' in k:
                self.feature_button_instance_map[self.dataCard.ids[k].text] = self.dataCard.ids[k]
            if 'segment' in k:
                self.feature_segment_instance_map[self.dataCard.ids[k].control_type] = self.dataCard.ids[k]

        # default colors
        for new_feature in self.feature_button_instance_map.keys():
            self.feature_button_instance_map[new_feature].md_bg_color = self.app.theme_cls.accent_color

        for new_feature in self.feature_segment_instance_map.keys():
            self.feature_segment_instance_map[new_feature].segment_color = self.app.theme_cls.accent_color
            print(f"ACTIVE SEGMENT OF {new_feature} is {self.feature_segment_instance_map[new_feature].current_active_segment}")

        # color features
        # colors for buttons and segment positions for existed record
        if self.controller.is_record_edited:
            for record_feature in self.controller.new_record_dict.keys():

                if record_feature in self.feature_button_instance_map.keys():
                    self.feature_button_instance_map[record_feature].md_bg_color = self.app.theme_cls.primary_color

                if record_feature in self.feature_segment_instance_map.keys():
                    self.feature_segment_instance_map[record_feature].segment_color = self.app.theme_cls.primary_color
                    segment_val = self.controller.new_record_dict.get(record_feature)
                    print('segment_val: ', segment_val)
                    self.feature_segment_instance_map[record_feature].preset_segment_panel_pos_from_val(segment_val)
        else:
            # reset color of feature buttons
            for new_feature in self.feature_button_instance_map.keys():
                self.feature_button_instance_map[new_feature].md_bg_color = self.app.theme_cls.accent_color
            for new_feature in self.feature_segment_instance_map.keys():
                self.feature_segment_instance_map[new_feature].segment_color = self.app.theme_cls.accent_color


        Logger.info(f"{__name__}: on_pre_enter fired ,ids: {self.ids.box_layout.ids}")
