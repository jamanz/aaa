from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty, NumericProperty,ListProperty
from kivy import Logger
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RectangularElevationBehavior
)
import unicodedata
from kivymd.uix.textfield import MDTextField


from kivy import app
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.recycleview import MDRecycleView
from kivy.app import App


class MySegmentedControl(MDSegmentedControl):
    custom_panel_width = NumericProperty(25)
    control_type = StringProperty('')

    health_cond_vals = ['0', '1', '2', '3', '4', '5']
    tree_loc_vals = ['X', '1', '2', '3', '4', '5']
    crown_cone_vals = ['Yes', 'No']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._segment_switch_x = 6

    def on_custom_panel_width(self, *args):
        Logger.info(f"{__name__}: basic seg switch: {self.ids.segment_switch.width}")
        self.ids.segment_panel.width = self.custom_panel_width
        if self.control_type == 'Health condition':
            #self.ids.segment_switch.width = 70# self.ids.segment_panel.width/(len(self.health_cond_vals)-1)
            Logger.info(f"{__name__}: changed seg switch: {self.ids.segment_switch.width}")

        # self._segment_switch_x = f"{float(self.custom_panel_width[:-2]) - 6}dp"

    def preset_segment_panel_pos_from_val(self, val):
        Logger.info(f"{__name__}: preset activated")
        if self.control_type == 'Health condition':
            ind = self.health_cond_vals.index(val)
            self._segment_switch_x = ind*(float(self.ids.segment_panel.width)/len(self.health_cond_vals)) + 6
        elif self.control_type == 'Tree location':
            ind = self.tree_loc_vals.index(val)
            self._segment_switch_x = ind*(float(self.ids.segment_panel.width)/len(self.tree_loc_vals)) + 6
        elif self.control_type == 'Crown cone':
            ind = self.crown_cone_vals.index(val)
            self._segment_switch_x = ind * (float(self.ids.segment_panel.width) / len(self.crown_cone_vals)) + 6

    def on_active(self,*args, ) -> None:
        '''Called when the segment is activated.'''

        if len(args) == 1:
            control_value = args[0].text
            control_object_label = args[0].parent.parent.control_type
            #print("screen parent: ", )
            self.parent.parent.parent.add_data_view.get_input_feature_value(control_object_label, control_value)
            print(f"parent: {self.parent}")
            self.segment_color = self.parent.parent.parent.add_data_view.app.theme_cls.primary_color

class FeatureButton(MDFillRoundFlatButton):
    pass

class HebrewTextField(MDTextField):
    #font_name_hint_text = "Arimo"
    #font_name = "Arimo"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addDataCard = None
        Clock.schedule_once(self.set_heb_font)

    def set_heb_font(self, dt):
        print("hint text set: ", self.hint_text)

    def check_hebrew(self, term):
        for i in set(term):
            if 'HEBREW' in unicodedata.name(i):
                return True
        return False





class addDataCard(MDCard, RoundedRectangularElevationBehavior): #RectangularElevationBehavior
    chosen_feature = StringProperty()
    chosen_feature_instance = ObjectProperty()
    shadow_animation = ObjectProperty()
    health_cond = StringProperty()

    add_data_view = ObjectProperty()

    feature_input = ObjectProperty()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print('kkkkkkk k down', keycode[1])
        if keycode[1] == "backspace":
            if len(self.ids.input_field_id.text) > 0:
                if self.check_hebrew(self.ids.input_field_id.text):
                    self.ids.input_field_id.text = self.ids.input_field_id.text[1:]
                    self.ids.input_field_id.cursor = (0, 0)
                else:
                    return self.basic_keyboard_on_key_down(window, keycode, text, modifiers)
        elif keycode[1] == 'enter':
            self.add_data_view.get_input_feature_value(self.chosen_feature, self.ids.input_field_id.text)
            self.ids.input_field_id.focus = False
    def text_insert_field_hebrew(self, inserted_text, from_undo=False):
        print('commets field heb called')
        if len(self.ids.input_field_id.text) > 0:
            if inserted_text == ' ':
                if self.check_hebrew(self.ids.input_field_id.text):
                    self.ids.input_field_id.text = inserted_text + self.ids.input_field_id.text
                    self.ids.input_field_id.cursor = (0, 0)
                    return
            if self.check_hebrew(inserted_text):
                self.ids.input_field_id.base_direction = 'rtl'
                self.ids.input_field_id.text = inserted_text + self.ids.input_field_id.text
                self.ids.input_field_id.cursor = (0, 0)

            else:
                #self.ids.comments_id.text = self.ids.comments_id.text + inserted_text
                self.basic_insert_text_func(inserted_text, from_undo=False)
        else:
            self.ids.input_field_id.text = self.ids.input_field_id.text + inserted_text

    def check_hebrew(self, term):
        for i in set(term):
            if 'HEBREW' in unicodedata.name(i):
                return True
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.basic_insert_text_func = None
        self.basic_keyboard_on_key_down = None
        print("HS SEG ", self.ids.health_segment.ids.segment_switch.ids)
        Clock.schedule_once(self.set_segments)
        Clock.schedule_once(self.set_heb_text_field)
        #self.ids.input_field_id.bind(on_insert_text=self.on_insert)

    def set_heb_text_field(self, dt):
        self.basic_insert_text_func = self.ids.input_field_id.insert_text
        self.ids.input_field_id.insert_text = self.text_insert_field_hebrew

        self.basic_keyboard_on_key_down = self.ids.input_field_id.keyboard_on_key_down
        self.ids.input_field_id.keyboard_on_key_down = self.keyboard_on_key_down


    def set_segments(self, dt):
        self.ids.health_segment.custom_panel_width = 250
        self.ids.health_segment.ids.segment_switch.width = self.ids.health_segment.custom_panel_width / 7.6

        self.ids.location_segment.custom_panel_width = 250
        self.ids.location_segment.ids.segment_switch.width = self.ids.location_segment.custom_panel_width/7.6

        self.ids.crown_cone_segment.custom_panel_width = 100
        self.ids.crown_cone_segment.ids.segment_switch.width = self.ids.crown_cone_segment.custom_panel_width/2.5

    def fill_card_with_record(self, record: dict):
        self.add_data_view.controller.update_record(record)

    def refocus(self, *args):
        self.feature_input.focus = True




    def choose_feature(self, instance):
        self.ids.input_field_id.addDataCard = self
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.disabled = False
        feature_value = self.add_data_view.controller.new_record_dict.get(instance.text)
        if feature_value:
            self.ids.input_field_id.text = feature_value
        else:
            self.ids.input_field_id.text = ''

        self.ids.input_field_id.helper_text = ''

        self.ids.input_field_id.hint_text = instance.text
        if instance.text == 'Tree diameter':
            m_units = 'cm'
            self.ids.input_field_id.helper_text = f"Measurement units: [{m_units}]"
        elif instance.text == 'Crown diameter' or instance.text == 'Tree height':
            m_units = 'm'
            self.ids.input_field_id.helper_text = f"Measurement units: [{m_units}]"
        else:
            self.ids.input_field_id.helper_text = ''

        self.chosen_feature = instance.text
        self.chosen_feature_instance = instance

        self.feature_input.focus = True



