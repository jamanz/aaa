from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedcontrol import (
    MDSegmentedControl, MDSegmentedControlItem
)

class MySegmentedControl(MDSegmentedControl):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        items = []
        print(f"panel width before {self.ids.segment_panel.width}")
        for i in range(6):
            items.append(MDSegmentedControlItem(text=f'{i}'))
            print(f"before change for {i}: texture size: {items[i].texture_size}")
            items[i].texture_update()
            self.ids.segment_panel.width += (
                    items[i].texture_size[0] + self.ids.segment_panel.spacing
            )
            print(f"after change for {i}: texture size:{items[i].texture_size}")
            self.add_widget(items[i])
        print(f"panel width after {self.ids.segment_panel.width}")
        self.ids.segment_panel.width = "100dp"
        print(f"panel width after manual change {self.ids.segment_panel.width}")
        print(self.ids)



class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return (
            MDScreen(
                    MySegmentedControl()
                )
            )



Example().run()