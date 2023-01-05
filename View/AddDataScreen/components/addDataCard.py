from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty, NumericProperty,ListProperty
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
from kivy.metrics import dp
from kivymd.uix.recycleview import MDRecycleView

#
# class SuggestButton(MDFillRoundFlatButton):
#     id = NumericProperty()
#     tree_page = ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def callback(self, item):
#         Logger.info(f"{__name__}: suggestion pressed: {item.text}")
#
#
# class SuggestButtonsView(MDRecycleView):
#     suggestion_list = ListProperty()
#     session_screen_view = ObjectProperty()
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def update_suggestions(self):
#         Logger.info(f"{__name__}: items updated")
#         self.data = [
#             {'text': str(suggestion)}
#             for i, suggestion in enumerate(self.suggestion_list)]



# <SuggestButton>:
#     size_hint: .33, .8
#     on_press: root.callback(self)
#     #_txt_left_pad: "12dp"
#     #bcolor: utils.get_color_from_hex('#B1122f')
#
# <SuggestButtonsView>:
#     viewclass: "SuggestButton"
#     RecycleBoxLayout:
#         bcolor: utils.get_color_from_hex('#B1122f')
#         id: recycle_suggestions
#         orientation: "horizontal"
#         padding: "5dp"
#         spacing: "5dp"
#         #default_size: None, "26dp"
#         default_size_hint: 1, None
#         size_hint_y: 0.1
#         #height: f"{self.minimum_height}dp"
#         #height: f"{root.height}dp"

class MySegmentedControl(MDSegmentedControl):
    custom_panel_width = StringProperty('100dp')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.segment_panel.width = self.custom_panel_width

    def on_custom_panel_width(self, *args):
        Logger.info(f"{__name__}: panel width changed, ids: {self.ids}")
        self.ids.segment_panel.width = self.custom_panel_width
        self._segment_switch_x = f"{float(self.custom_panel_width[:-2]) - 6}dp"

class FeatureButton(MDFillRoundFlatButton):
    pass



class addDataCard(MDCard):
    chosen_feature = StringProperty()
    chosen_feature_instance = ObjectProperty()
    shadow_animation = ObjectProperty()

    health_cond = StringProperty()

    suggestions = ListProperty(["apple", "banana", "orange", "grape", "mango"])


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited, data card ids: {self.ids}")
        #self.ids.health_condition_layout.add_widget(MySegmentedControl())
        self.ids.health_segment.custom_panel_width = "170dp"
        self.ids.location_segment.custom_panel_width = "150dp"
        self.ids.crown_cone_segment.custom_panel_width = "130dp"


    def choose_feature(self, instance):
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.text = ''
        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text
        self.chosen_feature_instance = instance

        # self.ids.input_field_id.focus = True








        # print(f"btn inited, obj prop: {self.parent.root}")

