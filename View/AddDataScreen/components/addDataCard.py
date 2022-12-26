from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ObjectProperty
from kivy import Logger


class addDataCard(MDCard):
    chosen_feature = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def callback(self, instance):
        Logger.info(f"{__name__}: pressed - {instance.text}")
        self.ids.input_field_id.hint_text = instance.text
        self.chosen_feature = instance.text





        # print(f"btn inited, obj prop: {self.parent.root}")

