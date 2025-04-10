from numpy._core.numerictypes import uint8
from scipy.ndimage import zoom
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from scipy.ndimage import rotate


class ImageProcessor:
    def __init__(self, logo_path, img1_path):
        self.logo = np.array(plt.imread(logo_path))
        self.img1 = np.array(plt.imread(img1_path))

        if self.logo.dtype == np.uint8:
            self.logo = self.logo / 255.0

        if self.img1.dtype == np.uint8:
            self.img1 = self.img1 / 255.0

    def show_image(self, matrix):
        plt.imshow(matrix, cmap="gray")
        plt.axis("off")
        plt.show()

    def brightness(self, factor):
        print("\nAplicando factor de brillo a la imagen")
        factor = float(factor)
        return self.logo + factor

    def adjust_channel_brightness(self, channel, factor):
        """
        Ajusta el brillo de un canal específico de la imagen.

        Parámetros:
        - channel: 'r', 'g' o 'b' para seleccionar el canal rojo, verde o azul.
        - factor: número que indica cuánto aumentar o disminuir el brillo del canal.

        Retorna:
        - Imagen con el brillo ajustado en el canal especificado.
        """
        factor = float(factor)
        image_copy = np.copy(self.logo)

        # Determinar el índice del canal segun una letra
        channel_map = {
            'r': 0,
            'g': 1,
            'b': 2
        }

        if channel.lower() not in channel_map:
            print("Canal inválido. Usa 'r', 'g' o 'b'.")
            return self.logo

        ch_idx = channel_map[channel.lower()]
        adjusted_image = np.zeros_like(image_copy)
        adjusted_image[:, :, ch_idx] = image_copy[:, :, ch_idx] + factor
        return adjusted_image

    def adjust_contrast(self, factor):
        """
        Ajusta el contraste de la imagen de acuerdo con el factor dado.

        Parámetros:
        - factor: número que indica cuánto aumentar o disminuir el contraste (1 mantiene igual, >1 aumenta, <1 reduce).

        Retorna:
        - Imagen con el contraste ajustado.
        """
        factor = float(factor)
        image_copy = np.copy(self.img1)

        image_dark_areas = factor * np.log10(1 + image_copy)
        image_clear_areas = factor * np.exp(image_copy - 1)
        contrasted_image = image_dark_areas + image_clear_areas
        return contrasted_image

    def zoom_image(self, zoom_percentage):
        """
        Aplica un zoom en el centro de la imagen según un porcentaje.

        Parámetro:
        - zoom_percentage: Porcentaje de zoom (ejemplo: 200 = 200%).

        Retorna:
        - Imagen con zoom aplicado.
        """
        image_copy = np.copy(self.logo) / 255

        h, w = image_copy.shape[:2]
        zoom_area = 100
        start_row = h // 2 - zoom_area // 2
        end_row = h // 2 + zoom_area // 2
        start_col = w // 2 - zoom_area // 2
        end_col = w // 2 - zoom_area // 2

        cut = image_copy[start_row:end_row, start_col:end_col]
        zoomed = np.kron(cut, np.ones((zoom_percentage, zoom_percentage, 1)))

        return zoomed

    def binarize_image(self):
        """
        Binariza la imagen automáticamente con un umbral de 128.

        Retorna:
        - Imagen binarizada en blanco y negro.
        """
        image_copy = np.copy(self.logo)

        # Convertir a escala de grises
        grayscale = np.mean(image_copy, axis=-1)
        umbral = 0.5
        img_bin = (grayscale > umbral)

        return img_bin

    def rotate_image(self, angle):
        """
        Rota la imagen por un ángulo dado.

        Parámetro:
        - angle: Ángulo en grados (positivo = antihorario, negativo = horario).

        Retorna:
        - Imagen rotada.
        """
        image_copy = np.copy(self.logo)

        # Rotar imagen
        rotated = rotate(image_copy, angle, reshape=True)

        return rotated

    def plot_histogram(self):
        """
        Genera y muestra los histogramas de las capas roja, verde y azul de la imagen.
        """
        image_copy = np.copy(self.logo)

        # Separar los canales de color
        red_channel = image_copy[:, :, 0].flatten()
        green_channel = image_copy[:, :, 1].flatten()
        blue_channel = image_copy[:, :, 2].flatten()

        # Crear una figura con 3 subgráficos (filas)
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))  # 3 filas, 1 columna

        # Histograma de la capa roja
        axes[0].hist(red_channel, bins=256, color="red", alpha=0.7)
        axes[0].set_title("Histograma - Canal Rojo")
        axes[0].set_xlabel("Valor de Intensidad")
        axes[0].set_ylabel("Frecuencia")

        # Histograma de la capa verde
        axes[1].hist(green_channel, bins=256, color="green", alpha=0.7)
        axes[1].set_title("Histograma - Canal Verde")
        axes[1].set_xlabel("Valor de Intensidad")
        axes[1].set_ylabel("Frecuencia")

        # Histograma de la capa azul
        axes[2].hist(blue_channel, bins=256, color="blue", alpha=0.7)
        axes[2].set_title("Histograma - Canal Azul")
        axes[2].set_xlabel("Valor de Intensidad")
        axes[2].set_ylabel("Frecuencia")

        # Ajustar espaciado entre subgráficos y mostrar
        plt.tight_layout()
        plt.show()


