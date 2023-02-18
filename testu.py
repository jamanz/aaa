from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen


# create camera popup 
class CameraDialog(ModalView):
    # initiate caller variable 
    caller = None

    # disconnect the camera when close the dialog 
    def on_dismiss(self):
        self.ids.camera_widget.disconnect_camera()

        # open the dialog and connect the camera this

    def open_camera(self, caller):
        # set the caller variable, so we can access their properties and children 
        self.caller = caller
        # connect to the camera provider 
        self.ids.camera_widget.connect_camera(
            filepath_callback=self.filepath_callback,
            # set the camera resolution 
            analyze_pixels_resolution=720,
        )
        # open the camera dialog 
        self.open()

    def record_video(self, state):
        from kivy import platform
        if state:
            # store the video in front dir if is recorded using front camera and back if it recorded with back camera 
            dir = self.ids.camera_widget.preview.facing
            if platform == 'android':
                location = 'private'
            else:
                location = '.'
                # set cache folder as folder for the image and camera_shot as image name location on android can be 'shared'
            # or 'private', other values default to 'shared'. The value 'shared' specifies Android shared storage 
            # DCIM/<appname>. The value 'private' specifies app local storage app_storage_path()/DCIM. If you want a 
            # different location use 'private' and move the resulting file based on the path provided by filepath_callback. 
            self.ids.camera_widget.capture_video(location=location, subdir=dir)
        else:
            self.ids.camera_widget.stop_capture_video()

    def filepath_callback(self, file_path):
        from kivymd.toast import toast
        # test if the path for image or video 
        if 'jpg' in file_path:
            # set the token image path tobe image_holder source 
            self.caller.ids.image_holder.source = file_path
            # reload the image to display the token image 
            self.caller.ids.image_holder.reload()

        elif 'mp4' in file_path:
            self.caller.ids.video_player.source = file_path

        toast(str(file_path))

        # dismiss the camera dialog when we take the image 
        self.dismiss()

        # toggle the camera used on android to use the front camera

    def select_camera(self, facing):
        self.ids.camera_widget.select_camera(facing)

        # take a camera shot

    def capture_photo(self):
        from kivy import platform
        if platform == 'android':
            location = 'private'
            # store the image in front dir if is captured using front camera and back if it captured with back camera 
            dir = self.ids.camera_widget.preview.facing
        else:
            location = '.'
            dir = 'camera'

            # set camera folder as folder for the image location on android can be 'shared'
        # or 'private', other values default to 'shared'. The value 'shared' specifies Android shared storage 
        # DCIM/<appname>. The value 'private' specifies app local storage app_storage_path()/DCIM. 
        self.ids.camera_widget.capture_photo(location=location, subdir=dir)

    # create CameraWidget widget tobe the root widget of the app


class CameraWidget(MDScreen):
    camera_widget = None

    # this method will open the camera dialog 
    def open_camera(self):
        from kivy import platform
        # ask for run time permission on android 
        if platform == 'android':
            from android.permissions import request_permissions, check_permission, Permission

            # check if the permission is granted or not if not ask for it 
            if not check_permission(Permission.CAMERA):
                request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO])
                return
            if not check_permission(Permission.RECORD_AUDIO):
                request_permissions([Permission.RECORD_AUDIO])
                return
        if not self.camera_widget:
            self.camera_widget = CameraDialog()

        self.camera_widget.open_camera(self)

    # creating app instance


class App(MDApp):
    # create build method this will launch when the app is building 
    def build(self):
        # here we will specify the app primary color
        self.theme_cls.primary_palette = "Blue"

        # here we will specify the app primary hue 
        self.theme_cls.primary_hue = "500"

        # here we will specify the app accent color
        self.theme_cls.accent_palette = "Amber"

        # here we will specify the app accent hue 
        self.theme_cls.accent_hue = "500"

        # here we will specify the app theme 
        self.theme_cls.theme_style = "Light"

        # load kv file to load the ui using Builder 
        Builder.load_file('main.kv')

        # specify the material style version 
        self.theme_cls.material_style = "M3"

        # return the root widget of the app 
        return CameraWidget()

    # run the app


