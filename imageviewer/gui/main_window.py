import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, filedialog, Scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageViewerUi(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.parent.title("Image Viewer")
        self.parent.geometry("1000x700")

        frame_top = tk.Frame(self.parent, bg='#34495e', pady=10, padx=10)
        frame_top.pack(fill='x')

        self.entry_path = tk.Entry(frame_top, width=50)
        self.entry_path.pack(side="left", padx=10)

        self.btn_load = tk.Button(
            frame_top, text="Cargar imagen", command=self.on_load_image)
        self.btn_load.pack(side="right", padx=10)

        self.status_label = tk.Label(
            self.parent, text="Listo", bg="#ecf0f1", anchor="w")
        self.status_label.pack(fill="x", padx=5, pady=5)
        # ⚠ Agregar la inicialización de histogram_frame
        self.histogram_frame = tk.Frame(self.parent, bg="white", height=200)
        self.histogram_frame.pack(fill="x", padx=10, pady=10)

        # ⚠ Agregar sliders para evitar errores en reset_controls
        self.brightness_slider = Scale(
            self.parent, from_=-100, to=100, orient="horizontal")
        self.contrast_slider = Scale(
            self.parent, from_=0.1, to=3.0, resolution=0.1, orient="horizontal")
        self.rotation_slider = Scale(
            self.parent, from_=-180, to=180, orient="horizontal")
        self.zoom_slider = Scale(
            self.parent, from_=0.5, to=3.0, resolution=0.1, orient="horizontal")
        self.threshold_slider = Scale(
            self.parent, from_=0, to=1, resolution=0.01, orient="horizontal")

        self.brightness_slider.pack()
        self.contrast_slider.pack()
        self.rotation_slider.pack()
        self.zoom_slider.pack()
        self.threshold_slider.pack()

    def on_load_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif;*.tiff;*.bmp")]
        )
        if filepath:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, filepath)
            self.update_status("Cargando imagen...")

            image_data = self.controller.load_image(filepath)
            if image_data is not None:
                self.show_image(image_data)
                self.update_status(f"Imagen cargada: {filepath}")

                # Resetear los controles
                self.reset_controls()

    def on_export_image(self):
        """Gestiona la exportación de una imagen"""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tif")
            ]
        )

        if save_path:
            self.update_status("Exportando imagen...")
            if self.controller.save_image(save_path):
                self.update_status(f"Imagen guardada en: {save_path}")
            else:
                self.update_status("Error al guardar la imagen")

    def on_reset_image(self):
        """Gestiona la restauración de la imagen original"""
        image_data = self.controller.reset_image()
        if image_data is not None:
            self.show_image(image_data)
            self.reset_controls()
            self.update_status("Imagen restaurada a su estado original")

    def on_adjust_brightness(self, value):
        """Gestiona el ajuste de brillo"""
        value = float(value)
        self.update_status(f"Ajustando brillo: {value}")

        image_data = self.controller.process_image('brightness', value)
        if image_data is not None:
            self.show_image(image_data)

    def on_show_histogram(self):
        """Gestiona la visualización del histograma"""
        histogram_data = self.controller.get_histogram_data()
        if histogram_data is None:
            self.update_status("No hay imagen para mostrar histograma")
            return

        self.update_status("Mostrando histograma")

        # Limpiar el frame del histograma
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()

        # Crear una figura de matplotlib para el histograma
        fig = plt.Figure(figsize=(6, 4))

        if histogram_data['type'] == 'grayscale':
            ax = fig.add_subplot(111)
            ax.hist(histogram_data['data'], bins=256, color='gray', alpha=0.7)
            ax.set_title("Histograma - Escala de Grises")
            ax.set_xlabel("Valor de Intensidad")
            ax.set_ylabel("Frecuencia")
        else:
            # Crear histogramas para cada canal de color
            ax1 = fig.add_subplot(311)
            ax1.hist(histogram_data['r'], bins=256, color='red', alpha=0.7)
            ax1.set_title("Canal Rojo")

            ax2 = fig.add_subplot(312)
            ax2.hist(histogram_data['g'], bins=256, color='green', alpha=0.7)
            ax2.set_title("Canal Verde")

            ax3 = fig.add_subplot(313)
            ax3.hist(histogram_data['b'], bins=256, color='blue', alpha=0.7)
            ax3.set_title("Canal Azul")

            fig.tight_layout()

        # Mostrar en el canvas de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

    def show_image(self, img_data):
        """Muestra la imagen dentro de la UI"""
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.imshow(img_data, cmap="gray")
        ax.axis("off")

        for widget in self.histogram_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_status(self, message):
        """Actualiza el mensaje de estado en la barra inferior"""
        self.status_label.config(text=message)

    def reset_controls(self):
        """Resetea todos los controles a sus valores por defecto"""
        self.brightness_slider.set(0)
        self.contrast_slider.set(1.0)
        self.rotation_slider.set(0)
        self.zoom_slider.set(1.0)
        self.threshold_slider.set(0.5)
