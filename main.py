from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty

from kivymd.app import MDApp

from widgets import MedicalCard, TitleBar
import json
import os

Window.size = (330, 550)


class MainApp(MDApp):
    data = DictProperty()

    def build(self):
        if os.path.isfile("data/account.json"):
            with open("data/account.json", 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "account": {
                    "avatar": "data/лиссс.png"
                }
            }
        return Builder.load_file("kv_files/mainapp.kv")

    def createCard(self):
        self.root.ids.main_scroll.add_widget(
            MedicalCard()
        )

    def on_stop(self):
        with open("data/account.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(self.data))


if __name__ == '__main__':
    MainApp().run()
