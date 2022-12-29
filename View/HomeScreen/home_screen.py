from View.base_screen import BaseScreenView
from kivy.storage.jsonstore import JsonStore
import secrets
from kivy.properties import StringProperty
from kivy import Logger
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
from kivymd.uix.pickers import MDDatePicker
import weakref


class DialogContent(MDBoxLayout):
    date = StringProperty('Pick date')

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_date, on_cancel=self.cancel_date)
        date_dialog.open()

    def save_date(self, instance, value, date_range):
        print(instance, value, date_range)
        self.date = str(value)

    def cancel_date(self, instance, value):
        self.date = '1011-11-11'

class HomeScreenView(BaseScreenView):

    # session_json_path = StringProperty()
    new_session_name = StringProperty()
    new_session_date = StringProperty()

    #img_path = StringProperty('TREEZ-LOGO-RGB.png')

    def __init__(self, **kwargs):
        super(HomeScreenView, self).__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def start_new_session_dialog(self):

        def close_dialog(event):
            self.dialog.dismiss()

        def confirm_dialog(event):

            if self.ids.new_ses_dialog.ids.date_picker.text == 'Pick date':
                self.ids.new_ses_dialog.date = '1011-11-11'

            if not self.ids.new_ses_dialog.ids.session_name.text:
                self.ids.new_ses_dialog.ids.session_name.required = True
                self.ids.new_ses_dialog.ids.session_name.focus = True
            else:
                self.new_session_name = self.ids.new_ses_dialog.ids.session_name.text
                self.new_session_date = self.ids.new_ses_dialog.ids.date_picker.text

                Logger.info(f"{__name__}: new session name: {self.new_session_name}, date: {self.new_session_date}")
                self.controller.start_new_session(self.new_session_name, self.new_session_date)

                self.app.go_next_screen('home screen', 'session screen')
                self.dialog.dismiss()

        close_btn = MDFlatButton(text="Cancel", on_release=close_dialog)
        confirm_btn = MDFlatButton(text="Confirm", on_release=confirm_dialog)

        self.dialog = MDDialog(title='Create new session',
                               size_hint=(.7, .5),
                               type="custom",
                               content_cls=DialogContent(),
                               buttons=(close_btn, confirm_btn)
                               )
        self.ids['new_ses_dialog'] = weakref.ref(self.dialog.content_cls)
        self.dialog.open()


    def start_recorded_sessions(self):
        self.model.start_list_sessions("completed")
        self.app.go_next_screen('home screen', 'list sessions screen')

    def start_incomplete_sessions(self):
        self.model.start_list_sessions("incomplete")
        self.app.go_next_screen('home screen', 'list sessions screen')

