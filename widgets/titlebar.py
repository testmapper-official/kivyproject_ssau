from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.uix.list import MDListItem
from kivy.app import App


class TitleBar(MDListItem):
    surname = StringProperty()
    name = StringProperty()
    avatar = StringProperty()
    Builder.load_file("kv_files/titlebar.kv")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_avatar()

    def set_avatar(self):
        self.avatar = App.get_running_app().data['account']['avatar']

    def on_press(self):
        self.set_avatar()
        print("Title bar is clicked")
