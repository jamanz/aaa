from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty
from kivy import Logger
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)


class FeatureButton(MDFillRoundFlatButton):
    pass

class addDataCard(MDCard):
    chosen_feature = StringProperty()
    shadow_animation = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def choose_feature(self, instance):
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.text = ''
        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text
        # self.ids.input_field_id.focus = True






        # print(f"btn inited, obj prop: {self.parent.root}")

