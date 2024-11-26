import os

from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App

from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
    MDDialogContentContainer
)
from kivymd.uix.fitimage import FitImage
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldLeadingIcon,
    MDTextFieldHintText,
    MDTextFieldHelperText,
    MDTextFieldTrailingIcon,
    MDTextFieldMaxLengthText,
)

from widgets.button_extra_behavior import ButtonExtraBehavior
from widgets.textfieldDate import TextFieldDate


class MedicalCard(ButtonExtraBehavior, MDCard):
    name = StringProperty()
    date = StringProperty()
    status = NumericProperty()
    image = StringProperty()
    recommendation = StringProperty()
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

    def __init__(self, name="Справка", date="01.01.1935", status=0, image="data/лиссс.png",
                 recommendation="Все хорошо"):
        super().__init__()
        self.name = name
        self.date = date
        self.status = status
        self.expanded = False
        self.set_status(status)
        self.image = image
        self.recommendation = recommendation
        # App.get_running_app().convert_image_to_text(self.image)
        # " ".join(App.get_running_app().reader.readtext(self.image, detail = 0))
        self.set_image()

    def image_open(self):
        if not self.expanded:
            self.expand()
            return

        # create content and add to the popup
        content = ScatterLayout()
        content.add_widget(Image(source=self.image))

        popup = Popup(title='', content=content, auto_dismiss=True, size_hint=(0.9, 0.9))

        # open the popup
        popup.open()
        print("image is clicked")

    def on_long_press(self, *args):
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Что хотите сделать?",
                halign="left",
            ),
            MDDialogContentContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Удалить",
                                 theme_text_color="Custom",
                                 text_color="red"
                                 ),
                    style="text",
                    on_release=self.delete_card,
                ),
                MDButton(
                    MDButtonText(text="Редактировать"),
                    style="text",
                    on_release=self.edit_card,
                ),
                Widget(),
                orientation="horizontal",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Ничего"),
                    style="text",
                    on_release=self.close_dialog,
                ),
                Widget()
            )
        )
        self.dialog.update_width()
        self.dialog.open()

    def edit_card(self, *args):
        self.close_dialog()

        textfield = MDTextField(
            MDTextFieldHintText(
                text=self.name
            )
        )
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Редактирование",
                halign="left",
            ),

            MDDialogContentContainer(
                MDTextField(
                    MDTextFieldHintText(
                        text="Название"
                    ),
                    text=self.name,
                    id="name"
                ),

                TextFieldDate(
                    text=self.date,
                    id="date"
                ),
                orientation="vertical",
                spacing="10dp"
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Отмена"),
                    style="text",
                    on_release=self.close_dialog,
                ),
                MDButton(
                    MDButtonText(text="Сохранить"),
                    style="text",
                    on_release=self.save_edit,
                ),
                Widget()
            )
        )
        self.dialog.update_width()
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def save_edit(self, *args):
        new_date = self.dialog.ids.content_container.children[0].children[0].text
        new_name = self.dialog.ids.content_container.children[0].children[1].text
        self.name = new_name
        self.date = new_date

        docs = App.get_running_app().data['documents']
        images = list(map(lambda x: os.path.abspath(x["scan"].replace("/", "\\")), docs))
        index = images.index(self.image)
        docs[index]["title"] = self.name
        docs[index]["date"] = self.date

        self.close_dialog()

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
