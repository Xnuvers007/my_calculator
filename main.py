import time
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
import sympy as sp

# Konfigurasi Window (Opsional untuk testing di PC)
Window.size = (350, 600)

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: 0.1, 0.1, 0.1, 1  # Background gelap profesional

    MDTopAppBar:
        title: "Scientific Calc"
        elevation: 2
        pos_hint: {"top": 1}
        md_bg_color: 0.2, 0.2, 0.2, 1
        specific_text_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"
        size_hint_y: 0.3

        MDTextField:
            id: input_field
            hint_text: "Masukkan Ekspresi (contoh: sin(x) + x**2)"
            helper_text: "Gunakan 'x' untuk variabel simbolik"
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
            text_color: 0, 1, 0, 1  # Hijau terminal
            font_style: "H5"
            halign: "right"

    MDGridLayout:
        cols: 4
        spacing: "10dp"
        padding: "10dp"
        size_hint_y: 0.7
        id: button_grid
'''

class ScientificCalc(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.screen = Builder.load_string(KV)
        
        # Mapping tombol
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
        for btn in buttons:
            button = MDFillRoundFlatButton(
                text=btn,
                font_size="18sp",
                size_hint=(1, 1)
            )
            button.bind(on_release=self.on_button_press)
            
            # Styling khusus untuk tombol operasi
            if btn in ['=', 'C', 'DEL']:
                button.md_bg_color = (1, 0.3, 0.3, 1) # Merah pudar
            elif btn in ['solve', 'diff', 'int']:
                button.md_bg_color = (0.3, 0.6, 1, 1) # Biru
                
            grid.add_widget(button)

        # Variabel untuk double back exit
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
            # Tambahkan spasi untuk fungsi agar rapi
            if button_text in ['sin', 'cos', 'tan', 'sqrt']:
                new_text = current_text + button_text + "("
            else:
                new_text = current_text + button_text
            self.screen.ids.input_field.text = new_text

    def calculate_result(self, expression):
        try:
            # Gunakan sympify untuk evaluasi aman (support akar, pangkat, dll)
            # Hindari eval() Python murni demi keamanan
            expr = sp.sympify(expression)
            result = expr.evalf() # Evaluasi numerik
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
                # Asumsi persamaan diset sama dengan 0
                res = sp.solve(expr, x)
                display_text = f"x = {res}"
            
            self.screen.ids.result_label.text = str(display_text)
            
        except Exception as e:
            self.screen.ids.result_label.text = "Error Logic"
            toast(f"Gunakan variabel 'x'. Error: {str(e)}")

    def events(self, instance, keyboard, keycode, text, modifiers):
        # Tombol Back di Android biasanya kode 27 (Escape di PC)
        if keyboard in (1001, 27): 
            if time.time() - self.last_back_time > 2:
                self.last_back_time = time.time()
                toast("Tekan sekali lagi untuk keluar")
                return True # Jangan tutup dulu
            else:
                return False # Biarkan sistem menutup aplikasi
        return False

if __name__ == '__main__':
    ScientificCalc().run()
