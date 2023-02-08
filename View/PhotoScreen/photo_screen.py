from View.base_screen import BaseScreenView
from kivy.logger import Logger

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from camera4kivy import Preview
from View.PhotoScreen.components.toast import Toast
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
import os



class PhotoScreenView(BaseScreenView):
    session_name = StringProperty()
    tree_name = StringProperty()
    photo_count = 0
    photoReview = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info(f"{__name__}: Inited")

    def set_tree_name(self, tree_name):
        self.tree_name = tree_name

    def on_enter(self):
        self.photo_count = 0
        self.session_name = self.model.session_name
        self.tree_name = self.model.tree_name
        self.ids.preview.connect_camera(filepath_callback=self.capture_path)


    def on_pre_leave(self):
        self.ids.preview.disconnect_camera()

    def capture_path(self, file_path):
        Logger.info(f"{__name__}: Photo maked, path-> {file_path}")


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
            self.ids.buttons.ids.photo_and_save.min_state_time = 0.3
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


class ButtonsLayout1(RelativeLayout):
    file_path = StringProperty()
    photo_screen_view = ObjectProperty()

    def __init__(self, **args):
        super().__init__(**args)

    def photo(self):
        self.photo_screen_view = self.parent.parent
        tree_name = self.photo_screen_view.tree_name
        session_name = self.photo_screen_view.session_name
        photo_count = self.photo_screen_view.photo_count

        Logger.info(f"{__name__:} -> {self.parent.parent.ids}")
        if tree_name:
            if photo_count == 0:
                self.photo_screen_view.ids.preview.capture_photo(location='photos', subdir=session_name, name=f"{tree_name}")
                self.file_path = f'./photos/{session_name}/{tree_name}.jpg'
            else:
                self.photo_screen_view.ids.preview.capture_photo(location='photos', subdir=session_name,
                                                      name=f"{tree_name}_{photo_count}")
                self.file_path = f'./photos/{session_name}/{tree_name}_{photo_count}.jpg'


            self.image_preview = Image(source=self.file_path, size_hint=(1, .98))
            self.photo_screen_view.ids.preview.add_widget(self.image_preview)
            self.photo_screen_view.photo_count += 1
            self.photo_screen_view.photoReview = True

        else:
            pass

    def save_photo(self):
        print('Photo saved')
        self.photo_screen_view.ids.preview.remove_widget(self.image_preview)
        self.photo_screen_view.photoReview = False
        Toast().show("Saved as:\n" + self.file_path)

    def reject_photo(self):
        print('Photo rejected')
        os.remove(self.file_path)
        #Toast().show("Photo" + self.file_path)
        self.photo_screen_view.ids.preview.remove_widget(self.image_preview)
        #self.photo_screen_view.ids.preview.connect_camera(filepath_callback=self.photo_screen_view.capture_path)

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
