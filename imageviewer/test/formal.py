import tkinter as tk
import numpy as np
import os
from tkinter import filedialog, Scale, messagebox
from image_processor import ImageProcessor
from PIL import ImageTk, Image


class ImageViewer:
    def __init__(self, root):

        self.current_image_path = ''
        self.processor = ImageProcessor()

        self.root = root
        self.root.title("Image viewr")
        self.root.geometry("1000x700")
        self.root.configure(background="white")

        self.image_label = tk.Label(self.root)
        self.image_label.pack(side="left")

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side="left")

        self.open_btn = tk.Button(
            self.control_frame,
            text="Open", command=self.open_image)
        self.open_btn.pack(side="left")
        self.brightness_slider = tk.Scale(self.root, from_=-1.0, to=1.0, resolution=0.01,
                                          orient="horizontal", label="Brillo",
                                          command=self.on_adjust_brightness)
        self.brightness_slider.pack(pady=5)

        # 🖼 Label para mostrar la imagen
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def open_image(self):
        self.current_image_path = filedialog.askopenfilename(
            defaultextension=".jpg", filetypes=[("All Files", "*.*"),
                                                ("JPEG", "*.jpg"), ("PNG", ".png")])
        if self.current_image_path:
            self.load_image()

    def load_image(self):
        image_loaded = self.processor._load_image(self.current_image_path)
        if image_loaded.dtype != np.uint8:
            image_loaded = (image_loaded * 255).clip(0, 255).astype(np.uint8)
        image = Image.fromarray(image_loaded)
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.tk_image)

    def on_adjust_brightness(self, value):
        factor = float(value)

        # Aplicar el ajuste de brillo con tu biblioteca
        adjusted_image = self.processor.brightness(factor)

        # Convertir la imagen ajustada a formato uint8 para que Tkinter la muestre
        adjusted_image = self.processor.to_uint8(adjusted_image)

        # Mostrar la imagen actualizada en la UI
        self.show_image(adjusted_image)

    def show_image(self, img_data):
        """Convierte la imagen NumPy a un formato compatible con Tkinter y la muestra"""
        # Convertir NumPy a PIL
        image_pil = Image.fromarray(img_data)

        # Convertir PIL a Tkinter
        self.tk_image = ImageTk.PhotoImage(image_pil)

        # Actualizar el Label con la nueva imagen
        self.image_label.configure(image=self.tk_image)
        # Evitar que la imagen sea eliminada por el recolector de basura
        self.image_label.image = self.tk_image


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
