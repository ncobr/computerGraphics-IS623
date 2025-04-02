import tkinter as tk
from tkinter import ttk, filedialog, Scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from image_processor import ImageProcessor


class ImageViewerApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.viewer = ImageViewerBackend()
        self.current_image = None  # Para almacenar la imagen actualmente mostrada
        self.original_image = None  # Para guardar la imagen original
        self.init_ui()

    def init_ui(self):
        self.parent.title("Visor y Editor de Imágenes")
        self.parent.geometry("1000x700")
        self.parent.configure(bg="#2c3e50")

        # Frame superior para carga de archivos
        frame_top = tk.Frame(self.parent, bg="#34495e", pady=10, padx=10)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Archivo:", fg="white", bg="#34495e",
                 font=("Arial", 10)).pack(side="left", padx=5)
        self.entry_path = tk.Entry(frame_top, width=50, font=("Arial", 10))
        self.entry_path.pack(side="left", padx=5)

        self.btn_load = tk.Button(
            frame_top, text="Cargar", command=self.load_image, bg="#3498db", fg="white", padx=10
        )
        self.btn_load.pack(side="left", padx=5)

        self.btn_export = tk.Button(
            frame_top, text="Exportar", command=self.export_image, bg="#2ecc71", fg="white", padx=10
        )
        self.btn_export.pack(side="left", padx=5)

        self.btn_reset = tk.Button(
            frame_top, text="Restaurar Original", command=self.reset_image, bg="#e74c3c", fg="white", padx=10
        )
        self.btn_reset.pack(side="left", padx=5)

        # Frame principal
        frame_main = tk.Frame(self.parent, bg="#2c3e50")
        frame_main.pack(expand=True, fill="both", padx=10, pady=10)

        # Área de imagen (lado izquierdo)
        self.frame_image = tk.Frame(
            frame_main, bg="#34495e", width=600, height=500
        )
        self.frame_image.pack(side="left", padx=5, pady=5,
                              expand=True, fill="both")

        # Inicializar con un mensaje
        self.label_no_image = tk.Label(
            self.frame_image, text="Carga una imagen para comenzar",
            fg="white", bg="#34495e", font=("Arial", 12)
        )
        self.label_no_image.pack(expand=True)

        # Panel de pestañas para opciones (lado derecho)
        self.notebook = ttk.Notebook(frame_main)
        self.notebook.pack(side="right", padx=5, pady=5, fill="both")

        # --- Pestaña 1: Ajustes básicos ---
        self.tab_basic = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_basic, text="Ajustes Básicos")

        # Brillo
        frame_brightness = tk.Frame(self.tab_basic, pady=10)
        frame_brightness.pack(fill="x")
        tk.Label(frame_brightness, text="Brillo:").pack(side="top")
        self.brightness_slider = Scale(
            frame_brightness, from_=-0.5, to=0.5, resolution=0.05,
            orient="horizontal", command=self.adjust_brightness, length=200
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side="top")

        # Contraste
        frame_contrast = tk.Frame(self.tab_basic, pady=10)
        frame_contrast.pack(fill="x")
        tk.Label(frame_contrast, text="Contraste:").pack(side="top")
        self.contrast_slider = Scale(
            frame_contrast, from_=0.5, to=2.0, resolution=0.1,
            orient="horizontal", command=self.adjust_contrast, length=200
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(side="top")

        # Rotación
        frame_rotation = tk.Frame(self.tab_basic, pady=10)
        frame_rotation.pack(fill="x")
        tk.Label(frame_rotation, text="Rotación:").pack(side="top")
        self.rotation_slider = Scale(
            frame_rotation, from_=-180, to=180, resolution=5,
            orient="horizontal", command=self.rotate_image, length=200
        )
        self.rotation_slider.set(0)
        self.rotation_slider.pack(side="top")

        # Zoom
        frame_zoom = tk.Frame(self.tab_basic, pady=10)
        frame_zoom.pack(fill="x")
        tk.Label(frame_zoom, text="Zoom:").pack(side="top")
        self.zoom_slider = Scale(
            frame_zoom, from_=0.5, to=2.0, resolution=0.1,
            orient="horizontal", command=self.zoom_image, length=200
        )
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(side="top")

        # --- Pestaña 2: Filtros de color ---
        self.tab_color = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_color, text="Filtros de Color")

        # Botones para filtros de color
        filters_frame = tk.Frame(self.tab_color, pady=10)
        filters_frame.pack(fill="x")

        # Filtros RGB
        rgb_frame = tk.LabelFrame(
            filters_frame, text="Filtros RGB", padx=5, pady=5)
        rgb_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(rgb_frame, text="Rojo", command=lambda: self.apply_filter("red"),
                  bg="#ff6b6b", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(rgb_frame, text="Verde", command=lambda: self.apply_filter("green"),
                  bg="#51cf66", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(rgb_frame, text="Azul", command=lambda: self.apply_filter("blue"),
                  bg="#339af0", width=10).pack(side="left", padx=5, pady=5)

        # Filtros adicionales
        cmyk_frame = tk.LabelFrame(
            filters_frame, text="Filtros CMYK", padx=5, pady=5)
        cmyk_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(cmyk_frame, text="Cian", command=lambda: self.apply_filter("cyan"),
                  bg="#15aabf", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(cmyk_frame, text="Magenta", command=lambda: self.apply_filter("magenta"),
                  bg="#e64980", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(cmyk_frame, text="Amarillo", command=lambda: self.apply_filter("yellow"),
                  bg="#fcc419", width=10).pack(side="left", padx=5, pady=5)

        # Otros filtros
        other_frame = tk.LabelFrame(
            filters_frame, text="Otros Filtros", padx=5, pady=5)
        other_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(other_frame, text="Invertir", command=self.invert_colors,
                  bg="#868e96", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(other_frame, text="Gris (Prom)", command=lambda: self.grayscale("average"),
                  bg="#adb5bd", width=10).pack(side="left", padx=5, pady=5)
        tk.Button(other_frame, text="Gris (Lum)", command=lambda: self.grayscale("luminosity"),
                  bg="#ced4da", width=10).pack(side="left", padx=5, pady=5)

        # Control deslizante para umbral de binarización
        bin_frame = tk.LabelFrame(
            self.tab_color, text="Binarización", padx=5, pady=5)
        bin_frame.pack(fill="x", padx=10, pady=5)

        self.threshold_slider = Scale(
            bin_frame, from_=0.0, to=1.0, resolution=0.05,
            orient="horizontal", length=200
        )
        self.threshold_slider.set(0.5)
        self.threshold_slider.pack(side="left", padx=5, pady=5)

        tk.Button(bin_frame, text="Binarizar", command=self.binarize_image,
                  bg="#495057", fg="white", width=10).pack(side="left", padx=5, pady=5)

        # --- Pestaña 3: Histograma ---
        self.tab_histogram = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_histogram, text="Histograma")

        # Frame para el histograma
        self.histogram_frame = tk.Frame(self.tab_histogram, bg="#34495e")
        self.histogram_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón para mostrar histograma
        tk.Button(
            self.histogram_frame, text="Mostrar Histograma",
            command=self.show_histogram, bg="#9b59b6", fg="white"
        ).pack(pady=20)

        # Frame de estado (parte inferior)
        self.status_frame = tk.Frame(self.parent, bg="#34495e", height=25)
        self.status_frame.pack(fill="x", side="bottom")

        self.status_label = tk.Label(
            self.status_frame, text="Listo", fg="white", bg="#34495e",
            anchor="w", padx=10
        )
        self.status_label.pack(fill="x")

    def update_status(self, message):
        """Actualiza el mensaje de estado en la barra inferior."""
        self.status_label.config(text=message)
        self.parent.update_idletasks()

    def load_image(self):
        """Abre el diálogo para seleccionar una imagen y la carga en el visor."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif;*.tiff;*.bmp")]
        )
        if filepath:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, filepath)
            self.update_status("Cargando imagen...")

            img_data = self.viewer.load_image(filepath)
            if img_data is not None:
                self.original_image = np.copy(
                    img_data)  # Guardar copia original
                # Imagen actual para procesamiento
                self.current_image = np.copy(img_data)
                self.show_image(self.current_image)
                self.update_status(f"Imagen cargada: {filepath}")

                # Resetear los controles
                self.brightness_slider.set(0)
                self.contrast_slider.set(1.0)
                self.rotation_slider.set(0)
                self.zoom_slider.set(1.0)
                self.threshold_slider.set(0.5)

    def show_image(self, img_data):
        """Muestra la imagen dentro de la UI."""
        # Limpiar el frame de imagen
        for widget in self.frame_image.winfo_children():
            widget.destroy()

        # Crear una figura de matplotlib y mostrar la imagen
        fig, ax = plt.subplots(figsize=(6, 5))

        # Verificar si es una imagen en escala de grises o binaria
        if len(img_data.shape) == 2 or (len(img_data.shape) == 3 and img_data.shape[2] == 1):
            ax.imshow(img_data, cmap='gray')
        else:
            # Para imágenes RGB o RGBA
            ax.imshow(img_data)

        ax.axis("off")  # Ocultar ejes
        plt.tight_layout()

        # Mostrar en el canvas de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_image)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

    def export_image(self):
        """Abre el diálogo para guardar la imagen procesada."""
        if self.current_image is None:
            self.update_status("No hay imagen para exportar")
            return

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
            try:
                plt.imsave(save_path, self.current_image, cmap='gray' if len(
                    self.current_image.shape) == 2 else None)
                self.update_status(f"Imagen guardada en: {save_path}")
            except Exception as e:
                self.update_status(f"Error al guardar la imagen: {str(e)}")

    def reset_image(self):
        """Restaura la imagen original."""
        if self.original_image is not None:
            self.current_image = np.copy(self.original_image)
            self.show_image(self.current_image)

            # Resetear los controles
            self.brightness_slider.set(0)
            self.contrast_slider.set(1.0)
            self.rotation_slider.set(0)
            self.zoom_slider.set(1.0)

            self.update_status("Imagen restaurada a su estado original")

    # --- Funciones para procesar imágenes ---

    def adjust_brightness(self, value):
        """Ajusta el brillo de la imagen usando el valor del deslizador."""
        if self.current_image is None:
            return

        value = float(value)
        self.update_status(f"Ajustando brillo: {value}")

        processed = self.viewer.processor.brightness(
            value, self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def adjust_contrast(self, value):
        """Ajusta el contraste de la imagen usando el valor del deslizador."""
        if self.current_image is None:
            return

        value = float(value)
        self.update_status(f"Ajustando contraste: {value}")

        processed = self.viewer.processor.adjust_contrast(
            value, self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def rotate_image(self, angle):
        """Rota la imagen según el ángulo especificado."""
        if self.current_image is None:
            return

        angle = float(angle)
        self.update_status(f"Rotando imagen: {angle}°")

        processed = self.viewer.processor.rotate_image(
            angle, self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def zoom_image(self, factor):
        """Aplica zoom a la imagen según el factor especificado."""
        if self.current_image is None:
            return

        factor = float(factor)
        self.update_status(f"Aplicando zoom: {factor}x")

        processed = self.viewer.processor.zoom_image(
            factor, None, self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def apply_filter(self, filter_type):
        """Aplica un filtro de color a la imagen."""
        if self.current_image is None:
            return

        self.update_status(f"Aplicando filtro: {filter_type}")

        if filter_type == "red":
            processed = self.viewer.processor.red_layer(self.original_image)
        elif filter_type == "green":
            processed = self.viewer.processor.green_layer(self.original_image)
        elif filter_type == "blue":
            processed = self.viewer.processor.blue_layer(self.original_image)
        elif filter_type == "cyan":
            processed = self.viewer.processor.cyan_layer(self.original_image)
        elif filter_type == "magenta":
            processed = self.viewer.processor.magenta_layer(
                self.original_image)
        elif filter_type == "yellow":
            processed = self.viewer.processor.yellow_layer(self.original_image)

        self.current_image = processed
        self.show_image(self.current_image)

    def invert_colors(self):
        """Invierte los colores de la imagen."""
        if self.current_image is None:
            return

        self.update_status("Invirtiendo colores")

        processed = self.viewer.processor.invert_colors(self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def grayscale(self, method):
        """Convierte la imagen a escala de grises según el método especificado."""
        if self.current_image is None:
            return

        self.update_status(f"Convirtiendo a escala de grises: {method}")

        if method == "average":
            processed = self.viewer.processor.grayscale_average(
                self.original_image)
        elif method == "luminosity":
            processed = self.viewer.processor.grayscale_luminosity(
                self.original_image)
        elif method == "midgray":
            processed = self.viewer.processor.grayscale_midgray(
                self.original_image)

        self.current_image = processed
        self.show_image(self.current_image)

    def binarize_image(self):
        """Binariza la imagen según el umbral establecido."""
        if self.current_image is None:
            return

        threshold = self.threshold_slider.get()
        self.update_status(f"Binarizando imagen con umbral: {threshold}")

        processed = self.viewer.processor.binarize_image(
            threshold, self.original_image)
        self.current_image = processed
        self.show_image(self.current_image)

    def show_histogram(self):
        """Muestra el histograma de la imagen actual."""
        if self.current_image is None:
            self.update_status("No hay imagen para mostrar histograma")
            return

        self.update_status("Mostrando histograma")

        # Limpiar el frame del histograma
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()

        # Crear una figura de matplotlib para el histograma
        fig = plt.Figure(figsize=(6, 4))

        # Verificar si es una imagen en escala de grises
        if len(self.current_image.shape) == 2:
            ax = fig.add_subplot(111)
            ax.hist(self.current_image.flatten(),
                    bins=256, color='gray', alpha=0.7)
            ax.set_title("Histograma - Escala de Grises")
            ax.set_xlabel("Valor de Intensidad")
            ax.set_ylabel("Frecuencia")
        else:
            # Crear histogramas para cada canal de color
            r_data = self.current_image[:, :, 0].flatten()
            g_data = self.current_image[:, :, 1].flatten()
            b_data = self.current_image[:, :, 2].flatten()

            ax1 = fig.add_subplot(311)
            ax1.hist(r_data, bins=256, color='red', alpha=0.7)
            ax1.set_title("Canal Rojo")

            ax2 = fig.add_subplot(312)
            ax2.hist(g_data, bins=256, color='green', alpha=0.7)
            ax2.set_title("Canal Verde")

            ax3 = fig.add_subplot(313)
            ax3.hist(b_data, bins=256, color='blue', alpha=0.7)
            ax3.set_title("Canal Azul")

            fig.tight_layout()

        # Mostrar en el canvas de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")


class ImageViewerBackend:
    def __init__(self):
        self.processor = None
        self.image_data = None

    def load_image(self, filepath):
        """Carga la imagen desde el archivo seleccionado."""
        if filepath:
            self.processor = ImageProcessor(filepath)
            self.image_data = self.processor.logo
            return self.image_data
        return None


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = ImageViewerApp(parent=ROOT)
    ROOT.mainloop()