if __name__ == '__main__':
    app = App()
    app.run()

"""
Костянтин К, [14.02.2023 22:59]
# import camera 4 kivy Preview widget 
#: import Preview camera4kivy.Preview 
 
# import kivy platform 
#: import platform kivy.platform 
 
# create root widget 
<CameraWidget>: 
    # create vertical box 
    MDBoxLayout: 
        orientation:'vertical' 
        MDBoxLayout: 
            # add padding between the widgets and the outer borders 
            padding:"25dp" 
            orientation:'vertical' 
            # add image widget to display the token image 
            AsyncImage: 
                # allow the image to stretch as much as possible and keep the image ratio 
                allow_stretch:True 
                keep_ratio:True 
                # set id for this image so we can referring it anywhere 
                id:image_holder 
                # Some third party image viewers will incorrectly display a .jpg as rotated by 90 degrees. This occurs if 
                # the capture preview orientation is not the same as the device orientation, and the third party viewer 
                # does not use the Exif metadata. 
                canvas.before: 
                    PushMatrix 
                    Rotate: 
                        # rotate the widget by -90 if the image was token using front or 90 if using back camera degree only on android 
                        angle: (90 if self.source and 'front' in self.source else -90) if platform =='android' else 0 
                        origin: self.center 
                canvas.after: 
                    PopMatrix 
            Video: 
                # set the initial state to play the video will start automatically 
                state: 'play' 
                id:video_player 
                allow_stretch:True 
                keep_ratio:True 
                # set eos option to loop this will replay the video automatically 
                options:{'eos': 'loop'} 
                canvas.before: 
                    PushMatrix 
                    Rotate: 
                        # rotate the widget by -90 if the video was recorded using front or 90 if using back 
                        # camera degree only on android 
                        angle:(90 if self.source and 'front' in self.source else -90) if platform =='android' else 0 
                        origin: self.center 
                canvas.after: 
                    PopMatrix 
        MDRaisedButton: 
            size_hint_x:1 
            text:'Open Camera' 
            on_release:root.open_camera() 
 
# style camera dialog widget 
<-CameraDialog>: 
    # use float layout so we can arrange the children top of each other. 
    MDFloatLayout: 
        Preview: 
            id:camera_widget 
            aspect_ratio:  '16:9' 
            allow_stretch:True 
            keep_ratio:False 
        MDBoxLayout: 
            size_hint_y:None 
            height:'50dp' 
            padding:"10dp" 
            # specify the color to be according the app theme 
            md_bg_color:app.theme_cls.bg_darkest[:-1]+[.5] 
            # add RelativeLayout as spacer 
            RelativeLayout 
            # create icon button to close the dialog 
            MDIconButton: 
                icon:'camera-off' 
                on_release:root.dismiss() 
                pos_hint:{'center_x':.5,"center_y":0.5} 
            RelativeLayout 
            # create icon button to capture a photo 
            MDIconButton: 
                icon:'camera-iris' 
                pos_hint:{'center_x':.5,"center_y":0.5} 
                on_release:root.capture_photo() 
            RelativeLayout 
            # create icon button to toggle th camera 
            MDIconButton: 
                icon:'camera-flip' 
                pos_hint:{'center_x':.5,"center_y":0.5} 
                on_release:root.select_camera('toggle') 
            RelativeLayout 
 
            # create icon button to start recording video 
            MDIconButton: 
                icon:'play' 
                pos_hint:{'center_x':.5,"center_y":0.5} 
                on_release: 
                    root.record_video(True if self.icon=='play' else False) 
                    self.icon='stop' if self.icon=='play' else 'play' 
            RelativeLayout 
            # create icon button to toggle flash state 
            MDIconButton: 
                icon:'flash-auto' 
                pos_hint:{'center_x':.5,"center_y":0.5} 
                on_release: 
                    camera_widget.flash() 
                    self.icon='flash-off' if self.icon=='flash' else 'flash' 
            RelativeLayout
"""