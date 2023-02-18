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




class PhotoScreenView(BaseScreenView):
    session_name = StringProperty()
    tree_name = ObjectProperty()
    photo_count = 0
    photoReview = BooleanProperty(False)


    saved_filename = StringProperty()
    config_json = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")
        self.config_json_path = pathlib.Path('./config/imortant_path.json').resolve()
        self.file_basic_path = ''

    def set_tree_name(self, tree_name):
        self.tree_name = tree_name

    def on_enter(self):
        self.session_name = self.model.session_name
        self.tree_name = self.model.tree_name


        if platform == 'android':
            # self.file_basic_path = pathlib.Path(f"/storage/emulated/0/DCIM/Treez/{session_name}/{file_name}")
            from android.storage import primary_external_storage_path
            self.photo_count = len(list(pathlib.Path(primary_external_storage_path()).joinpath(
                f'DCIM/Treez/{self.session_name}/').glob(f'{self.tree_name}*jpg')))
        else:
            self.photo_count = len(list(pathlib.Path(self.app.app_folder).joinpath(self.session_name).glob(f'{self.tree_name}*jpg')))
        print('len exist: ', self.photo_count)
        self.ids.preview.connect_camera(filepath_callback=self.capture_path)


    def on_pre_leave(self):
        self.ids.preview.disconnect_camera()

    def on_image_load(self):
        Logger.info(f"{__name__}: on_image_load loaded")


    def capture_path(self, file_path):

        self.file_basic_path = pathlib.Path(file_path).resolve()
        #file_name = self.file_basic_path.name
        file_name = self.file_basic_path.stem
        suf = self.file_basic_path.suffix
        session_name = self.file_basic_path.parent.name
        Logger.info(f"{__name__}: Photo maked, file callback, basic path-> {self.file_basic_path}, session name: {session_name}, filename: {file_name}")
        self.saved_filename = self.file_basic_path.name

        if platform == 'android':
            # self.file_basic_path = pathlib.Path(f"/storage/emulated/0/DCIM/Treez/{session_name}/{file_name}")
            from android.storage import primary_external_storage_path
            self.file_basic_path = pathlib.Path(primary_external_storage_path()).joinpath(
                f'DCIM/Treez/{session_name}/{file_name}')
        else:
            self.file_basic_path = pathlib.Path(self.app.app_folder).joinpath(session_name, self.saved_filename)
            Logger.info(f"primary ext storage {self.file_basic_path}, {os.listdir(self.file_basic_path.parent)}")
        #self.ids.image_holder.source = str(self.file_basic_path)
        #Logger.info(f"{__name__}: soaus added = {self.ids.image_holder.source}")
        #self.ids.image_holder.reload()

        Logger.info(f"{__name__}: capture path ended with reload: {self.file_basic_path}, saved fn: {self.saved_filename}")
        print(self.ids)

        #photos_dir_path = pathlib.Path(file_path).resolve().parent.parent
        #photos_dir_path = pathlib.Path(file_path).resolve().parent.parent
        #Logger.info(f"{__name__}: config json path: {self.config_json_path}")
        self.config_json = JsonStore(str(self.config_json_path))
        self.config_json.put("camera", path=str(self.file_basic_path.parent.parent))
        #print("Photo path: ", photos_dir_path)

    def on_size(self, layout, size):
        if Window.width < Window.height:
            self.ids.photo_layout.orientation = 'vertical'
            #self.ids.preview.size_hint = (1, .8)
            self.ids.preview.size_hint = (1, 1)
            self.ids.buttons.size_hint = (1, .15)
            self.ids.pad_end.size_hint = (1, .1)
        else:
            self.ids.photo_layout.orientation = 'horizontal'
            self.ids.preview.size_hint = (.8, 1)
            self.ids.buttons.size_hint = (.15, 1)
            self.ids.pad_end.size_hint = (.1, 1)

        if platform in ['android', 'ios']:
            self.ids.buttons.ids.photo_and_save.min_state_time = 0.2
        else:
            self.ids.buttons.ids.photo_and_save.min_state_time = 1
        if Window.width < Window.height:
            #self.ids.buttons.ids.other.pos_hint = {'center_x': .2, 'center_y': .5}
            #self.ids.buttons.ids.other.size_hint = (.2, None)
            self.ids.buttons.ids.photo_and_save.pos_hint = {'center_x': .25, 'center_y': .5}
            self.ids.buttons.ids.photo_and_save.size_hint = (.2, None)
            self.ids.buttons.ids.flash_and_cancel.pos_hint = {'center_x': .75, 'center_y': .5}
            self.ids.buttons.ids.flash_and_cancel.size_hint = (.2, None)
        else:
            #self.ids.buttons.ids.other.pos_hint = {'center_x': .5, 'center_y': .8}
            #self.ids.buttons.ids.other.size_hint = (None, .2)
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
        #self.source

    def set_img_source(self, source):
        self.source = source

