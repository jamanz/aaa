import pathlib

from View.base_screen import BaseScreenView
from kivy.logger import Logger

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from camera4kivy import Preview
from View.PhotoScreen.components.toast import Toast
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial

import os, shutil
from kivy.storage.jsonstore import JsonStore
from kivy import user_home_dir, kivy_home_dir, kivy_base_dir, dirname, kivy_data_dir
from kivy.clock import Clock
from kivy.graphics import Rectangle

from kivy.uix.image import AsyncImage, Image


if platform == 'android':
    from jnius import autoclass, cast
    from android.storage import primary_external_storage_path
    from android import mActivity
    from android.permissions import request_permissions, Permission, check_permission
    from kvdroid.tools.path import sdcard

class PhotoScreenView(BaseScreenView):
    session_name = StringProperty()
    tree_name = ObjectProperty()
    photo_count = 0
    photoReview = BooleanProperty(False)
    photo_ready = BooleanProperty(False)

    saved_filename = StringProperty()
    config_json = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")
        self.config_json_path = pathlib.Path('./config/imortant_path.json').resolve()
        self.file_basic_path = ''

    def set_tree_name(self, tree_name):
        self.tree_name = tree_name

    def on_pre_enter(self, *args):
        self.ids.preview.connect_camera(filepath_callback=self.capture_path)

    def on_enter(self):
        self.session_name = self.model.session_name
        self.tree_name = self.model.tree_name

        if platform == 'android':

            # Request permissions to read external storage
            request_permissions([Permission.READ_EXTERNAL_STORAGE,
                                 Permission.WRITE_EXTERNAL_STORAGE])

            Logger.info(f"{__name__}: Check for EXTERNAL STORAGE PERMISSONS: "
                        f"WRITE: {check_permission(Permission.READ_EXTERNAL_STORAGE)}, "
                        f"READ: {check_permission(Permission.READ_EXTERNAL_STORAGE)}"
                        )
            # todo: change photo count assign
            self.photo_count = len(list(pathlib.Path(primary_external_storage_path()).joinpath(
                                    f'DCIM/Treez/{self.session_name}/').glob(f'{self.tree_name}*jpg')))
        else:
            self.photo_count = len(
                list(pathlib.Path(self.app.app_folder).joinpath(self.session_name).glob(f'{self.tree_name}*jpg')))

        Logger.info(f"{__name__}: number of existed photos of tree: {self.tree_name} is {self.photo_count} ")

    def on_pre_leave(self):
        self.ids.preview.disconnect_camera()
    # For Async Image
    # def on_image_load(self):
    #     Logger.info(f"{__name__}: on_image_load loaded")

    def capture_path(self, file_path):
        self.file_basic_path = pathlib.Path(file_path).resolve()
        file_name = self.file_basic_path.stem
        suf = self.file_basic_path.suffix
        session_name = self.file_basic_path.parent.name

        Logger.info(
            f"{__name__}: Photo maked, file callback, "
            f"basic path-> {self.file_basic_path}, "
            f"session name: {session_name},"
            f" filename: {file_name}")

        self.saved_filename = self.file_basic_path.name

        # file path shaping for shared storage !Does not work on Android > 10
        # if platform == 'android':
        #     self.file_basic_path = pathlib.Path(sdcard()).joinpath(f'DCIM/Treez/{session_name}/{file_name}{suf}')
        # else:
        #     self.file_basic_path = pathlib.Path(self.app.app_folder).joinpath(session_name, self.saved_filename)

        self.file_basic_path = pathlib.Path(file_path).resolve()

        self.photo_ready = True
        Logger.info(
            f"{__name__}: capture path ended with default fp: {self.file_basic_path}, saved fn: {self.saved_filename}")

        # Write default image path for use in list_session_screen
        self.config_json = JsonStore(str(self.config_json_path))
        self.config_json.put("camera", path=str(self.file_basic_path.parent.parent))

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.ids.photo_layout.orientation = 'vertical'
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (1, .15)
            self.ids.pad_end.size_hint = (1, .1)
        else:
            self.ids.photo_layout.orientation = 'horizontal'
            self.ids.preview.size_hint = (.8, 1)
            self.ids.buttons.size_hint = (.15, 1)
            self.ids.pad_end.size_hint = (.1, 1)

        # buttons resize and repos on change
        if platform in ['android', 'ios']:
            self.ids.buttons.ids.photo_and_save.min_state_time = 0.2
        else:
            self.ids.buttons.ids.photo_and_save.min_state_time = 1
        if Window.width < Window.height:
            self.ids.buttons.ids.photo_and_save.pos_hint = {'center_x': .25, 'center_y': .5}
            self.ids.buttons.ids.photo_and_save.size_hint = (.2, None)
            self.ids.buttons.ids.flash_and_cancel.pos_hint = {'center_x': .75, 'center_y': .5}
            self.ids.buttons.ids.flash_and_cancel.size_hint = (.2, None)
        else:
            self.ids.buttons.ids.photo_and_save.pos_hint = {'center_x': .5, 'center_y': .75}
            self.ids.buttons.ids.photo_and_save.size_hint = (None, .2)
            self.ids.buttons.ids.flash_and_cancel.pos_hint = {'center_x': .5, 'center_y': .25}
            self.ids.buttons.ids.flash_and_cancel.size_hint = (None, .2)


