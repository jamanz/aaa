from kivy.logger import Logger
from kivy import app
from View.base_screen import BaseScreenView
from pathlib import Path
from kivymd.uix.list import OneLineListItem
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.behaviors import TouchBehavior
from kivy.clock import Clock
from functools import partial
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.recycleview import MDRecycleView
import os
from os.path import exists
import shutil
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
from kivy.clock import mainthread
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage, Chooser
    Environment = autoclass('android.os.Environment')
    ss = SharedStorage()


def rtl(heb_str):
    return heb_str[::-1]

class PdfDialogContent(MDBoxLayout):
    chosen_session = StringProperty()
    list_screen_view = ObjectProperty()

    @mainthread
    def update_pdf_progress(self, page_no):
        # print("ids: ", self.ids.pdf_dialog_content.ids)
        try:
            val = 100 * page_no / self.page_num
            self.ids.progress_bar_id.value = int(val)
        except ZeroDivisionError:
            pass
        #Logger.info(f"{__name__}: pdf progres val updated in mainthread: ", self.ids.progress_bar_id.value)

    def set_pdf_data(self, image_list, page_num, session_name):
        self.image_list = image_list
        self.page_num = page_num
        self.session_name = session_name


    def on_pdf_dialog_open(self, *args):
        dest_path = generate_pdf(image_dir=self.list_screen_view.photo_path,
                                 dest_path=self.list_screen_view.photo_path,
                                 filename=f'session_{self.session_name}',
                                 progress_func=self.update_pdf_progress)
        Toast().show("Saved pdf:\n" + str(dest_path))
        while not dest_path:
            continue
        else:
            if platform == 'android':
                # Request permissions to read external storage
                request_permissions([Permission.READ_EXTERNAL_STORAGE])
                # Get the Java classes for Intent and Uri
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')

                # Set the path to the PDF file you want to open
                path = str(dest_path)
                share_path = ss.copy_to_shared(path)
                print('Sharepath: ', share_path)
                # Create an Intent to open the PDF file
                intent = Intent(Intent.ACTION_VIEW)
                # intent.setDataAndType(Uri.parse(share_path), "application/pdf")
                intent.setDataAndType(share_path, "application/pdf")
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)

                # Start the Activity to open the PDF file
                current_activity = cast('android.app.Activity', autoclass('org.kivy.android.PythonActivity').mActivity)
                current_activity.startActivity(intent)

                self.list_screen_view.clean_cache_after_generation()

            self.update_pdf_progress(1)
            self.list_screen_view.pdf_dialog.dismiss()
            Logger.info("pdf intent ended")


class SessionItemIconContainer(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class SessionItem(OneLineAvatarIconListItem, TouchBehavior):
    session_name = StringProperty()
    session_sid = StringProperty()

    can_delete = BooleanProperty(False)
    page_id = NumericProperty()
    sessions_page = ObjectProperty()
    duration_long_touch = NumericProperty(0.6)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_long_touch(self, *args):
        self.sessions_page = self.parent.parent

        if self.sessions_page.session_type == 'incomplete':
            self.sessions_page.incomplete_snackbar.open()
        elif self.sessions_page.session_type == 'completed':
            self.sessions_page.completed_snackbar.open()





        self.sessions_page.long_touch = True
        print("on long touch args: ", *args)

    def set_chosen_session_for_snackbar(self, session):
        self.sessions_page = self.parent.parent

    def callback(self, item):
        self.sessions_page = self.parent.parent
        if not self.sessions_page.long_touch:
            session_json_name = f"{self.session_name}_{self.session_sid}.json"
            list_sessions_view = self.parent.parent.parent.parent

            if list_sessions_view.current_sessions_list_type == 'incomplete':
                list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.incomplete_path, session_json_name))
                list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')

            elif list_sessions_view.current_sessions_list_type == 'completed':
                list_sessions_view.send_path_to_session_screen(Path(list_sessions_view.completed_path, session_json_name))
                list_sessions_view.app.go_next_screen('list sessions screen', 'session screen')
        else:
            self.sessions_page.chosen_session_item = item

    ## function for old IconRight widget interface
    def make_pdf_from_session(self, session):
        # print('make pdf from session ', session)
        self.sessions_page = self.parent.parent
        print(self.sessions_page)
        self.sessions_page.list_sessions_view.make_pdf_for_session(session.session_name, session.session_sid)

    ## function for old IconRight widget interface
    def delete_session(self, session):
        self.sessions_page = self.parent.parent
        Logger.info(f"{__name__}: session: {session},  gonna be deleted")
        self.sessions_page.delete_session(session)


class CustomSnackbar(Snackbar):
    snackbar_x = dp(10)
    snackbar_y = dp(10)
    duration = 2
    size_hint_x = (Window.width - (dp(10) * 2)) / Window.width

