from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from kivy.clock import Clock, mainthread
from _functools import partial
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout

Builder.load_string('''
<CustomSearchBar>:                    
    orientation: 'vertical'
    md_bg_color: 'red'            # to see the current size
    padding: '10dp'
    adaptive_size: True
    MDBoxLayout:
        id: search_box
        orientation: 'vertical'
        adaptive_size: True
        # size_hint_x: 1
        # md_bg_color: "pink"            # to see the current size
        CustomMDTextField:
            id: search_input
            icon_left: "magnify"
            # hint_text: "Field with left icon"
            on_text: root.on_search_input
            size_hint: None, None 
            width: '50dp'
            # height: '50dp'
            mode: 'fill'            # using 'fill' instead of 'round' because searchbar not circular at startup
            halign: "center"
            valign: "center"
            radius: [25, 25, 25, 25]
            on_kv_post: self.bind(focus=self.do_animation)

        MDRecycleView:
            id: suggestions
            # key_viewclass: 'viewclass'
            viewclass: 'MDLabel'
            key_size: 'height'        # this not work
            md_bg_color: 'yellow'        # to see if MDRecycleView is there
            # size_hint: 1, None        # breaks position
            # size_hint_x: 1


            RecycleBoxLayout:
                id: rbl
                spacing: dp(5)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint: 1, None
                orientation: 'vertical'
                height: self.minimum_height

<CustomFloatSearchBar>:        # not heeded, the CustomSearchBar is working without FloatLayout, or it is working just in this case
    md_bg_color: 'blue'        # to see the current size
    CustomSearchBar:
        id: searchbar

''')


class CustomFloatSearchBar(MDFloatLayout):
    pass


class CustomMDTextField(MDTextField):

    def do_animation(self, _, focus):
        width = dp(50) if not focus else int(Window.width * (2 / 3))
        radius = [25, 25, 25, 25] if not focus else [8, 8, 8, 8]
        anim = Animation(width=width, d=.3, radius=radius)
        anim.start(self)


class CustomSearchBar(MDBoxLayout):

    def on_kv_post(self, base_widget):
        # MDBoxLayout.on_kv_post(self, base_widget)
        search_input = self.ids.search_input
        search_input.bind(text=self.on_search_input)

    def on_search_input(self, _, search_text):
        if len(search_text) > 3:  # search is starting from 4 characters

            print(search_text)

            suggest = self.ids.suggestions

            suggest.data = \
                [
                    *suggest.data,
                    {
                        # 'viewclass': 'MDLabel',
                        'text': search_text
                    },
                ]
            self.ids.search_box.height = dp(300)  # I tryet this, but it doesnt' help
            print("DATA:", suggest.data)

            print("MDLabels is here", suggest.children[0].children)  # here is only two MDLabel

    pass


kv = '''
MDBoxLayout:
    md_bg_color: 'gray'
    CustomSearchBar:
        pos_hint: {'left': 1, 'top': 1}        # pos_hint works without MDFloatLayout, or it is working just in this case

'''

if __name__ == "__main__":
    from kivymd.app import MDApp


    class App(MDApp):
        def build(self):
            return Builder.load_string(kv)


    App().run()