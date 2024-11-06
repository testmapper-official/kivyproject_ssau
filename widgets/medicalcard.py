from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp

from kivymd.uix.card import MDCard

class MedicalCard(MDCard):
    name = StringProperty()
    date = StringProperty()
    status = StringProperty()
    image = StringProperty()
    scan = StringProperty()
    status_variants = {"хорошо": [0.596, 0.835, 0.556, 1],
                       "срок истёк": [0.87, 0.27, 0.27, 1]}
    Builder.load_file("kv_files/medicalcard.kv")

    def __init__(self, name="Справка", date="01.01.1935", status="хорошо", image="data/лиссс.png", **kwargs):
        super().__init__(kwargs)
        self.name = name
        self.date = date
        self.status = status
        self.expanded = False
        self.set_status(status)
        self.image = image
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
