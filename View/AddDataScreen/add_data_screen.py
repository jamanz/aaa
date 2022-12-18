from View.base_screen import BaseScreenView
from View.AddDataScreen.components.addDataCard import addDataCard
# from main import logger
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class AddDataScreenView(BaseScreenView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("w: AddDataScreenView inited")
        ### add widgets
        self.add_widget(addDataCard())

        confirm_btn = Button(text="Confirm", size_hint=(.3, .1), on_press=self.save_record_and_back_to_session_screen)
        self.add_widget(confirm_btn)
        Logger.info(f"{__name__}: AddDataCard and buttons added")

    def save_record_and_back_to_session_screen(self, event):
        self.controller.write_record_to_json()
        self.app.manager_screens.current = "session screen"

    def get_input_feature_value(self, feature_key, feature_value):
        # print(instance.text)
        # print("parent: ", self.parent.save_feature_from_input_to_json(self.chosen_feature, instance.text))
        self.controller.get_input_feature_value(feature_key, feature_value)


    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
