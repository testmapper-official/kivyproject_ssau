from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.textfield import MDTextField

KV = '''
<TextFieldDate>
    on_focus: root.show_date_picker(self.focus)
    text: root.text
    
    MDTextFieldHintText:
        text: "Дата"
'''


class TextFieldDate(MDTextField):
    Builder.load_string(KV)

    def __init__(self, text, **kwargs):
        super().__init__(kwargs)
        self.text = text

    def on_ok_date(self, instance_date_picker):
        instance_date_picker.dismiss()
        date = instance_date_picker.get_date()[0]
        date = date.strftime("%d.%m.%Y")
        self.text = date

    def show_date_picker(self, focus):
        if not focus:
            return
        date_dialog = MDDockedDatePicker()
        date_dialog.pos = [
            Window.width / 2 - date_dialog.width / 2,
            self.y
        ]
        date_dialog.bind(on_cancel=date_dialog.dismiss)
        date_dialog.bind(on_ok=self.on_ok_date)
        date_dialog.open()
