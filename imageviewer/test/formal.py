import tkinter as tk
import numpy as np
import os
from tkinter import filedialog, Scale, messagebox, ttk, Frame
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de Imágenes")
        self.root.geometry("1200x800")
        self.root.configure(background="#f0f0f0")

        # Variables de estado
        self.current_image_path = ''
        self.second_image_path = ''
        self.original_image = None
        self.current_image = None
        self.second_image = None
        self.processor = ImageProcessor()

        # Configuración de la interfaz
        self.setup_layout()
        self.setup_controls()

    def setup_layout(self):
        """Configura el layout principal de la aplicación"""
        # Panel izquierdo para la imagen
        self.image_frame = Frame(self.root, bg="#e0e0e0")
        self.image_frame.pack(side="left", fill="both",
                              expand=True, padx=10, pady=10)

        # Panel de información de la imagen
        self.info_frame = Frame(self.image_frame, bg="#e0e0e0")
        self.info_frame.pack(side="top", fill="x")

        self.path_label = tk.Label(
            self.info_frame, text="Ruta: ", bg="#e0e0e0")
        self.path_label.pack(side="left", padx=5)

        self.path_entry = tk.Entry(self.info_frame, width=50)
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Contenedor para la imagen
        self.image_container = Frame(self.image_frame, bg="#d0d0d0")
        self.image_container.pack(side="top", fill="both", expand=True, pady=5)

        self.image_label = tk.Label(self.image_container, bg="#d0d0d0")
        self.image_label.pack(pady=10)

        # Panel derecho para los controles
        self.control_frame = Frame(self.root, bg="#e0e0e0", width=300)
        self.control_frame.pack(side="right", fill="y", padx=10, pady=10)
        self.control_frame.pack_propagate(False)

        # Notebook para organizar los controles por categorías
        self.control_notebook = ttk.Notebook(self.control_frame)
        self.control_notebook.pack(fill="both", expand=True)

        # Pestañas para diferentes categorías de controles
        self.file_tab = Frame(self.control_notebook, bg="#e0e0e0")
        self.adjust_tab = Frame(self.control_notebook, bg="#e0e0e0")
        self.color_tab = Frame(self.control_notebook, bg="#e0e0e0")
        self.transform_tab = Frame(self.control_notebook, bg="#e0e0e0")
        self.advanced_tab = Frame(self.control_notebook, bg="#e0e0e0")

        self.control_notebook.add(self.file_tab, text="Archivo")
        self.control_notebook.add(self.adjust_tab, text="Ajustes")
        self.control_notebook.add(self.color_tab, text="Color")
        self.control_notebook.add(self.transform_tab, text="Transformar")
        self.control_notebook.add(self.advanced_tab, text="Avanzado")

    def setup_controls(self):
        """Configura todos los controles de la interfaz"""
        # Controles de archivo
        self.setup_file_controls()

        # Controles de ajuste
        self.setup_adjust_controls()

        # Controles de color
        self.setup_color_controls()

        # Controles de transformación
        self.setup_transform_controls()

        # Controles avanzados
        self.setup_advanced_controls()

    def setup_file_controls(self):
        """Configuración de controles relacionados con archivos"""
        # Botón para explorar
        self.open_btn = tk.Button(
            self.file_tab, text="Explorar", command=self.open_image, width=20)
        self.open_btn.pack(pady=5)

        # Botón para cargar
        self.load_btn = tk.Button(
            self.file_tab, text="Cargar", command=self.load_image, width=20)
        self.load_btn.pack(pady=5)

        # Botón para guardar
        self.save_btn = tk.Button(
            self.file_tab, text="Guardar", command=self.save_image, width=20)
        self.save_btn.pack(pady=5)

        # Botón para actualizar
        self.update_btn = tk.Button(
            self.file_tab, text="Actualizar", command=self.update_image, width=20)
        self.update_btn.pack(pady=5)

        # Botón para restaurar
        self.restore_btn = tk.Button(
            self.file_tab, text="Restaurar Original", command=self.restore_original, width=20)
        self.restore_btn.pack(pady=5)

    def setup_adjust_controls(self):
        """Configuración de controles de ajuste"""
        # Control de brillo
        self.brightness_frame = Frame(self.adjust_tab, bg="#e0e0e0")
        self.brightness_frame.pack(fill="x", pady=5)

        self.brightness_label = tk.Label(
            self.brightness_frame, text="Brillo:", bg="#e0e0e0")
        self.brightness_label.pack(side="left", padx=5)

        self.brightness_slider = Scale(self.brightness_frame, from_=-1.0, to=1.0, resolution=0.01,
                                       orient="horizontal", command=self.on_adjust_brightness)
        self.brightness_slider.set(0)
        self.brightness_slider.pack(
            side="right", padx=5, fill="x", expand=True)

        # Control de contraste
        self.contrast_frame = Frame(self.adjust_tab, bg="#e0e0e0")
        self.contrast_frame.pack(fill="x", pady=5)

        self.contrast_label = tk.Label(
            self.contrast_frame, text="Contraste:", bg="#e0e0e0")
        self.contrast_label.pack(side="left", padx=5)

        self.contrast_slider = Scale(self.contrast_frame, from_=0.5, to=2.0, resolution=0.01,
                                     orient="horizontal", command=self.on_adjust_contrast)
        self.contrast_slider.set(1)
        self.contrast_slider.pack(side="right", padx=5, fill="x", expand=True)

    def setup_color_controls(self):
        """Configuración de controles de color"""
        # Canales RGB
        self.rgb_frame = Frame(self.color_tab, bg="#e0e0e0")
        self.rgb_frame.pack(fill="x", pady=5)

        self.rgb_label = tk.Label(
            self.rgb_frame, text="Canales RGB:", bg="#e0e0e0")
        self.rgb_label.pack(side="top", anchor="w", padx=5)

        self.r_var = tk.IntVar(value=1)
        self.g_var = tk.IntVar(value=1)
        self.b_var = tk.IntVar(value=1)

        self.r_check = tk.Checkbutton(self.rgb_frame, text="Rojo", variable=self.r_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.r_check.pack(side="left", padx=5)

        self.g_check = tk.Checkbutton(self.rgb_frame, text="Verde", variable=self.g_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.g_check.pack(side="left", padx=5)

        self.b_check = tk.Checkbutton(self.rgb_frame, text="Azul", variable=self.b_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.b_check.pack(side="left", padx=5)

        # Canales CMY
        self.cmy_frame = Frame(self.color_tab, bg="#e0e0e0")
        self.cmy_frame.pack(fill="x", pady=5)

        self.cmy_label = tk.Label(
            self.cmy_frame, text="Canales CMY:", bg="#e0e0e0")
        self.cmy_label.pack(side="top", anchor="w", padx=5)

        self.c_var = tk.IntVar(value=1)
        self.m_var = tk.IntVar(value=1)
        self.y_var = tk.IntVar(value=1)

        self.c_check = tk.Checkbutton(self.cmy_frame, text="Cian", variable=self.c_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.c_check.pack(side="left", padx=5)

        self.m_check = tk.Checkbutton(self.cmy_frame, text="Magenta", variable=self.m_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.m_check.pack(side="left", padx=5)

        self.y_check = tk.Checkbutton(self.cmy_frame, text="Amarillo", variable=self.y_var,
                                      bg="#e0e0e0", command=self.update_channels)
        self.y_check.pack(side="left", padx=5)

        # Zonas claras/oscuras
        self.zones_frame = Frame(self.color_tab, bg="#e0e0e0")
        self.zones_frame.pack(fill="x", pady=5)

        self.zones_label = tk.Label(
            self.zones_frame, text="Zonas:", bg="#e0e0e0")
        self.zones_label.pack(side="left", padx=5)

        self.zone_var = tk.StringVar(value="normal")

        self.normal_radio = tk.Radiobutton(self.zones_frame, text="Normal", variable=self.zone_var,
                                           value="normal", bg="#e0e0e0", command=self.apply_zone_filter)
        self.normal_radio.pack(side="left", padx=5)

        self.light_radio = tk.Radiobutton(self.zones_frame, text="Claras", variable=self.zone_var,
                                          value="light", bg="#e0e0e0", command=self.apply_zone_filter)
        self.light_radio.pack(side="left", padx=5)

        self.dark_radio = tk.Radiobutton(self.zones_frame, text="Oscuras", variable=self.zone_var,
                                         value="dark", bg="#e0e0e0", command=self.apply_zone_filter)
        self.dark_radio.pack(side="left", padx=5)

        # Negativo
        self.negative_btn = tk.Button(self.color_tab, text="Negativo de imagen",
                                      command=self.apply_negative, width=20)
        self.negative_btn.pack(pady=5)

    def setup_transform_controls(self):
        """Configuración de controles de transformación"""
        # Control de rotación
        self.rotation_frame = Frame(self.transform_tab, bg="#e0e0e0")
        self.rotation_frame.pack(fill="x", pady=5)

        self.rotation_label = tk.Label(
            self.rotation_frame, text="Rotación:", bg="#e0e0e0")
        self.rotation_label.pack(side="left", padx=5)

        self.rotation_slider = Scale(self.rotation_frame, from_=0, to=360, resolution=1,
                                     orient="horizontal", command=self.on_rotate)
        self.rotation_slider.set(0)
        self.rotation_slider.pack(side="right", padx=5, fill="x", expand=True)

        # Control de zoom
        self.zoom_frame = Frame(self.transform_tab, bg="#e0e0e0")
        self.zoom_frame.pack(fill="x", pady=5)

        self.zoom_label = tk.Label(self.zoom_frame, text="Zoom:", bg="#e0e0e0")
        self.zoom_label.pack(side="top", anchor="w", padx=5)

        # Coordenadas iniciales para el zoom
        self.zoom_coords_frame = Frame(self.zoom_frame, bg="#e0e0e0")
        self.zoom_coords_frame.pack(fill="x")

        self.x_label = tk.Label(self.zoom_coords_frame,
                                text="X:", bg="#e0e0e0")
        self.x_label.pack(side="left", padx=5)

        self.x_entry = tk.Entry(self.zoom_coords_frame, width=5)
        self.x_entry.insert(0, "0")
        self.x_entry.pack(side="left", padx=5)

        self.y_label = tk.Label(self.zoom_coords_frame,
                                text="Y:", bg="#e0e0e0")
        self.y_label.pack(side="left", padx=5)

        self.y_entry = tk.Entry(self.zoom_coords_frame, width=5)
        self.y_entry.insert(0, "0")
        self.y_entry.pack(side="left", padx=5)

        self.zoom_factor_frame = Frame(self.zoom_frame, bg="#e0e0e0")
        self.zoom_factor_frame.pack(fill="x", pady=5)

        self.zoom_factor_label = tk.Label(
            self.zoom_factor_frame, text="Factor:", bg="#e0e0e0")
        self.zoom_factor_label.pack(side="left", padx=5)

        self.zoom_slider = Scale(self.zoom_factor_frame, from_=1, to=5, resolution=0.1,
                                 orient="horizontal", command=self.on_zoom)
        self.zoom_slider.set(1)
        self.zoom_slider.pack(side="right", padx=5, fill="x", expand=True)

        self.apply_zoom_btn = tk.Button(self.zoom_frame, text="Aplicar Zoom",
                                        command=self.apply_zoom, width=15)
        self.apply_zoom_btn.pack(pady=5)

    def setup_advanced_controls(self):
        """Configuración de controles avanzados"""
        # Binarización
        self.binary_frame = Frame(self.advanced_tab, bg="#e0e0e0")
        self.binary_frame.pack(fill="x", pady=5)

        self.binary_label = tk.Label(
            self.binary_frame, text="Umbral de binarización:", bg="#e0e0e0")
        self.binary_label.pack(side="left", padx=5)

        self.binary_slider = Scale(self.binary_frame, from_=0, to=255, resolution=1,
                                   orient="horizontal", command=self.on_binary_threshold)
        self.binary_slider.set(127)
        self.binary_slider.pack(side="right", padx=5, fill="x", expand=True)

        self.apply_binary_btn = tk.Button(self.advanced_tab, text="Binarizar",
                                          command=self.apply_binary, width=20)
        self.apply_binary_btn.pack(pady=5)

        # Histograma
        self.histogram_btn = tk.Button(self.advanced_tab, text="Mostrar Histograma",
                                       command=self.show_histogram, width=20)
        self.histogram_btn.pack(pady=5)

        # Fusión de imágenes
        self.fusion_frame = Frame(self.advanced_tab, bg="#e0e0e0")
        self.fusion_frame.pack(fill="x", pady=5)

        self.fusion_label = tk.Label(
            self.fusion_frame, text="Fusión de imágenes", bg="#e0e0e0")
        self.fusion_label.pack(side="top", anchor="w", padx=5)

        self.load_second_btn = tk.Button(self.fusion_frame, text="Cargar segunda imagen",
                                         command=self.load_second_image, width=20)
        self.load_second_btn.pack(pady=5)

        self.transparency_frame = Frame(self.fusion_frame, bg="#e0e0e0")
        self.transparency_frame.pack(fill="x", pady=5)

        self.transparency_label = tk.Label(
            self.transparency_frame, text="Transparencia:", bg="#e0e0e0")
        self.transparency_label.pack(side="left", padx=5)

        self.transparency_slider = Scale(self.transparency_frame, from_=0, to=1, resolution=0.01,
                                         orient="horizontal", command=self.on_transparency)
        self.transparency_slider.set(0.5)
        self.transparency_slider.pack(
            side="right", padx=5, fill="x", expand=True)

        self.apply_fusion_btn = tk.Button(self.fusion_frame, text="Aplicar Fusión",
                                          command=self.apply_fusion, width=15)
        self.apply_fusion_btn.pack(pady=5)

    # Métodos de manejo de archivos
    def open_image(self):
        """Abre un cuadro de diálogo para seleccionar una imagen"""
        file_path = filedialog.askopenfilename(
            defaultextension=".jpg",
            filetypes=[("Todos los archivos", "*.*"),
                       ("JPEG", "*.jpg"),
                       ("PNG", "*.png"),
                       ("BMP", "*.bmp")]
        )

        if file_path:
            self.current_image_path = file_path
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)
            self.load_image()

    def load_image(self):
        """Carga la imagen desde la ruta actual"""
        if not self.current_image_path:
            messagebox.showerror(
                "Error", "No se ha seleccionado ninguna imagen")
            return

        try:
            # Cargar la imagen con el procesador
            img = self.processor.load_image(self.current_image_path)
            # Guardar una copia del original
            self.original_image = np.copy(img)
            self.current_image = np.copy(img)   # Imagen actual para modificar

            # Mostrar la imagen
            self.show_image(self.current_image)

            # Resetear los controles
            self.reset_controls()

        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo cargar la imagen: {str(e)}")

    def load_second_image(self):
        """Carga una segunda imagen para fusión"""
        file_path = filedialog.askopenfilename(
            defaultextension=".jpg",
            filetypes=[("Todos los archivos", "*.*"),
                       ("JPEG", "*.jpg"),
                       ("PNG", "*.png"),
                       ("BMP", "*.bmp")]
        )

        if file_path:
            try:
                self.second_image_path = file_path
                self.second_image = self.processor.load_image(file_path)
                messagebox.showinfo(
                    "Éxito", "Segunda imagen cargada correctamente")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo cargar la segunda imagen: {str(e)}")

    def save_image(self):
        """Guarda la imagen actual"""
        if self.current_image is None:
            messagebox.showerror("Error", "No hay imagen para guardar")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"),
                       ("PNG", "*.png"),
                       ("BMP", "*.bmp")]
        )

        if file_path:
            try:
                # Convertir a uint8 si es necesario
                save_image = self.processor.to_uint8(self.current_image)

                # Guardar usando PIL
                Image.fromarray(save_image).save(file_path)
                messagebox.showinfo("Éxito", "Imagen guardada correctamente")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo guardar la imagen: {str(e)}")

    def update_image(self):
        """Aplica todos los ajustes actuales a la imagen original"""
        if self.original_image is None:
            messagebox.showerror("Error", "No hay imagen para actualizar")
            return

        # Aplicar todos los ajustes desde cero
        # Esto dependerá de cómo esté implementado tu procesador de imágenes
        # Por ahora, simplemente mostramos la imagen actual
        self.show_image(self.current_image)

    def restore_original(self):
        """Restaura la imagen original sin ajustes"""
        if self.original_image is None:
            messagebox.showerror(
                "Error", "No hay imagen original para restaurar")
            return

        self.current_image = np.copy(self.original_image)
        self.show_image(self.current_image)
        self.reset_controls()

    def reset_controls(self):
        """Resetea todos los controles a sus valores por defecto"""
        self.brightness_slider.set(0)
        self.contrast_slider.set(1)
        self.rotation_slider.set(0)
        self.zoom_slider.set(1)
        self.binary_slider.set(127)
        self.transparency_slider.set(0.5)
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, "0")
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, "0")

        # Resetear los checkboxes de canales
        self.r_var.set(1)
        self.g_var.set(1)
        self.b_var.set(1)
        self.c_var.set(1)
        self.m_var.set(1)
        self.y_var.set(1)

        # Resetear el filtro de zonas
        self.zone_var.set("normal")

    # Métodos de manipulación de imagen
    def on_adjust_brightness(self, value):
        """Ajusta el brillo de la imagen"""
        if self.current_image is None:
            return

        try:
            factor = float(value)
            adjusted_image = self.processor.adjust_brightness(
                self.current_image, factor)
            self.current_image = adjusted_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al ajustar el brillo: {str(e)}")

    def on_adjust_contrast(self, value):
        """Ajusta el contraste de la imagen"""
        if self.current_image is None:
            return

        try:
            factor = float(value)
            adjusted_image = self.processor.adjust_contrast(
                self.current_image, factor)
            self.current_image = adjusted_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al ajustar el contraste: {str(e)}")

    def on_rotate(self, value):
        """Rota la imagen según el ángulo especificado"""
        if self.current_image is None:
            return

        try:
            angle = float(value)
            rotated_image = self.processor.rotate_image(
                self.current_image, angle)
            self.current_image = rotated_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al rotar la imagen: {str(e)}")

    def on_zoom(self, value):
        """Previsualiza el factor de zoom (sin aplicarlo)"""
        # Este método solo actualiza la UI, el zoom real se aplica con apply_zoom
        pass

    def apply_zoom(self):
        """Aplica el zoom a la imagen según las coordenadas y factor"""
        if self.current_image is None:
            return

        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            factor = float(self.zoom_slider.get())

            zoomed_image = self.processor.apply_zoom(
                self.current_image, x, y, factor)
            self.current_image = zoomed_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar zoom: {str(e)}")

    def on_binary_threshold(self, value):
        """Previsualiza el umbral de binarización (sin aplicarlo)"""
        # Este método solo actualiza la UI, la binarización real se aplica con apply_binary
        pass

    def apply_binary(self):
        """Binariza la imagen según el umbral especificado"""
        if self.current_image is None:
            return

        try:
            threshold = int(self.binary_slider.get())
            binary_image = self.processor.binarize_image(
                self.current_image, threshold)
            self.current_image = binary_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al binarizar la imagen: {str(e)}")

    def update_channels(self):
        """Actualiza los canales de color visibles"""
        if self.current_image is None:
            return

        try:
            # Obtener los valores de los checkboxes
            r_active = self.r_var.get()
            g_active = self.g_var.get()
            b_active = self.b_var.get()
            c_active = self.c_var.get()
            m_active = self.m_var.get()
            y_active = self.y_var.get()

            # Aplicar el filtro de canales RGB
            channels_image = self.processor.filter_channels(
                self.original_image,
                r_active, g_active, b_active,
                c_active, m_active, y_active
            )

            self.current_image = channels_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al actualizar canales: {str(e)}")

    def apply_zone_filter(self):
        """Aplica filtro de zonas claras u oscuras"""
        if self.current_image is None:
            return

        try:
            zone_type = self.zone_var.get()

            if zone_type == "normal":
                # Restaurar la imagen original con los filtros aplicados
                self.update_channels()
            else:
                # Aplicar filtro de zonas
                filtered_image = self.processor.apply_zone_filter(
                    self.current_image, zone_type)
                self.current_image = filtered_image
                self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al aplicar filtro de zonas: {str(e)}")

    def apply_negative(self):
        """Aplica el negativo a la imagen"""
        if self.current_image is None:
            return

        try:
            negative_image = self.processor.apply_negative(self.current_image)
            self.current_image = negative_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al aplicar negativo: {str(e)}")

    def on_transparency(self, value):
        """Previsualiza la transparencia (sin aplicarla)"""
        # Este método solo actualiza la UI, la fusión real se aplica con apply_fusion
        pass

    def apply_fusion(self):
        """Fusiona la imagen actual con la segunda imagen"""
        if self.current_image is None or self.second_image is None:
            messagebox.showerror("Error", "Faltan imágenes para la fusión")
            return

        try:
            transparency = float(self.transparency_slider.get())
            fused_image = self.processor.fuse_images(
                self.current_image, self.second_image, transparency)
            self.current_image = fused_image
            self.show_image(self.current_image)
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al fusionar imágenes: {str(e)}")

    def show_histogram(self):
        """Muestra el histograma de la imagen actual"""
        if self.current_image is None:
            messagebox.showerror(
                "Error", "No hay imagen para mostrar el histograma")
            return

        try:
            # Crear una nueva ventana para el histograma
            histogram_window = tk.Toplevel(self.root)
            histogram_window.title("Histograma")
            histogram_window.geometry("600x500")

            # Crear figura para el histograma
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))

            # Histograma RGB
            if len(self.current_image.shape) == 3:  # Imagen a color
                # Histograma para cada canal
                colors = ('r', 'g', 'b')
                for i, color in enumerate(colors):
                    histogram = self.processor.calculate_histogram(
                        self.current_image[:, :, i])
                    ax1.plot(histogram, color=color)

                ax1.set_title('Histograma RGB')
                ax1.set_xlabel('Intensidad de pixel')
                ax1.set_ylabel('Frecuencia')

                # Histograma de luminosidad
                gray_image = self.processor.to_grayscale(self.current_image)
                histogram = self.processor.calculate_histogram(gray_image)
                ax2.plot(histogram, color='black')
                ax2.set_title('Histograma de Luminosidad')
                ax2.set_xlabel('Intensidad de pixel')
                ax2.set_ylabel('Frecuencia')
            else:  # Imagen en escala de grises
                histogram = self.processor.calculate_histogram(
                    self.current_image)
                ax1.plot(histogram, color='black')
                ax1.set_title('Histograma de Escala de Grises')
                ax1.set_xlabel('Intensidad de pixel')
                ax1.set_ylabel('Frecuencia')

                # Ocultar el segundo eje
                ax2.axis('off')

            # Ajustar espaciado
            plt.tight_layout()

            # Incorporar el gráfico a la ventana de Tkinter
            canvas = FigureCanvasTkAgg(fig, master=histogram_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al mostrar histograma: {str(e)}")

    def show_image(self, img_data):
        """Convierte la imagen NumPy a un formato compatible con Tkinter y la muestra"""
        if img_data is None:
            return

        try:
            # Convertir a uint8 si es necesario
            if img_data.dtype != np.uint8:
                img_data = self.processor.to_uint8(img_data)

            # Ajustar el tamaño para visualización si es muy grande
            h, w = img_data.shape[:2]
            max_display_size = 800  # Tamaño máximo para visualización

            if h > max_display_size or w > max_display_size:
                # Calcular la relación de aspecto
                aspect_ratio = w / h

                if h > w:
                    new_h = max_display_size
                    new_w = int(max_display_size * aspect_ratio)
                else:
                    new_w = max_display_size
                    new_h = int(max_display_size / aspect_ratio)

                # Redimensionar para visualización
                display_img = self.processor.resize_image(
                    img_data, new_w, new_h)
            else:
                display_img = img_data

            # Convertir NumPy a PIL
            image_pil = Image.fromarray(display_img)

            # Convertir PIL a Tkinter
            self.tk_image = ImageTk.PhotoImage(image_pil)

            # Actualizar el Label con la nueva imagen
            self.image_label.configure(image=self.tk_image)

            # Evitar que la imagen sea eliminada por el recolector de basura
            self.image_label.image = self.tk_image

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al mostrar la imagen: {str(e)}")

# La clase ImageProcessor debe ser implementada con todas las funciones necesarias
# A continuación se muestra una implementación básica:


class ImageProcessor:
    def __init__(self):
        pass

    def load_image(self, image_path):
        """Carga una imagen desde un archivo"""
        try:
            img = np.array(Image.open(image_path))
            return img
        except Exception as e:
            raise Exception(f"Error al cargar la imagen: {str(e)}")

    def to_uint8(self, image):
        """Convierte la imagen a formato uint8"""
        if image.dtype != np.uint8:
            # Normalizar y convertir a uint8
            if image.max() > 1.0:
                # Ya está en rango 0-255
                return np.clip(image, 0, 255).astype(np.uint8)
            else:
                # Está en rango 0-1
                return (image * 255).clip(0, 255).astype(np.uint8)
        return image

    def adjust_brightness(self, image, factor):
        """Ajusta el brillo de la imagen"""
        # Implementación básica, ajustar según tu biblioteca
        adjusted = image + (factor * 255)
        return np.clip(adjusted, 0, 255).astype(image.dtype)

    def adjust_contrast(self, image, factor):
        """Ajusta el contraste de la imagen"""
        # Implementación básica, ajustar según tu biblioteca
        mean = np.mean(image)
        adjusted = (image - mean) * factor + mean
        return np.clip(adjusted, 0, 255).astype(image.dtype)

    def rotate_image(self, image, angle):
        """Rota la imagen según el ángulo especificado"""
        # Usar PIL para rotación
        pil_img = Image.fromarray(self.to_uint8(image))
        rotated = pil_img.rotate(angle, resample=Image.BICUBIC, expand=True)
        return np.array(rotated)

    def apply_zoom(self, image, x, y, factor):
        """Aplica zoom a la imagen desde el punto (x,y) con el factor especificado"""
        # Implementación básica, ajustar según tu biblioteca
        h, w = image.shape[:2]

        # Asegurar que x e y estén dentro de la imagen
        x = max(0, min(x, w-1))
        y = max(0, min(y, h-1))

        # Calcular el tamaño de la región a recortar
        new_w = int(w / factor)
        new_h = int(h / factor)

        # Calcular las coordenadas de recorte
        x1 = max(0, x - new_w // 2)
        y1 = max(0, y - new_h // 2)
        x2 = min(w, x1 + new_w)
        y2 = min(h, y1 + new_h)

        # Recortar y redimensionar
        cropped = image[y1:y2, x1:x2]
        return self.resize_image(cropped, w, h)

    def resize_image(self, image, width, height):
        """Redimensiona la imagen al tamaño especificado"""
        pil_img = Image.fromarray(self.to_uint8(image))
        resized = pil_img.resize((width, height), Image.BICUBIC)
        return np.array(resized)

    def binarize_image(self, image, threshold):
        """Binariza la imagen según el umbral especificado"""
        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = self.to_grayscale(image)
        else:
            gray = image

        # Aplicar umbral
        binary = np.zeros_like(gray)
        binary[gray > threshold] = 255

        return binary

    def to_grayscale(self, image):
        """Convierte la imagen a escala de grises"""
        if len(image.shape) == 2:
            return image  # Ya está en escala de grises

        # Usar ponderación estándar para luminosidad
        return np.dot(image[..., :3], [0.299, 0.587, 0.114])

    def filter_channels(self, image, r_active, g_active, b_active, c_active, m_active, y_active):
        """Filtra los canales de color de la imagen"""
        if len(image.shape) != 3:
            return image  # No es una imagen a color

        # Crear una copia para no modificar la original
        result = np.copy(image)

        # Aplicar filtros RGB
        if not r_active:
            result[:, :, 0] = 0
        if not g_active:
            result[:, :, 1] = 0
        if not b_active:
            result[:, :, 2] = 0

        # Aplicar filtros CMY
        if not c_active:
            result[:, :, 0] = 255  # Rojo al máximo (ausencia de cian)
        if not m_active:
            result[:, :, 1] = 255  # Verde al máximo (ausencia de magenta)
        if not y_active:
            result[:, :, 2] = 255  # Azul al máximo (ausencia de amarillo)

        return result

    def apply_zone_filter(self, image, zone_type):
        """Aplica filtro para resaltar zonas claras u oscuras"""
        if zone_type == "light":
            # Resaltar zonas claras
            threshold = 128
            mask = image > threshold
            result = np.copy(image)
            result[~mask] = 0  # Oscurecer zonas oscuras
            return result
        elif zone_type == "dark":
            # Resaltar zonas oscuras
            threshold = 128
            mask = image < threshold
            result = np.copy(image)
            result[~mask] = 255  # Aclarar zonas claras
            return result
        else:
            return image  # Normal

    def apply_negative(self, image):
        """Aplica el negativo a la imagen"""
        return 255 - image

    def fuse_images(self, image1, image2, alpha):
        """Fusiona dos imágenes con un factor de transparencia"""
        # Asegurar que las imágenes tengan el mismo tamaño
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]

        if h1 != h2 or w1 != w2:
            image2 = self.resize_image(image2, w1, h1)

        # Asegurar que ambas sean RGB
        if len(image1.shape) == 2:
            image1 = np.stack([image1, image1, image1], axis=2)
        if len(image2.shape) == 2:
            image2 = np.stack([image2, image2, image2], axis=2)

        # Aplicar fusión
        result = image1 * alpha + image2 * (1 - alpha)
        return np.clip(result, 0, 255).astype(image1.dtype)

    def calculate_histogram(self, image):
        """Calcula el histograma de la imagen"""
        # Asegurar que es uint8
        img = self.to_uint8(image)

        # Calcular histograma
        histogram = np.zeros(256)
        for pixel_value in img.flatten():
            histogram[pixel_value] += 1

        return histogram

# Función principal para ejecutar la aplicación


def main():
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
