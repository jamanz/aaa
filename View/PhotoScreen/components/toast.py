from kivy.utils import platform

if platform == 'android':

    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    JToast = autoclass('android.widget.Toast')
    JString = autoclass('java.lang.String')


    class Toast():

        @run_on_ui_thread
        def show(self, msg):
            if msg[0] == '/' or 'DCIM/' in msg:
                #msg = 'Saved as:\n' + msg
                context = PythonActivity.mActivity.getApplicationContext()
                JToast.makeText(context, JString(msg), JToast.LENGTH_LONG).show()
            else:
                context = PythonActivity.mActivity.getApplicationContext()
                JToast.makeText(context, JString(msg), JToast.LENGTH_LONG).show()

else:

    from kivy.uix.popup import Popup
    from kivymd.uix.dialog import MDDialog

    from kivy.uix.label import Label
    from kivy.clock import Clock


    class Toast(Popup):
        _md_bg_color = (.8, .3, 1, .5)
        radius = [10, 10, 10, 10]
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_once(self.dismiss_popup, 2)

        def dismiss_popup(self, dt):
            self.dismiss()

        def show(self, msg):
            self.title = 'Saved as'
            self.content = Label(text=msg)
            self.size_hint = (0.5, 0.2)
            self.pos_hint = {'center_x': .5, 'center_y': .1}
            self.open()
