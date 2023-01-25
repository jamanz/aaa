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

from kivy import app
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.recycleview import MDRecycleView
from kivy.app import App


class MySegmentedControl(MDSegmentedControl):
    custom_panel_width = StringProperty('100dp')
    control_type = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_custom_panel_width(self, *args):
        Logger.info(f"{__name__}: panel width changed, ids: {self.ids}")
        self.ids.segment_panel.width = self.custom_panel_width
        self._segment_switch_x = f"{float(self.custom_panel_width[:-2]) - 6}dp"

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


class addDataCard(MDCard, RoundedRectangularElevationBehavior): #RectangularElevationBehavior
    chosen_feature = StringProperty()
    chosen_feature_instance = ObjectProperty()
    shadow_animation = ObjectProperty()
    health_cond = StringProperty()

    add_data_view = ObjectProperty()

    feature_input = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.health_segment.custom_panel_width = "120dp"
        self.ids.location_segment.custom_panel_width = "110dp"
        self.ids.crown_cone_segment.custom_panel_width = "60dp"

    def refocus(self, *args):
        self.feature_input.focus = True

    def choose_feature(self, instance):
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.text = ''
        Logger.info(f"{__name__}: field focus: {self.ids.input_field_id.focus}")

        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text
        self.chosen_feature_instance = instance
        # Clock.schedule_once(self.refocus)
        self.feature_input.focus = True










        # print(f"btn inited, obj prop: {self.parent.root}")

