from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty
from kivy import Logger
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)


class MySegmentedControl(MDSegmentedControl):
    custom_panel_width = StringProperty('100dp')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.segment_panel.width = self.custom_panel_width

    def on_custom_panel_width(self, *args):
        Logger.info(f"{__name__}: panel width changed")
        self.ids.segment_panel.width = self.custom_panel_width


class FeatureButton(MDFillRoundFlatButton):
    pass


class addDataCard(MDCard):
    chosen_feature = StringProperty()
    shadow_animation = ObjectProperty()

    health_cond = StringProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited, data card ids: {self.ids}")
        #self.ids.health_condition_layout.add_widget(MySegmentedControl())
        self.ids.health_segment.custom_panel_width = "150dp"
        self.ids.location_segment.custom_panel_width = "150dp"
        self.ids.crown_cone_segment.custom_panel_width = "150dp"


    def choose_feature(self, instance):
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.text = ''
        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text
        # self.ids.input_field_id.focus = True








        # print(f"btn inited, obj prop: {self.parent.root}")

