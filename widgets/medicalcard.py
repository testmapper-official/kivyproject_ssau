from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.app import App
from kivy.metrics import dp


class MedicalCard(MDCard):
    title = StringProperty()
    desc = StringProperty()
    scan = StringProperty()
    status_variants = {"good": [0.596, 0.835, 0.556, 1],
                       "bad": [0.87, 0.27, 0.27, 1]}
    Builder.load_file("kv_files/medicalcard.kv")

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.expanded = False
        self.set_status("bad")
        self.set_scan()

    def on_press(self, *args) -> None:
         self.narrow() if self.expanded else self.expand()

    def expand(self):
        self.expanded = True
        card_animation = Animation(height=dp(300), duration=.35, t="out_expo")
        card_animation.start(self)

    def narrow(self):
        self.expanded = False
        card_animation = Animation(height=dp(85), duration=.35, t="out_expo")
        card_animation.start(self)

    def set_scan(self):
        pass
        # self.scan = App.get_running_app().data['documents'].title['scan']

    def set_status(self, status: str):
        '''
        Color the right line in two colors: green = good and red = bad
        :param status: "good" or "bad"
        :return the message of color changing
        '''
        self.md_bg_color = self.status_variants[status]

        return "The color changed"
