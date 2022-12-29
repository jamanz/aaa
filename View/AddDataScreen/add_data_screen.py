from View.base_screen import BaseScreenView
from View.AddDataScreen.components.addDataCard import addDataCard
# from main import logger
from kivy.logger import Logger
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import weakref

class PreviewContent(MDBoxLayout):
    tree_number = StringProperty()
    tree_specie = StringProperty()
    stem_number = StringProperty()

    def update_values(self, record):
        self.tree_number = str(record.get('Tree Number'))
        self.tree_specie = str(record.get('Tree Specie'))
        self.stem_number = str(record.get('Stem Number'))


class AddDataScreenView(BaseScreenView):
    app_bar_title = StringProperty('New Tree')

    def show_preview(self):

        def close_dialog(event):
            self.dialog.dismiss()

        def ok_dialog(event):
            self.dialog.dismiss()

        close_btn = MDFlatButton(text="Back", on_release=close_dialog)
        ok_btn = MDFlatButton(text="Ok", on_release=ok_dialog)

        self.dialog = MDDialog(title='Preview',
                               size_hint=(.7, .5),
                               type="custom",
                               content_cls=PreviewContent(),
                               buttons=(close_btn, ok_btn)
                               )
        self.ids['preview_dialog'] = weakref.ref(self.dialog.content_cls)
        self.ids.preview_dialog.update_values(self.controller.get_record())
        self.dialog.open()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

        self.add_widget(addDataCard())

        Logger.info(f"{__name__}: AddDataCard and buttons added")

    def cancel_record(self):
        self.controller.clear_record()
        self.app.go_prev_screen()

    def save_record_and_back_to_session_screen(self):
        self.controller.write_record_to_json()
        self.app.go_prev_screen()

    def get_input_feature_value(self, feature_key, feature_value):
        #print(feature_value, self.ids.box_layout.ids)

        # print("parent: ", self.parent.save_feature_from_input_to_json(self.chosen_feature, instance.text))
        self.controller.get_input_feature_value(feature_key, feature_value)