class ButtonsLayout1(RelativeLayout):
    file_path = StringProperty()
    photo_screen_view = ObjectProperty()

    def __init__(self, **args):
        super().__init__(**args)



        #
        # if self.tree_name:
        #     print('tr: ', tree_name, 'pth  ', f"{tree_name.stem}_{photo_count}{tree_name.suffix}")
        #     if photo_count == 0:
        #         self.photo_screen_view.ids.preview.capture_photo(subdir=session_name, name=f"{tree_name}")
        #     else:
        #         self.photo_screen_view.ids.preview.capture_photo(subdir=session_name,
        #                                                          name=f"{tree_name.stem}_{photo_count}{tree_name.suffix}")
        #
        # self.photo_screen_view = self.parent.parent
        # self.tree_name = self.photo_screen_view.tree_name
        # self.session_name = self.photo_screen_view.session_name
        # self.photo_count = self.photo_screen_view.photo_count

    def photo(self):
        self.photo_screen_view = self.parent.parent
        tree_name = self.photo_screen_view.tree_name
        session_name = self.photo_screen_view.session_name
        photo_count = self.photo_screen_view.photo_count

        Logger.info(f"{__name__:} -> {self.parent.parent.ids}")
        Logger.info(f"{__name__}: self.photo assigned from file basic path, filepath {self.file_path}")
        if photo_count == 0:
            name = f"{tree_name}"
        else:
            name = f"{tree_name}_{photo_count}"
        #self.photo_screen_view.ids.img_preview.clear_widgets()
        #self.photo_screen_view.ids.img_preview.clear_widgets()
        self.photo_screen_view.ids.preview.capture_photo(subdir=session_name, name=name)
        Clock.schedule_once(self.show_photo_image, 0.1)
        Logger.info(f"{__name__}: self.show_photo_image() showed")
        Logger.info(f"{__name__}: img of new photo {self.file_path}")
        Logger.info(f"{__name__}: listdir userhomedir{os.listdir(self.photo_screen_view.app.app_folder)}")

        #Logger.info(f"{__name__}: listdir userhomedir{os.listdir(user_home_dir)}")



    def show_photo_image(self, dt):
        self.file_path = str(self.photo_screen_view.file_basic_path)
        Logger.info(f"{__name__}: show photo image called: file path: {self.file_path}")


        #with self.photo_screen_view.ids.preview.canvas:
        #    Rectangle(source=self.file_path, size=self.photo_screen_view.ids.preview.size, pos=self.photo_screen_view.ids.preview.pos)
        self.image_preview = ImgPrev()
        self.image_preview.set_img_source(str(self.file_path))
        self.image_preview.reload()


        #self.image_preview = Image(source=self.file_path, size=self.photo_screen_view.ids.preview.size, pos=self.photo_screen_view.ids.preview.pos)
        self.photo_screen_view.ids.img_preview.add_widget(self.image_preview)
        # self.photo_screen_view.ids.preview.add_widget(self.image_preview)
        #self.photo_screen_view.ids.preview.сlear_widgets()
        # with self.photo_screen_view.ids.preview.canvas:
        #     self.img_prev = Rectangle(source=self.file_path, size=self.photo_screen_view.ids.preview.size,
        #                               pos=self.photo_screen_view.ids.preview.pos)

        #self.image_preview = Image(source=self.file_path, size_hint=(1, .98))
        #print('idss: ', self.photo_screen_view.ids)
        #self.photo_screen_view.ids.img_preview.add_widget(self.image_preview)
        #self.photo_screen_view.ids.preview.add_widget(self.image_preview)

        self.photo_screen_view.photoReview = True


    def save_photo(self):
        print('Photo saved')
        self.photo_screen_view.photo_count += 1
        #self.photo_screen_view.ids.preview.remove_widget(self.image_preview)
        # self.photo_screen_view.ids.preview.canvas.clear()
        # self.photo_screen_view.ids.preview.remove_widget(self.img_prev)
        # self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)

        self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)
        # self.photo_screen_view.ids.image_holder.reload()

        #self.photo_screen_view.ids.image_holder.remove_from_cache()

        #self.photo_screen_view.ids.image_holder.canvas.after
        # self.photo_screen_view.ids.preview.remove_widget(self.image_preview)

        self.photo_screen_view.photoReview = False
        Toast().show("Saved as:\n" + self.file_path)
        #from camera4kivy import Preview


    def reject_photo(self):
        print('Photo rejected')
        #os.remove(self.file_path)
        # self.photo_screen_view.ids.preview.canvas.ask_update()
        path = self.file_path
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))
        #self.photo_screen_view.ids.preview.canvas.clear()
        #Toast().show("Photo" + self.file_path)
        #self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)


        #self.photo_screen_view.ids.img_preview.clear_widgets()
        # self.photo_screen_view.ids.image_holder.reload()
        self.photo_screen_view.ids.img_preview.remove_widget(self.image_preview)
        from kivy.uix.image import AsyncImage, Image
        # self.photo_screen_view.ids.preview.remove_widget(self.image_preview)

        # self.image_preview.remove_from_cache()

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
