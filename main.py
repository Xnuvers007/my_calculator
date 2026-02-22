import time
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
import sympy as sp

# PENTING: Window.size dihapus agar aplikasi Fullscreen dan responsif di Android

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDTopAppBar:
        title: "Scientific Calc"
        elevation: 2
        pos_hint: {"top": 1}
        md_bg_color: 0.2, 0.2, 0.2, 1
        specific_text_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "15dp"
        size_hint_y: 0.35 # Sedikit diperbesar agar input tidak terpotong

        MDTextField:
            id: input_field
            hint_text: "Ekspresi (contoh: sin(x) + x**2)"
            helper_text: "Gunakan 'x' untuk variabel"
            helper_text_mode: "on_focus"
            multiline: False
            font_size: "24sp"
            foreground_color: 1, 1, 1, 1
            cursor_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0

        MDLabel:
            id: result_label
            text: "Hasil: "
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            font_style: "H5"
            halign: "right"
            size_hint_y: None
            height: self.texture_size[1]

    MDGridLayout:
        cols: 4
        spacing: "8dp" # Jarak antar tombol disesuaikan
        padding: "10dp"
        size_hint_y: 0.65
        id: button_grid
'''

class ScientificCalc(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)
        
        buttons = [
            'C', 'DEL', '(', ')',
            'sin', 'cos', 'tan', 'sqrt',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'x', '+',
            'diff', 'int', 'solve', '='
        ]
        
        grid = self.screen.ids.button_grid
        from kivymd.uix.button import MDFillRoundFlatButton
        for btn in buttons:
            button = MDFillRoundFlatButton(
                text=btn,
                font_size="20sp", # Ukuran font tombol diperbesar sedikit
                size_hint=(1, 1)  # Agar tombol mengisi ruang kosong secara merata
            )
            button.bind(on_release=self.on_button_press)
            
            if btn in ['=', 'C', 'DEL']:
                button.md_bg_color = (0.8, 0.2, 0.2, 1) 
            elif btn in ['solve', 'diff', 'int']:
                button.md_bg_color = (0.2, 0.5, 0.8, 1) 
                
            grid.add_widget(button)

        self.last_back_time = 0
        Window.bind(on_keyboard=self.events)
        
        return self.screen

    def on_button_press(self, instance):
        current_text = self.screen.ids.input_field.text
        button_text = instance.text

        if button_text == 'C':
            self.screen.ids.input_field.text = ""
            self.screen.ids.result_label.text = "Hasil: "
        elif button_text == 'DEL':
            self.screen.ids.input_field.text = current_text[:-1]
        elif button_text == '=':
            self.calculate_result(current_text)
        elif button_text == 'diff':
            self.calculate_symbolic(current_text, 'diff')
        elif button_text == 'int':
            self.calculate_symbolic(current_text, 'integrate')
        elif button_text == 'solve':
            self.calculate_symbolic(current_text, 'solve')
        else:
            if button_text in ['sin', 'cos', 'tan', 'sqrt']:
                new_text = current_text + button_text + "("
            else:
                new_text = current_text + button_text
            self.screen.ids.input_field.text = new_text

    def calculate_result(self, expression):
        try:
            expr = sp.sympify(expression)
            result = expr.evalf()
            self.screen.ids.result_label.text = f"= {result:.4f}"
        except Exception as e:
            self.screen.ids.result_label.text = "Error"
            toast("Format salah/Invalid Syntax")

    def calculate_symbolic(self, expression, operation):
        try:
            x = sp.symbols('x')
            expr = sp.sympify(expression)
            
            if operation == 'diff':
                res = sp.diff(expr, x)
                display_text = f"d/dx: {res}"
            elif operation == 'integrate':
                res = sp.integrate(expr, x)
                display_text = f"∫: {res} + C"
            elif operation == 'solve':
                res = sp.solve(expr, x)
                display_text = f"x = {res}"
            
            self.screen.ids.result_label.text = str(display_text)
            
        except Exception as e:
            self.screen.ids.result_label.text = "Error Logic"
            toast("Gunakan variabel 'x'")

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27): 
            if time.time() - self.last_back_time > 2:
                self.last_back_time = time.time()
                toast("Tekan sekali lagi untuk keluar")
                return True
            else:
                return False
        return False

if __name__ == '__main__':
    ScientificCalc().run()
