import math
import tkinter as tk
from tkinter import messagebox

class FactoryPatternDemo:
    def create_product(self, product_type):
        if product_type == "A":
            return ProductA()
        elif product_type == "B":
            return ProductB()
        elif product_type == "C":
            return ProductC()
        else:
            return None

class ProductA:
    def operation(self):
        return "A", "lightblue", "rectangle"

class ProductB:
    def operation(self):
        return "B", "lightgreen", "oval"

class ProductC:
    def operation(self):
        return "C", "lightcoral", "triangle"

class ObserverPatternDemo:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Observer:
    def __init__(self, label):
        self.label = label

    def update(self, message):
        self.label.config(text=f"Observer received: {message}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Design Patterns Demo")

        self.factory_pattern_demo = FactoryPatternDemo()
        self.observer_pattern_demo = ObserverPatternDemo()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Factory Pattern").pack()
        tk.Button(self.root, text="Create Product A", command=self.create_product_a).pack()
        tk.Button(self.root, text="Create Product B", command=self.create_product_b).pack()
        tk.Button(self.root, text="Create Product C", command=self.create_product_c).pack()
        self.factory_canvas = tk.Canvas(self.root, width=600, height=300, bg="white")
        self.factory_canvas.pack()

        self.factory_canvas.create_rectangle(50, 50, 150, 250, outline="black", width=2)
        self.factory_canvas.create_text(100, 150, text="Factory", font=("Arial", 16))
        self.factory_canvas.create_line(150, 160, 600, 160, fill="black", width=2)
        self.create_gears()

        tk.Label(self.root, text="Observer Pattern").pack()
        self.notification_label = tk.Label(self.root, text="")
        self.notification_label.pack()
        self.observer = Observer(self.notification_label)
        self.observer_pattern_demo.attach(self.observer)

    def create_product_a(self):
        product = self.factory_pattern_demo.create_product("A")
        self.display_product(*product.operation())
        self.observer_pattern_demo.notify("Product A created")

    def create_product_b(self):
        product = self.factory_pattern_demo.create_product("B")
        self.display_product(*product.operation())
        self.observer_pattern_demo.notify("Product B created")

    def create_product_c(self):
        product = self.factory_pattern_demo.create_product("C")
        self.display_product(*product.operation())
        self.observer_pattern_demo.notify("Product C created")

    def display_product(self, product_type, color, shape):
        if shape == "rectangle":
            box = self.factory_canvas.create_rectangle(150, 100, 200, 150, fill=color)
        elif shape == "oval":
            box = self.factory_canvas.create_oval(150, 100, 200, 150, fill=color)
        elif shape == "triangle":
            box = self.factory_canvas.create_polygon(150, 150, 175, 100, 200, 150, fill=color)
        text = self.factory_canvas.create_text(175, 125, text=product_type, font=("Arial", 24))
        self.animate_box(box, text)

    def animate_box(self, box, text):
        def move():
            self.factory_canvas.move(box, 5, 0)
            self.factory_canvas.move(text, 5, 0)
            pos = self.factory_canvas.coords(box)
            if pos[2] < 600:
                self.root.after(50, move)
            else:
                self.factory_canvas.delete(box)
                self.factory_canvas.delete(text)
        move()

    def create_gears(self):
        for i in range(5):
            self.animate_gear(i * 100 + 200, 160, i)

    def animate_gear(self, x, y, index):
        def rotate(angle=0):
            self.factory_canvas.delete(f"gear{index}")
            gear = self.factory_canvas.create_oval(x, y, x + 50, y + 50, outline="black", width=2, tags=f"gear{index}")
            square_coords = self.calculate_rotated_square(x + 25, y + 25, 15, angle)
            square = self.factory_canvas.create_polygon(square_coords, fill="black", tags=f"gear{index}")
            self.root.after(100, rotate, (angle + 10) % 360)
        rotate()

    def calculate_rotated_square(self, cx, cy, size, angle):
        rad = math.radians(angle)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        half_size = size / 2

        points = [
            (cx + cos_val * -half_size - sin_val * -half_size, cy + sin_val * -half_size + cos_val * -half_size),
            (cx + cos_val * half_size - sin_val * -half_size, cy + sin_val * half_size + cos_val * -half_size),
            (cx + cos_val * half_size - sin_val * half_size, cy + sin_val * half_size + cos_val * half_size),
            (cx + cos_val * -half_size - sin_val * half_size, cy + sin_val * -half_size + cos_val * half_size)
        ]

        return [coord for point in points for coord in point]

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()