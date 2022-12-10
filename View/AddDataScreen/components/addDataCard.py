# todo: implement logging to understand order of widget initialization
# TODO:



from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.app import App
# from main import logger

from pprint import pprint


## todo: add block for input label when button is not pressed
class addDataCard(MDCard):
    chosen_feature = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("addDataCard initialization")
        # logger.info("addDataCard inited")

    def callback(self, instance):
        print("MyCard pressed ", instance)
        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text





        # print(f"btn inited, obj prop: {self.parent.root}")