class Menu:
    def __init__(self, image_processor):
        self.image_processor = image_processor
        self.options = {
            0: self.show_original,
            1: self.brightness,
            2: self.adjust_channel_brightness,
            3: self.adjust_contrast,
            4: self.zoom_image,
            5: self.binarize_image,
            6: self.rotate_image,
            7: self.show_histogram,
            8: self.exit_menu,
        }

    def show_original(self):
        """
        Muestra la imagen original.
        """
        self.image_processor.show_image(self.image_processor.logo)

    def brightness(self):
        factor = input("Ingrese el factor: ")
        factored = self.image_processor.brightness(factor)
        self.image_processor.show_image(factored)

    def adjust_channel_brightness(self):
        """
        Solicita un canal y un factor al usuario, y ajusta el brillo de ese canal en la imagen.
        """
        try:
            channel = input(
                "Ingrese el canal a modificar ('r' para rojo, 'g' para verde, 'b' para azul): ").strip().lower()
            factor = float(input(
                "Ingrese el factor de brillo (ej. 0.5 para oscurecer, 1.5 para iluminar): "))

            bright_image = self.image_processor.adjust_channel_brightness(
                channel, factor)
            self.image_processor.show_image(bright_image)
        except ValueError:
            print("Por favor, ingrese valores válidos.")

    def adjust_contrast(self):
        """
        Solicita un factor de contraste al usuario y ajusta el contraste de la imagen.
        """
        try:
            factor = float(input(
                "Ingrese el factor de contraste (ej. 0.5 para reducir, 1.5 para aumentar): "))
            contrasted_image = self.image_processor.adjust_contrast(factor)
            self.image_processor.show_image(contrasted_image)
        except ValueError:
            print("Por favor, ingrese un número válido.")

    def zoom_image(self):
        zoom_percentage = int(input(
            "Ingrese el porcentaje de zoom (ej. 200 para 200%): "))
        zoomed = self.image_processor.zoom_image(zoom_percentage)
        self.image_processor.show_image(zoomed)

    def binarize_image(self):
        binary = self.image_processor.binarize_image()
        self.image_processor.show_image(binary)

    def rotate_image(self):
        angle = float(input(
            "Ingrese el ángulo de rotación (positivo = antihorario, negativo = horario): "))
        rotated = self.image_processor.rotate_image(angle)
        self.image_processor.show_image(rotated)

    def show_histogram(self):
        self.image_processor.plot_histogram()

    def exit_menu(self):
        """
        Sale del menú.
        """
        print("Saliendo del menú...")
        exit()

    def display_menu(self):
        """
        Muestra el menú con opciones y espera la selección del usuario.
        """
        while True:
            print("\n--- Menú de Opciones ---")
            print("0. show original")
            print("1. Brillo de una imagen")
            print("2. Aplicar brillo a un canal de la imagen")
            print("3. Ajustar contraste de la imagen")
            print("4. Hacer zoom a la imagen")
            print("5. BInarizar la imagen")
            print("6. Rotar la imagen")
            print("7. Mostrar histograma de los canales")
            print("8. salir")

            try:
                option = int(input("\nSelecciona una opción (1-8): "))

                if option in self.options:
                    self.options[option]()  # Ejecuta la opción seleccionada
                else:
                    print(
                        "Opción no válida. Por favor, selecciona una opción entre 1 y 9.")
            except ValueError:
                print("Por favor ingresa un número válido.")


if __name__ == "__main__":
    # Crear el procesador de imágenes y el menú
    logo_path = "utplogo.jpg"
    img1_path = "beach.jpg"
    image_processor = ImageProcessor(logo_path, img1_path)
    menu = Menu(image_processor)

    # Ejecutar el menú
    menu.display_menu()
