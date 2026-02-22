import time
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDFillRoundFlatButton
import sympy as sp

# SANGAT PENTING: Mencegah keyboard HP menutupi layar input saat mengetik
Window.softinput_mode = "below_target"

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: 0.05, 0.05, 0.05, 1

    MDBoxLayout:
        orientation: "vertical"
        size_hint_y: 0.35
        padding: "20dp"
        spacing: "10dp"
        md_bg_color: 0.1, 0.1, 0.12, 1

        # Menggunakan TextField penuh agar dukung Keyboard, Copy, Paste, Select All
        MDTextField:
            id: input_field
            hint_text: "Ketik ekspresi (contoh: 2*a + 5 = 15)"
            font_size: "32sp"
            mode: "fill"
            fill_color_normal: 0.1, 0.1, 0.12, 1
            fill_color_focus: 0.1, 0.1, 0.12, 1
            text_color_normal: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            hint_text_color_normal: 0.5, 0.5, 0.5, 1
            hint_text_color_focus: 0.5, 0.5, 0.5, 1
            line_color_normal: 0, 0, 0, 0
            line_color_focus: 0.4, 0.8, 0.5, 1
            
        MDLabel:
            id: result_label
            text: ""
            halign: "right"
            valign: "top"
            font_size: "26sp"
            theme_text_color: "Custom"
            text_color: 0.4, 0.8, 0.5, 1
            size_hint_y: 0.3

    MDGridLayout:
        id: button_grid
        cols: 4
        padding: "12dp"
        spacing: "8dp"
        size_hint_y: 0.65
        md_bg_color: 0.05, 0.05, 0.05, 1
'''

class ScientificCalc(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = Builder.load_string(KV)
        
        # Tombol 'x' diganti dengan '=' untuk fitur persamaan (equation)
        buttons = [
            'solve', 'diff', 'int', '=',
            'sin', 'cos', 'tan', 'sqrt',
            'C', '(', ')', 'DEL',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', 'EXE', '+'
        ]
        
        grid = self.screen.ids.button_grid
        
        for btn in buttons:
            f_size = "22sp" if len(btn) <= 1 else "16sp"
            button = MDFillRoundFlatButton(text=btn, font_size=f_size, size_hint=(1, 1))
            
            # Pewarnaan Profesional
            if btn in ['C', 'DEL']:
                button.md_bg_color = (0.8, 0.2, 0.2, 1) 
            elif btn == 'EXE':
                button.md_bg_color = (0.2, 0.6, 0.3, 1) # Hijau untuk Eksekusi Numerik
            elif btn in ['/', '*', '-', '+', '=']:
                button.md_bg_color = (0.9, 0.5, 0.1, 1) 
            elif btn in ['sin', 'cos', 'tan', 'sqrt', 'solve', 'diff', 'int', '(', ')']:
                button.md_bg_color = (0.15, 0.25, 0.35, 1) 
            else:
                button.md_bg_color = (0.2, 0.2, 0.2, 1) 
                
            button.bind(on_release=self.on_button_press)
            grid.add_widget(button)

        self.last_back_time = 0
        Window.bind(on_keyboard=self.events)
        return self.screen

    def on_button_press(self, instance):
        input_field = self.screen.ids.input_field
        current_text = input_field.text
        button_text = instance.text

        if button_text == 'C':
            input_field.text = ""
            self.screen.ids.result_label.text = ""
        elif button_text == 'DEL':
            # Menghapus karakter di posisi kursor secara presisi (bukan cuma dari belakang)
            input_field.do_backspace(from_undo=False, mode='bkspc')
        elif button_text == 'EXE':
            if current_text:
                self.calculate_result(current_text)
        elif button_text in ['diff', 'int', 'solve']:
            if current_text:
                self.calculate_symbolic(current_text, button_text)
        else:
            # Menyisipkan teks di posisi kursor secara pintar
            if button_text in ['sin', 'cos', 'tan', 'sqrt']:
                input_field.insert_text(button_text + "(")
            else:
                input_field.insert_text(button_text)

    def calculate_result(self, expression):
        try:
            expr = sp.sympify(expression)
            result = expr.evalf()
            res_str = f"{float(result):.6f}".rstrip('0').rstrip('.') 
            self.screen.ids.result_label.text = f"= {res_str}"
        except Exception:
            self.screen.ids.result_label.text = "Syntax Error"
            toast("Format tidak valid / Mengandung variabel")

    def calculate_symbolic(self, expression, operation):
        try:
            # 1. Menangani format persamaan (contoh: a+5=10 menjadi a+5-10)
            if '=' in expression:
                left, right = expression.split('=', 1)
                expr = sp.sympify(f"({left}) - ({right})")
            else:
                expr = sp.sympify(expression)
                
            # 2. Mendeteksi SEMUA variabel yang ada di dalam ekspresi (a-z)
            variables = list(expr.free_symbols)
            
            if not variables:
                self.screen.ids.result_label.text = "Error: Tidak ada variabel"
                toast("Ketik minimal 1 variabel huruf (a-z)")
                return
                
            # Jika ada banyak variabel (misal a*b), urutkan abjad dan pakai yang pertama
            variables.sort(key=lambda x: str(x))
            target_var = variables[0] 
            
            # 3. Proses Kalkulus/Aljabar secara dinamis
            if operation == 'diff':
                res = sp.diff(expr, target_var)
                display_text = f"d/d{target_var} = {res}"
            elif operation == 'int':
                res = sp.integrate(expr, target_var)
                display_text = f"∫ d{target_var} = {res} + C"
            elif operation == 'solve':
                res = sp.solve(expr, target_var)
                display_text = f"{target_var} = {res}"
            
            self.screen.ids.result_label.text = str(display_text)
            
        except Exception as e:
            self.screen.ids.result_label.text = "Logic Error"
            toast("Pastikan format matematika benar")

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