class SessionsPage(MDRecycleView):
    incomplete_path = Path("assets", "data").resolve()
    completed_path = Path("assets", "data", "completed").resolve()
    sessions_list = ListProperty()

    list_sessions_view = ObjectProperty()

    delete_session_index = NumericProperty()
    delete_session_name = StringProperty()
    delete_session_sid = StringProperty()

    long_touch = False
    chosen_session_item = ObjectProperty()
    session_type = StringProperty('incomplete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        close_delete_dialog_btn = MDFlatButton(text=f"[font=Arimo]{rtl('ביטול')}[/font]", on_release=self.close_delete_session_dialog)
        confirm_delete_dialog_btn = MDFlatButton(text=f"[font=Arimo]{rtl('אישור')}[/font]", on_release=self.confirm_delete_session_dialog)
        self.delete_session_dialog = MDDialog(title=f"[font=Arimo]{rtl('למחוק')}[/font]",
                                              type="alert",
                                              buttons=(close_delete_dialog_btn, confirm_delete_dialog_btn)
                                              )
        self.incomplete_snackbar = CustomSnackbar(buttons=[MDFlatButton(
                                                            text=rtl("מחק הפעלה"),
                                                            font_name='Arimo',
                                                            # text_color=(1, 1, 1, 1),
                                                            on_release=self.delete_session)])

        self.completed_snackbar = CustomSnackbar(buttons=[
                                                    MDFlatButton(
                                                        text="PDF " + rtl("צור"),
                                                        font_name='Arimo',
                                                        # text_color=(1, 1, 1, 1),
                                                        on_release=self.make_pdf_from_session,
                                                    ),

                                                    MDFlatButton(
                                                        text=rtl("מחק הפעלה"),
                                                        font_name='Arimo',
                                                        # text_color=(1, 1, 1, 1),
                                                        on_release=self.delete_session,
                                                    )])

        self.incomplete_snackbar.bind(on_dismiss=self.on_snack_dismiss)
        self.completed_snackbar.bind(on_dismiss=self.on_snack_dismiss)



    # def delete_session(self, session_item):
    #     Logger.info(f"{__name__}: session: {session_item},  gonna be deleted")
    #     self.sessions_page.delete_session(session_item)
    #



    def make_pdf_from_session(self, *args):
        self.list_sessions_view.make_pdf_for_session(self.chosen_session_item.session_name, self.chosen_session_item.session_sid)

    def on_snack_dismiss(self, *args):
        self.long_touch = False

    def close_delete_session_dialog(self, event):
        self.delete_session_dialog.dismiss()

    def confirm_delete_session_dialog(self, event):
        self.sessions_list.pop(self.delete_session_index)
        self.list_sessions_view.delete_session(self.session_type, self.delete_session_sid)
        self.update_sessions(self.session_type)
        self.delete_session_dialog.dismiss()

    # updated func, adeed path handler for json session
    def delete_session(self, *args):
        session = self.chosen_session_item
        self.delete_session_index = session.page_id
        self.delete_session_name = session.session_name
        self.delete_session_sid = session.session_sid

        print('SES INFO,', self.session_type, self.delete_session_name, self.delete_session_sid)
        if self.session_type == 'incomplete':
            ses_path = self.incomplete_path.joinpath(f'{session.session_name}_{session.session_sid}.json')
        elif self.session_type == 'completed':
            ses_path = self.completed_path.joinpath(f'{session.session_name}_{session.session_sid}.json')
        else:
            raise ValueError('Session type must be incomplete or completed ')

        ses_num_of_records = len(JsonStore(ses_path).get('data').get('records'))

        #    ses_num_of_records = len(JsonStore(ses_path).get('data').get('records'))

        self.delete_session_dialog.title = f"[font=Arimo]{rtl('מחק הפעלה')}[/font]"
        #self.delete_session_dialog.text = f"You sure you want delete [b]{self.delete_session_name}[/b] with [b]{ses_num_of_records}[/b] records?"
        self.delete_session_dialog.text = f"[font=Arimo]{rtl('רשומות?')}[/font] " + f"[b]{ses_num_of_records}[/b]" + f"[font=Arimo] {rtl('עם')} [b]{self.delete_session_name} [/b][/font]" + f"[font=Arimo]{rtl('אתה בטוח שאתה רוצה למחוק')}[/font]"
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
    # photo_path = Path('photos').resolve()
    page_num = 0
    config_json_path = Path('./config/imortant_path.json').resolve()
    file_manager_open = False

    def set_topappbar_font(self, dt):
        self.ids.topappbar.ids.label_title.font_name = 'Arimo'

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


    # def make_pdf_for_session1(self, session_name: str, session_sid: str):
    #     self.photo_path = Path(JsonStore(self.config_json_path).get('camera').get('path'))
    #     # self.photo_path = self.photo_path.parent.parent
    #     print("in make pdf for ses from store path:", self.photo_path)
    #     self.open_file_manager(self.photo_path)


    def clean_cache_after_generation(self):
        temp = ss.get_cache_dir()
        if temp and exists(temp):
            shutil.rmtree(temp)
        Logger.info(f"{__name__}: Cache cleared")


    def get_path_from_media_store(self, ses_name):
        if platform == 'android':
            # Request permissions to read external storage
            request_permissions([Permission.READ_EXTERNAL_STORAGE])

            # Get the Java class for MediaStore and its sub-classes
            Environment = autoclass('android.os.Environment')
            MediaStore = autoclass('android.provider.MediaStore')
            Images = autoclass('android.provider.MediaStore$Images')
            MediaStoreImagesMedia = autoclass('android.provider.MediaStore$Images$Media')

            # Set the image directory you want to scan
            path = Environment.getExternalStoragePublicDirectory(
            Environment.DIRECTORY_DCIM).getPath() + "/Treez" + f"/{ses_name}"

            # Get the content resolver
            content_resolver = cast('android.content.ContextWrapper',
                                autoclass('org.kivy.android.PythonActivity').mActivity).getContentResolver()

            # Define the columns to retrieve
            projection = [MediaStoreImagesMedia._ID, MediaStoreImagesMedia.DATA]

            # Query the MediaStore for images in the specified directory
            cursor = content_resolver.query(
                                MediaStoreImagesMedia.EXTERNAL_CONTENT_URI,
                                projection,
                                MediaStoreImagesMedia.DATA + " like ? ",
                                ["%" + path + "%"],
                                MediaStoreImagesMedia.DEFAULT_SORT_ORDER
            )
            pth_list = []
            # Print the image paths
            if cursor is not None and cursor.moveToFirst():
                while not cursor.isAfterLast():
                    image_path = cursor.getString(cursor.getColumnIndexOrThrow(MediaStoreImagesMedia.DATA))
                    pth_list.append(image_path)
                    print(image_path)
                    cursor.moveToNext()

                cursor.close()
            return pth_list

    def make_pdf_for_session(self, session_name: str, session_sid: str):
        # self.photo_path = Path(JsonStore(self.config_json_path).get('camera').get('path'))
        if platform == 'android':

            self.photo_path = Path(Environment.DIRECTORY_DCIM).joinpath(f"Treez")
             #images_list = list(self.photo_path.joinpath(session_name).glob('*.jpg'))
            images_list = self.get_path_from_media_store(session_name)
            Logger.info(f"{__name__}: Image list from mediastore {images_list}")
            Logger.info(f"{__name__}: cache dir: {ss.get_cache_dir()}")

            private_paths = []
            for image in images_list:
                image_file_name = str(Path(image).name)
                image_path = self.photo_path.joinpath(f"{session_name}/{image_file_name}")
                Logger.info(f"{__name__}: current image path is: {image_path}")
                private_paths.append(ss.copy_from_shared(str(image_path)))

            try:
                Logger.info(f"{__name__}: cache dir after: {ss.get_cache_dir()}, pp: {private_paths} "
                            f"os.dir DCIM: {os.listdir('./DCIM')}"
                            f"os.dir .: {os.listdir('.')}")
            except:
                Logger.info(f"{__name__}: cache dir after: {ss.get_cache_dir()}, , pp: {private_paths}, os.dir gen: {os.listdir('.')}")

            self.photo_path = ss.get_cache_dir()
            images_list = private_paths
        else:
            images_list = []
            session_photo_dir = Path(f'./{session_name}/')
            self.photo_path = session_photo_dir

            for image in session_photo_dir.glob('*jpg'):
                Logger.info(f"{__name__}: image {image}")
                images_list.append(image)

        self.page_num = len(images_list) // 4
        if len(images_list) % 4 != 0:
            self.page_num += 1
        self.ids.pdf_progress_content.set_pdf_data(images_list, self.page_num, session_name)

        self.pdf_dialog.open()
        print(f"{__name__}: pdf dialog open photopath: {self.photo_path}")


    def delete_session(self, session_type: str, session_sid: str):
        self.model.delete_session(session_type, session_sid)

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
        self.pdf_dialog.on_open = self.pdf_content_cls.on_pdf_dialog_open
        self.ids['pdf_progress_content'] = WeakProxy(self.pdf_content_cls)
        # weakref.ref(self.upload_dialog.content_cls)
        # self.ids['upload_dialog'] = weakref.ref(self.upload_dialog.content_cls)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        Clock.schedule_once(self.set_topappbar_font)

    def close_pdf_dialog(self, event):
        self.pdf_dialog.dismiss()

    def on_pre_enter(self, *args):
        self.ids.sessions_page.update_sessions(self.current_sessions_list_type)

    def start_incomplete_sessions(self):
        Logger.info(f"{__name__}: started incomplete sessions")
        self.current_sessions_list_type = 'incomplete'
        self.app_bar_title = "Incomplete sessions"
        self.ids.sessions_page.update_sessions('incomplete')
        self.ids.sessions_page.session_type = 'incomplete'
        self.ids.sessions_page.list_sessions_view = self

    def start_completed_sessions(self):
        Logger.info(f"{__name__}: started completed sessions")
        self.current_sessions_list_type = 'completed'
        self.app_bar_title = "Completed sessions"
        self.ids.sessions_page.update_sessions('completed')
        self.ids.sessions_page.session_type = 'completed'
        self.ids.sessions_page.list_sessions_view = self

    def send_path_to_session_screen(self, path):
        self.model.send_path_to_session_screen(path)