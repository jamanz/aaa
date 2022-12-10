from View.base_screen import BaseScreenView
from View.AddDataScreen.components.addDataCard import addDataCard
# from main import logger
import logging
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

logger = logging.getLogger()

class AddDataScreenView(BaseScreenView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.model = model
        # self.controller = controller
        #
        logger.info("AddDataScreenView inited")
        # card =
        self.add_widget(addDataCard())
        confirm_btn = Button(text="Confirm", size_hint=(.3, .1), on_press=self.controller.write_record_to_json)
        self.add_widget(confirm_btn)
        # self.add_widget(BoxLayout().add_widget(Button(text="Preview")))


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
