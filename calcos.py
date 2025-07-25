"""
CalcOS
Author: Odafeigho

A Kivy-based cross-platform scientific calculator inspired by advanced Casio calculators (e.g., ClassWiz CW Series).
Features a modular, intuitive UI with high-contrast labels, simulation functions (dice roll, coin toss), and graphical solutions.
Modules include: Display, Keypad (numeric and scientific functions), History, and Graphing (with function plotting).
"""

import math
import operator
import sys
import subprocess
import random

# --- Dependency Check Module ---
try:
    import pkg_resources
except ModuleNotFoundError:
    print("pkg_resources not found, attempting to install setuptools...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'], stdout=subprocess.DEVNULL)
        import pkg_resources
        print("setuptools installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing setuptools: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error installing setuptools: {e}")
        sys.exit(1)

def check_and_install_dependencies():
    required = {'kivy', 'matplotlib'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print(f"Installing missing dependencies: {missing}")
        try:
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error during dependency installation: {e}")
            sys.exit(1)

# Run dependency check before importing Kivy, matplotlib, or numpy
check_and_install_dependencies()

# Now import Kivy, matplotlib, and numpy
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

# --- Calculator Logic Backend ---
class CalculatorError(Exception):
    pass

class ScientificCalculator:
    def __init__(self):
        self.operators = {
            '+': (operator.add, 1, 'left'), 
            '-': (operator.sub, 1, 'left'),
            '*': (operator.mul, 2, 'left'), 
            '/': (operator.truediv, 2, 'left'),
            '%': (operator.mod, 2, 'left'), 
            '^': (math.pow, 3, 'right'),
        }
        self.functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'arcsin': math.asin, 'arccos': math.acos, 'arctan': math.atan,
            'log': math.log10, 'ln': math.log,
            'sqrt': math.sqrt, 'abs': abs,
            'fact': self.factorial,
            'pi': math.pi, 'e': math.e,
            'dice': self.dice_roll, 'coin': self.coin_toss,
            'x': lambda x: x  # Added for graphing variable
        }

    def factorial(self, n):
        if isinstance(n, float) and n.is_integer():
            n = int(n)
        if not isinstance(n, int) or n < 0:
            raise CalculatorError("Factorial is defined only for non-negative integers.")
        return math.factorial(n)

    def dice_roll(self, _=None):
        return random.randint(1, 6)

    def coin_toss(self, _=None):
        return random.choice(['Heads', 'Tails'])

    def evaluate(self, expression, x=None):
        try:
            safe_dict = {**self.functions, **{k: v[0] for k, v in self.operators.items()}}
            if x is not None:
                safe_dict['x'] = x  # Inject x value for graphing
            expression = expression.replace('^', '**')
            return eval(expression, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            return f"Error: {str(e)}"

# --- UI Modules ---
class Display(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "0"
        self.font_size = 32
        self.halign = 'right'
        self.readonly = True
        self.size_hint_y = 0.2
        self.calculator = ScientificCalculator()

class Keypad(GridLayout):
    def __init__(self, display, **kwargs):
        super().__init__(**kwargs)
        self.cols = 6
        self.display = display
        self.calculator = ScientificCalculator()
        buttons = [
            'C', '(', ')', 'pi', 'e', 'dice',
            'sin', 'cos', 'tan', 'log', 'ln', 'coin',
            '7', '8', '9', '/', 'sqrt', 'fact',
            '4', '5', '6', '*', '^', '%',
            '1', '2', '3', '-', 'arcsin', 'arccos',
            '0', '.', '=', '+', 'arctan', 'abs'
        ]
        for label in buttons:
            btn = Button(
                text=label, 
                font_size=24,
                background_color=(1, 0, 0, 1) if label == 'C' else (0.2, 0.2, 0.2, 1),
                color=(1, 1, 0, 1) if label == 'C' else (1, 1, 1, 1)
            )
            btn.bind(on_release=self.on_button_press)
            self.add_widget(btn)

    def on_button_press(self, instance):
        text = instance.text
        current = self.display.text
        if text == '=':
            result = self.calculator.evaluate(current)
            self.display.text = str(result)
        elif text == 'C':
            self.display.text = "0"
        elif text in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'fact', 'arcsin', 'arccos', 'arctan']:
            self.display.text = text + '(' if current == '0' else current + text + '('
        elif text in ['pi', 'e']:
            self.display.text = str(self.calculator.functions[text]) if current == '0' else current + str(self.calculator.functions[text])
        elif text in ['dice', 'coin']:
            self.display.text = str(self.calculator.functions[text]())
        else:
            if current == '0' and text not in ['+', '-', '*', '/', '.']:
                self.display.text = text
            else:
                self.display.text += text

class HistoryPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.history = Label(text="Calculation history will appear here.", halign='left')
        self.add_widget(self.history)

class GraphingPanel(BoxLayout):
    def __init__(self, calculator, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.calculator = calculator
        self.size_hint_y = None
        self.height = 400

        # Expression input
        self.expr_input = TextInput(
            text='sin(x)', 
            font_size=20, 
            size_hint_y=0.1, 
            multiline=False,
            halign='left'
        )
        self.add_widget(self.expr_input)

        # Plot button
        plot_btn = Button(
            text='Plot', 
            font_size=20, 
            size_hint_y=0.1,
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        plot_btn.bind(on_release=self.plot_graph)
        self.add_widget(plot_btn)

        # Graph display
        self.graph_image = Image(size_hint_y=0.8)
        self.add_widget(self.graph_image)

        # Initial plot
        self.plot_graph(None)

    def plot_graph(self, instance):
        expression = self.expr_input.text.strip()
        if not expression:
            self.graph_image.source = ''
            return

        try:
            # Generate x values
            x = np.linspace(-10, 10, 200)
            # Evaluate expression for each x
            y = [self.calculator.evaluate(expression, x_val) for x_val in x]

            # Create plot
            plt.figure(figsize=(6, 4))
            plt.plot(x, y, color='blue', label=expression)
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Graph of {expression}')
            plt.legend()

            # Save plot to BytesIO
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            plt.close()

            # Update Kivy Image widget
            self.graph_image.texture = CoreImage(buf, ext='png').texture
            buf.close()
        except Exception as e:
            self.graph_image.texture = None
            self.graph_image.source = ''
            self.add_widget(Label(
                text=f"Error plotting: {str(e)}",
                font_size=20,
                size_hint_y=0.1
            ), index=0)

# --- Main Application ---
class CalcOSApp(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.display = Display()
        self.calculator = ScientificCalculator()

        # Main Calculator Tab
        calc_tab = TabbedPanelHeader(text='Calculator')
        calc_content = BoxLayout(orientation='vertical')
        calc_content.add_widget(self.display)
        calc_content.add_widget(Keypad(self.display))
        calc_tab.content = calc_content
        self.add_widget(calc_tab)
        self.default_tab = calc_tab

        # History Tab
        hist_tab = TabbedPanelHeader(text='History')
        hist_content = BoxLayout(orientation='vertical')
        hist_content.add_widget(HistoryPanel())
        hist_tab.content = hist_content
        self.add_widget(hist_tab)

        # Graphing Tab
        graph_tab = TabbedPanelHeader(text='Graph')
        graph_content = BoxLayout(orientation='vertical')
        graph_content.add_widget(GraphingPanel(self.calculator))
        graph_tab.content = graph_content
        self.add_widget(graph_tab)

class CalcOS(App):
    def build(self):
        return CalcOSApp()

if __name__ == '__main__':
    CalcOS().run()