from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText


class MedicalCard(MDCard):
    title = StringProperty()
    desc = StringProperty()
    Builder.load_file("kv_files/card.kv")


class MainApp(MDApp):
    def build(self):
        return Builder.load_file("kv_files/mainapp.kv")

    def on_start(self):
        for names in ("pog", "poggers", "pogchamp", "pogchamp", "pogchamp"):
            self.root.ids.main_scroll.add_widget(
                MedicalCard(style="elevated", title=names, desc="123")
            )
