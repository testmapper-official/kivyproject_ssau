from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty
)

# Loading Multiple .kv files
Builder.load_file('kv_files/templates/main.kv')
Builder.load_file('kv_files/templates/box1.kv')
Builder.load_file('kv_files/templates/box2.kv')
Builder.load_file('kv_files/templates/box3.kv')


# Creating main kv file class
class main_kv(GridLayout):
    pass


class GridApp(App):
    x = NumericProperty(150)
    y = NumericProperty(400)

    def build(self):
        return main_kv()
