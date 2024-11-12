import os

from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.app import App

from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer
)

from widgets.button_extra_behavior import ButtonExtraBehavior


class MedicalCard(ButtonExtraBehavior, MDCard):
    name = StringProperty()
    date = StringProperty()
    status = NumericProperty()
    image = StringProperty()
    status_variants = {
        0: {
            "verdict": "хорошо",
            "rgba": [0.596, 0.835, 0.556, 1],
        },
        1: {
            "verdict": "срок истёк",
            "rgba": [0.87, 0.27, 0.27, 1],
        },
        2: {
            "verdict": "срок истекает",
            "rgba": [1, 0.6, 0, 1],
        }
    }
    Builder.load_file("kv_files/medicalcard.kv")

    def __init__(self, name="Справка", date="01.01.1935", status=0, image="data/лиссс.png"):
        super().__init__()
        self.name = name
        self.date = date
        self.status = status
        self.expanded = False
        self.set_status(status)
        self.image = image
        self.set_image()

    def on_long_press(self, *args):
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Удалить справку?",
                halign="left",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Отмена"),
                    style="text",
                    on_release=self.close_dialog,
                ),
                MDButton(
                    MDButtonText(text="Удалить"),
                    style="text",
                    on_release=self.delete_card,
                ),
                spacing="8dp",
            ),
        )
        self.dialog.update_width()
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def delete_card(self, *args):
        self.close_dialog()
        docs = App.get_running_app().data['documents']
        images = list(map(lambda x: os.path.abspath(x["scan"].replace("/", "\\")), docs))
        docs.pop(images.index(self.image))
        os.remove(self.image)
        self.parent.remove_widget(self)

    def on_release(self, *args) -> None:
        self.narrow() if self.expanded else self.expand()

    def expand(self):
        self.expanded = True
        card_animation = Animation(height=dp(300), duration=.35, t="out_expo")
        card_animation.start(self)

    def narrow(self):
        self.expanded = False
        card_animation = Animation(height=dp(95), duration=.35, t="out_expo")
        card_animation.start(self)

    def set_image(self):
        pass
        # self.image = App.get_running_app().data['documents'].title['scan']

    def set_status(self, status: int):
        '''
        Color the right line in two colors: green = good and red = bad
        :param status: "good" or "bad"
        :return the message of color changing
        '''
        self.md_bg_color = self.status_variants[status]["rgba"]

        return "The color changed"
