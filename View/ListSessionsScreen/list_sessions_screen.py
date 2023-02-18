from kivy.logger import Logger

from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.clock import Clock
from functools import partial
from kivymd.uix.recycleview import MDRecycleView
import os
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from Utility.pdf_generator import generate_pdf
from kivy.weakproxy import WeakProxy
from View.PhotoScreen.components.toast import Toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform

class PdfDialogContent(MDBoxLayout):
    chosen_session = StringProperty()
    list_screen_view = ObjectProperty()


class SessionItem(OneLineAvatarIconListItem):
    session_name = StringProperty()
    session_sid = StringProperty()

    can_delete = BooleanProperty(False)
    page_id = NumericProperty()
    sessions_page = ObjectProperty()


    def callback(self, item):
        session_json_name = f"{self.session_name}_{self.session_sid}.json"
        list_sessions_view = self.parent.parent.parent.parent

        if list_sessions_view.current_sessions_list_type == 'incomplete':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.incomplete_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')

        elif list_sessions_view.current_sessions_list_type == 'completed':
            list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.completed_path, session_json_name))
            list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')


    def make_pdf_from_session(self, session):
        #print('make pdf from session ', session)
        self.sessions_page = self.parent.parent
        print(self.sessions_page)
        self.sessions_page.list_sessions_view.make_pdf_for_session(session.session_name, session.session_sid)

    def delete_session(self, session):
        self.sessions_page = self.parent.parent
        Logger.info(f"{__name__}: session: {session},  gonna be deleted")
        self.sessions_page.delete_session(session)


class SessionsPage(MDRecycleView):
    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()
    sessions_list = ListProperty()

    list_sessions_view = ObjectProperty()

    delete_session_index = NumericProperty()
    delete_session_name = StringProperty()
    delete_session_sid = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        close_delete_dialog_btn = MDFlatButton(text="Cancel", on_release=self.close_delete_session_dialog)
        confirm_delete_dialog_btn = MDFlatButton(text="Confirm", on_release=self.confirm_delete_session_dialog)
        self.delete_session_dialog = MDDialog(title="Delete",
                                      type="alert",
                                      buttons=(close_delete_dialog_btn, confirm_delete_dialog_btn)
                                      )

    def close_delete_session_dialog(self, event):
        self.delete_session_dialog.dismiss()

    def confirm_delete_session_dialog(self, event):
        self.sessions_list.pop(self.delete_session_index)
        self.list_sessions_view.delete_session(self.delete_session_sid)
        self.update_sessions('incomplete')
        self.delete_session_dialog.dismiss()

    def delete_session(self, session):
        self.delete_session_index = session.page_id
        self.delete_session_name = session.session_name
        self.delete_session_sid = session.session_sid
        ses_path = self.incomplete_path.joinpath(f'{session.session_name}_{session.session_sid}.json')
        ses_num_of_records = len(JsonStore(ses_path).get('data').get('records'))

        self.delete_session_dialog.title = "Delete Session"
        self.delete_session_dialog.text = f"You sure you want delete [b]{self.delete_session_name}[/b] with [b]{ses_num_of_records}[/b] records?"
        self.delete_session_dialog.open()

    def update_sessions(self, session_type):
        if session_type == 'completed':
            self.sessions_list = list(self.completed_path.glob("*.json"))
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1],

                 'can_delete': False,
                 'page_id': i}
                for i, session in enumerate(self.sessions_list)
            ]

        elif session_type == 'incomplete':
            self.sessions_list = list(self.incomplete_path.glob("*.json"))
            self.data = [
                {'session_name': session.stem.split('_')[0],
                 'session_sid': session.stem.split('_')[1],

                 'can_delete': True,
                 'page_id': i}
                for i, session in enumerate(self.sessions_list)
            ]



class ListSessionsScreenView(BaseScreenView):
    app_bar_title = StringProperty('Default Title')
    current_sessions_list_type = StringProperty()

    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()
    #photo_path = Path('photos').resolve()
    page_num = 0
    config_json_path = Path('./config/imortant_path.json').resolve()
    file_manager_open = False

    def update_pdf_progress(self, page_no):
        #print("ids: ", self.ids.pdf_dialog_content.ids)
        from kivymd.uix.progressbar import MDProgressBar
        val = 100*page_no/self.page_num
        print("pdf_progress val old: ", self.ids.pdf_progress_content.ids.progress_bar_id.value)
        self.ids.pdf_progress_content.ids.progress_bar_id.value = int(val)
        print("pdf_progress val new: ", self.ids.pdf_progress_content.ids.progress_bar_id.value)

    def open_file_manager(self, path):
        self.file_manager.show(os.path.expanduser(str(path)))  # output manager to the screen
        self.file_manager_open = True


    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        if platform == 'android':
            Toast.show(f'Got path:\n{path} ')
        else:
            toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.file_manager_open = False
        self.file_manager.close()

    def make_pdf_for_session(self, session_name: str, session_sid: str):
        self.photo_path = Path(JsonStore(self.config_json_path).get('camera').get('path'))
        #self.photo_path = self.photo_path.parent.parent
        print("in make pdf for ses from store path:", self.photo_path)
        self.open_file_manager(self.photo_path)

    def make_pdf_for_session1(self, session_name: str, session_sid: str):
        self.photo_path = Path(JsonStore(self.config_json_path).get('camera').get('path'))
        images_list = list(self.photo_path.joinpath(session_name).glob('*.jpg'))
        Logger.info(f"{__name__}: Image list {images_list}")
        self.page_num = len(images_list) // 4
        if len(images_list) % 4 != 0:
            self.page_num += 1

        self.pdf_dialog.open()
        print(f"{__name__}: photopath: {self.photo_path}")
        generate_pdf(image_dir=self.photo_path.joinpath(session_name),
                     dest_path=self.photo_path.joinpath(session_name),
                     filename=f'session_{session_name}',
                     progress_func=self.update_pdf_progress)
        Toast().show("Saved pdf:\n" + str(self.photo_path))

    def delete_session(self, session_sid: str):
        self.model.delete_session(session_sid)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

        confirm_pdf_btn = MDFlatButton(text="OK", on_release=self.close_pdf_dialog)
        self.pdf_content_cls = PdfDialogContent()
        self.pdf_content_cls.list_screen_view = self
        self.pdf_dialog = MDDialog(title=f'Making PDF',
                                      anchor_x="center",
                                      type="custom",
                                      content_cls=self.pdf_content_cls,
                                      buttons=([confirm_pdf_btn])
                                      )
        self.ids['pdf_progress_content'] = WeakProxy(self.pdf_content_cls)
        #weakref.ref(self.upload_dialog.content_cls)
        #self.ids['upload_dialog'] = weakref.ref(self.upload_dialog.content_cls)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def close_pdf_dialog(self, event):
        self.pdf_dialog.dismiss()

    def on_pre_enter(self, *args):
        self.ids.sessions_page.update_sessions(self.current_sessions_list_type)

    def start_incomplete_sessions(self):
        Logger.info(f"{__name__}: started incomplete sessions")
        self.current_sessions_list_type = 'incomplete'
        self.app_bar_title = "Incomplete sessions"
        self.ids.sessions_page.update_sessions('incomplete')
        self.ids.sessions_page.list_sessions_view = self

    def start_completed_sessions(self):
        Logger.info(f"{__name__}: started completed sessions")
        self.current_sessions_list_type = 'completed'
        self.app_bar_title = "Completed sessions"
        self.ids.sessions_page.update_sessions('completed')
        self.ids.sessions_page.list_sessions_view = self

    def send_path_to_session_screen(self, path):
        self.model.send_path_to_session_screen(path)