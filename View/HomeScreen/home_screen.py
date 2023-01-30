from View.base_screen import BaseScreenView
from kivy.storage.jsonstore import JsonStore
import secrets
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy import Logger
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
from kivymd.uix.pickers import MDDatePicker
import weakref
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.weakproxy import WeakProxy
import os
from Utility.google_sheets import get_user_email

class GoogleSheetsDialogContent(MDBoxLayout):
    user_email = StringProperty()


class CustomWorkSheetButton(MDRectangleFlatIconButton):
    item_id = StringProperty()
    icon_name = StringProperty()


class WorksheetChoiceDialogContent(MDBoxLayout):
    chosen_worksheet = StringProperty()
    last_picked_id = StringProperty()
    screen_view = ObjectProperty()

    def pick_worksheet(self, instance):
        if self.last_picked_id:
            self.ids[self.last_picked_id].icon_color = 'white'
            self.ids[instance.id].icon_color = 'green'
            self.last_picked_id = instance.id
        else:
            self.last_picked_id = instance.id
            self.ids[instance.id].icon_color = 'green'

        self.screen_view.chosen_worksheet = instance.text


    def populate_with_available_ws_buttons(self, list_of_available_worksheets: list[str]):

        for i, ws in enumerate(list_of_available_worksheets):
            ws_button = CustomWorkSheetButton(
                    text=f'{ws}',
                    id=ws,
                    on_release=self.pick_worksheet
                )
            self.ids[ws_button.id] = WeakProxy(ws_button)
            self.ids.ws_buttons_layout.add_widget(
                ws_button
            )


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
    current_worksheet = ObjectProperty()
    chosen_worksheet = StringProperty()
    #img_path = StringProperty('TREEZ_LOGO_RGB.png')
    user_email = StringProperty()

    is_autg = BooleanProperty()

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
                               md_bg_color=self.app.theme_cls.accent_color,
                               content_cls=DialogContent(),
                               buttons=(close_btn, confirm_btn)
                               )
        self.ids['new_ses_dialog'] = weakref.ref(self.dialog.content_cls)
        self.dialog.open()

    def start_authorized_dialog(self):
        def confirm_dialog(event):
            self.auth_dialog.dismiss()

        confirm_btn = MDFlatButton(text="Confirm", on_release=confirm_dialog)

        # content_cls = WorksheetChoiceDialogContent()
        content_cls = GoogleSheetsDialogContent()
        content_cls.user_email = get_user_email()
        content_cls.screen_view = self
        # list_of_available_worksheets = self.model.get_list_of_available_worksheets_to_view()
        # content_cls.populate_with_available_ws_buttons(list_of_available_worksheets)

        self.auth_dialog = MDDialog(title='Google Sheets',
                                                size_hint=(.6, .5),
                                                md_bg_color=self.app.theme_cls.accent_color,
                                                type="custom",
                                                content_cls=content_cls,
                                                buttons=([confirm_btn])
                                                )
        # cc
        # self.ids['worksheet_choice_dialog'] = WeakProxy(self.worksheet_choice_dialog.content_cls)
        self.auth_dialog.open()

    def start_login(self):
        print('in kivy call login s')
        self.app.gl_login()
        print('in kivy call login e')
        if os.path.exists("./config/authorized_user.json"):
            self.start_authorized_dialog()
        else:
            self.model.auth_in_google()
            self.start_authorized_dialog()


    def set_worksheet_in_model(self, worksheet_title):
        self.model.set_chosen_worksheet(worksheet_title)

    def start_worksheet_choice_dialog(self):

        def close_dialog(event):
            self.worksheet_choice_dialog.dismiss()

        def confirm_dialog(event):
            # self.chosen_worksheet was set from the dialog class
            Logger.info(f"{__name__}: Chosen worksheet: {self.chosen_worksheet}")
            if self.chosen_worksheet == '':
                Logger.info(f"{__name__}: self.chosen_worksheet is empty")
            else:
                self.set_worksheet_in_model(self.chosen_worksheet)
                self.worksheet_choice_dialog.dismiss()

        close_btn = MDFlatButton(text="Cancel", on_release=close_dialog)
        confirm_btn = MDFlatButton(text="Confirm", on_release=confirm_dialog)

        # content_cls = WorksheetChoiceDialogContent()
        content_cls = GoogleSheetsDialogContent()
        content_cls.screen_view = self
        # list_of_available_worksheets = self.model.get_list_of_available_worksheets_to_view()
        # content_cls.populate_with_available_ws_buttons(list_of_available_worksheets)

        self.worksheet_choice_dialog = MDDialog(title='Login to Google Sheets',
                                               size_hint=(.6, .5),
                                               md_bg_color=self.app.theme_cls.accent_color,
                                               type="custom",
                                               content_cls=content_cls,
                                               buttons=(close_btn, confirm_btn)
                                                )
        # cc
        self.ids['worksheet_choice_dialog'] = WeakProxy(self.worksheet_choice_dialog.content_cls)
        self.worksheet_choice_dialog.open()


    def start_recorded_sessions(self):
        self.model.start_list_sessions("completed")
        self.app.go_next_screen('home screen', 'list sessions screen')

    def start_incomplete_sessions(self):
        self.model.start_list_sessions("incomplete")
        self.app.go_next_screen('home screen', 'list sessions screen')