class Background(Label):
    pass


class ButtonsLayout2(RelativeLayout):
    filename = StringProperty()
    photo_screen_view = ObjectProperty()

    def __init__(self, **args):
        super().__init__(**args)


class ImgPrev(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_img_source(self, source):
        self.source = source


class ButtonsLayout1(RelativeLayout):
    file_path = StringProperty()
    photo_screen_view = ObjectProperty()

    def __init__(self, **args):
        super().__init__(**args)

    def photo(self):
        # first function that called when photo button is clicked
        self.photo_screen_view = self.parent.parent
        tree_name = self.photo_screen_view.tree_name
        session_name = self.photo_screen_view.session_name
        photo_count = self.photo_screen_view.photo_count

        #Logger.info(f"{__name__:} -> {self.parent.parent.ids}")
        Logger.info(f"{__name__}: self.photo assigned from file basic path, filepath {self.file_path}")
        if photo_count == 0:
            name = f"{tree_name}"
        else:
            name = f"{tree_name}_{photo_count}"

        # location "private" is app_path/... "shared" is storage/emulated/0/DCIM/appname/
        self.photo_screen_view.ids.preview.capture_photo(location='private', subdir=session_name, name=name)

        # wait for capture_photo callback
        while not self.photo_screen_view.photo_ready:
            continue
        #Clock.schedule_once(self.show_photo_image, 0.1)
        self.show_photo_image(0.1)
        self.photo_screen_view.photo_ready = False

    def show_photo_image(self, dt):
        self.file_path = str(self.photo_screen_view.file_basic_path)
        Logger.info(f"{__name__}: show photo image called: file path: {self.file_path}")

        self.image_preview = ImgPrev()
        self.image_preview.set_img_source(self.file_path) # self.get_path_from_media_store('kinky')
        self.photo_screen_view.ids.img_preview.add_widget(self.image_preview)
        #Logger.info(f"{__name__}:  path from MediaStore")

        self.photo_screen_view.photoReview = True

    # function to get session images path from shared MediaStore
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
            return pth_list[0]

    def save_photo(self):
        Logger.info(f"{__name__}: Photo {self.file_path} saved")
        self.photo_screen_view.photo_count += 1
        self.image_preview.reload()
        self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)
        self.photo_screen_view.photoReview = False
        Toast().show("Saved as:\n" + self.file_path)

    def reject_photo(self):
        Logger.info(f"{__name__}: Photo {self.file_path} rejected")

        path = self.file_path
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))

        self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)
        self.photo_screen_view.photoReview = False

    def flash(self):
        icon = self.photo_screen_view.ids.preview.flash()
        if icon == 'on':
            self.ids.flash_and_cancel.background_normal = 'assets/icons/flash.png'
            self.ids.flash_and_cancel.background_down = 'assets/icons/flash.png'
        elif icon == 'auto':
            self.ids.flash_and_cancel.background_normal = 'assets/icons/flash-auto.png'
            self.ids.flash_and_cancel.background_down = 'assets/icons/flash-auto.png'
        else:
            self.ids.flash_and_cancel.background_normal = 'assets/icons/flash-off.png'
            self.ids.flash_and_cancel.background_down = 'assets/icons/flash-off.png'

    def select_camera(self, facing):
        self.photo_screen_view.ids.preview.select_camera(facing)