import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate, zoom


class ImageProcessor:
    def __init__(self, logo_path=None, img1_path=None, img2_path=None):
        """
        Inicializa el procesador de imágenes con las imágenes proporcionadas.

        Parámetros:
        - logo_path: Ruta a la imagen principal
        - img1_path: Ruta a la primera imagen adicional
        - img2_path: Ruta a la segunda imagen adicional (opcional)
        """
        # Cargar imágenes solo si se proporciona la ruta
        if logo_path:
            self.logo = self._load_image(logo_path)
        else:
            self.logo = None

        if img1_path:
            self.img1 = self._load_image(img1_path)
        else:
            self.img1 = None

        if img2_path:
            self.img2 = self._load_image(img2_path)
        else:
            self.img2 = None

    def _load_image(self, path):
        """
        Carga una imagen desde la ruta proporcionada y la normaliza si es necesario.
        """
        img = np.array(plt.imread(path))
        if img.dtype == np.uint8:
            img = img / 255.0
        return img

    def set_image(self, image, image_type='logo'):
        """
        Establece una imagen directamente en lugar de cargarla desde un archivo.

        Parámetros:
        - image: Array NumPy que representa la imagen
        - image_type: 'logo', 'img1' o 'img2'
        """
        if image.dtype == np.uint8:
            image = image / 255.0

        if image_type == 'logo':
            self.logo = image
        elif image_type == 'img1':
            self.img1 = image
        elif image_type == 'img2':
            self.img2 = image
        else:
            raise ValueError("El tipo de imagen debe ser 'logo', 'img1' o 'img2'")

    def show_image(self, matrix, title=None):
        """
        Muestra la imagen en un gráfico de Matplotlib.

        Parámetros:
        - matrix: Matriz NumPy representando la imagen a mostrar
        - title: Título opcional para la imagen
        """
        plt.figure(figsize=(8, 6))
        plt.imshow(matrix, cmap="gray" if len(matrix.shape) == 2 else None)
        if title:
            plt.title(title)
        plt.axis("off")
        plt.show()

    # ---- Métodos del archivo t8.py ----

    def invert_colors(self, image=None):
        """
        Invierte los colores de la imagen.

        Parámetros:
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con colores invertidos
        """
        img = self.logo if image is None else image
        return 1 - img

    def extract_channel(self, channel, image=None):
        """
        Extrae un canal específico de la imagen.

        Parámetros:
        - channel: Canal a extraer ('red', 'green', 'blue')
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con solo el canal especificado
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)

        if channel == 'red':
            image_copy[:, :, 1] = 0  # Eliminar verde
            image_copy[:, :, 2] = 0  # Eliminar azul
        elif channel == 'green':
            image_copy[:, :, 0] = 0  # Eliminar rojo
            image_copy[:, :, 2] = 0  # Eliminar azul
        elif channel == 'blue':
            image_copy[:, :, 0] = 0  # Eliminar rojo
            image_copy[:, :, 1] = 0  # Eliminar verde
        else:
            raise ValueError("Canal inválido. Usa 'red', 'green' o 'blue'")

        return image_copy

    def red_layer(self, image=None):
        """
        Extrae la capa roja de la imagen.
        """
        return self.extract_channel('red', image)

    def green_layer(self, image=None):
        """
        Extrae la capa verde de la imagen.
        """
        return self.extract_channel('green', image)

    def blue_layer(self, image=None):
        """
        Extrae la capa azul de la imagen.
        """
        return self.extract_channel('blue', image)

    def extract_composite_channel(self, channel, image=None):
        """
        Extrae un canal compuesto específico (magenta, cyan, amarillo).

        Parámetros:
        - channel: Canal a extraer ('magenta', 'cyan', 'yellow')
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con solo el canal compuesto especificado
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)
        row, col = image_copy.shape[0], image_copy.shape[1]

        if channel == 'magenta':
            image_copy[:, :, 0] = np.ones((row, col))  # Rojo a máximo
            image_copy[:, :, 1] = 0  # Verde a 0
            image_copy[:, :, 2] = np.ones((row, col))  # Azul a máximo
        elif channel == 'cyan':
            image_copy[:, :, 0] = 0  # Rojo a 0
            image_copy[:, :, 1] = np.ones((row, col))  # Verde a máximo
            image_copy[:, :, 2] = np.ones((row, col))  # Azul a máximo
        elif channel == 'yellow':
            image_copy[:, :, 0] = np.ones((row, col))  # Rojo a máximo
            image_copy[:, :, 1] = np.ones((row, col))  # Verde a máximo
            image_copy[:, :, 2] = 0  # Azul a 0
        else:
            raise ValueError("Canal inválido. Usa 'magenta', 'cyan' o 'yellow'")

        return image_copy

    def magenta_layer(self, image=None):
        """
        Extrae la capa magenta de la imagen (rojo y azul a máximo, verde a 0).
        """
        return self.extract_composite_channel('magenta', image)

    def cyan_layer(self, image=None):
        """
        Extrae la capa cyan de la imagen (verde y azul a máximo, rojo a 0).
        """
        return self.extract_composite_channel('cyan', image)

    def yellow_layer(self, image=None):
        """
        Extrae la capa amarilla de la imagen (rojo y verde a máximo, azul a 0).
        """
        return self.extract_composite_channel('yellow', image)

    def combine_layers(self, red_img, green_img, blue_img):
        """
        Combina las tres capas de la imagen (rojo, verde y azul)
        en una imagen final.

        Parámetros:
        - red_img: Imagen con la capa roja
        - green_img: Imagen con la capa verde
        - blue_img: Imagen con la capa azul

        Retorna:
        - Imagen combinada
        """
        return np.stack(
            (red_img[:, :, 0], green_img[:, :, 1], blue_img[:, :, 2]), axis=-1
        )

    def fusion_images(self, img1=None, img2=None):
        """
        Fusiona dos imágenes mediante suma directa.

        Parámetros:
        - img1: Primera imagen opcional para procesar en lugar de self.img1
        - img2: Segunda imagen opcional para procesar en lugar de self.img2

        Retorna:
        - Imagen fusionada
        """
        image1 = self.img1 if img1 is None else img1
        image2 = self.img2 if img2 is None else img2

        return image1 + image2

    def fusion_images_weighted(self, alpha=0.5, img1=None, img2=None):
        """
        Fusiona dos imágenes con ponderación.

        Parámetros:
        - alpha: Factor de ponderación para la primera imagen (0-1)
        - img1: Primera imagen opcional para procesar en lugar de self.img1
        - img2: Segunda imagen opcional para procesar en lugar de self.img2

        Retorna:
        - Imagen fusionada
        """
        image1 = self.img1 if img1 is None else img1
        image2 = self.img2 if img2 is None else img2

        return (image1 * alpha) + (image2 * (1 - alpha))

    def brightness(self, factor, image=None):
        """
        Ajusta el brillo de la imagen.

        Parámetros:
        - factor: Factor de brillo (positivo aumenta, negativo disminuye)
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con brillo ajustado
        """
        img = self.logo if image is None else image
        factor = float(factor)

        # Limitar el resultado entre 0 y 1 para evitar desbordamiento
        return np.clip(img + factor, 0, 1)

    def convert_to_grayscale(self, method='average', image=None):
        """
        Convierte la imagen a escala de grises usando diferentes métodos.

        Parámetros:
        - method: Método a utilizar ('average', 'luminosity', 'midgray')
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen en escala de grises
        """
        img = self.logo if image is None else image

        if method == 'average':
            return np.mean(img, axis=2)
        elif method == 'luminosity':
            return 0.21 * img[:, :, 0] + 0.72 * img[:, :, 1] + 0.07 * img[:, :, 2]
        elif method == 'midgray':
            return (np.max(img, axis=2) + np.min(img, axis=2)) / 2
        else:
            raise ValueError("Método inválido. Usa 'average', 'luminosity' o 'midgray'")

    def grayscale_average(self, image=None):
        """
        Aplica escala de grises usando el método de promedio.
        """
        return self.convert_to_grayscale('average', image)

    def grayscale_luminosity(self, image=None):
        """
        Aplica escala de grises usando el método de luminosidad.
        """
        return self.convert_to_grayscale('luminosity', image)

    def grayscale_midgray(self, image=None):
        """
        Aplica escala de grises usando el método de gris medio.
        """
        return self.convert_to_grayscale('midgray', image)

    # ---- Métodos del archivo t9.py ----

    def adjust_channel_brightness(self, channel, factor, image=None):
        """
        Ajusta el brillo de un canal específico de la imagen.

        Parámetros:
        - channel: 'r', 'g' o 'b' para seleccionar el canal rojo, verde o azul
        - factor: Número que indica cuánto aumentar o disminuir el brillo del canal
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con el brillo ajustado en el canal especificado
        """
        img = self.logo if image is None else image
        factor = float(factor)
        image_copy = np.copy(img)

        # Determinar el índice del canal según una letra
        channel_map = {
            'r': 0,
            'g': 1,
            'b': 2
        }

        if channel.lower() not in channel_map:
            raise ValueError("Canal inválido. Usa 'r', 'g' o 'b'")

        ch_idx = channel_map[channel.lower()]

        # Crear una copia de la imagen original
        adjusted_image = np.copy(image_copy)

        # Ajustar solo el canal específico
        adjusted_image[:, :, ch_idx] = np.clip(image_copy[:, :, ch_idx] + factor, 0, 1)

        return adjusted_image

    def adjust_contrast(self, factor, image=None):
        """
        Ajusta el contraste de la imagen de acuerdo con el factor dado.

        Parámetros:
        - factor: Número que indica cuánto aumentar o disminuir el contraste
                 (1 mantiene igual, >1 aumenta, <1 reduce)
        - image: Imagen opcional para procesar en lugar de self.img1

        Retorna:
        - Imagen con el contraste ajustado
        """
        img = self.img1 if image is None else image
        factor = float(factor)
        image_copy = np.copy(img)

        # Aplicar ajuste de contraste
        image_dark_areas = factor * np.log10(1 + image_copy)
        image_clear_areas = factor * np.exp(image_copy - 1)
        contrasted_image = np.clip(image_dark_areas + image_clear_areas, 0, 1)

        return contrasted_image

    def zoom_image(self, zoom_factor, center=None, image=None):
        """
        Aplica un zoom en la imagen.

        Parámetros:
        - zoom_factor: Factor de zoom (1 = sin cambios, >1 = zoom in, <1 = zoom out)
        - center: Tupla (y, x) con las coordenadas del centro del zoom, None para centro de la imagen
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen con zoom aplicado
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)

        # Si la imagen tiene 3 canales, aplicar zoom a cada canal
        if len(image_copy.shape) == 3:
            zoomed_image = np.zeros_like(image_copy)
            for i in range(image_copy.shape[2]):
                zoomed_image[:, :, i] = zoom(image_copy[:, :, i], zoom_factor, order=1)
        else:
            zoomed_image = zoom(image_copy, zoom_factor, order=1)

        return zoomed_image

    def binarize_image(self, threshold=0.5, image=None):
        """
        Binariza la imagen usando un umbral.

        Parámetros:
        - threshold: Umbral de binarización (0-1)
        - image: Imagen opcional para procesar en lugar de self.logo

        Retorna:
        - Imagen binarizada
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)

        # Convertir a escala de grises si es una imagen a color
        if len(image_copy.shape) == 3:
            grayscale = np.mean(image_copy, axis=-1)
        else:
            grayscale = image_copy

        # Binarizar
        img_bin = (grayscale > threshold)

        return img_bin

    def rotate_image(self, angle, image=None, reshape=True):
        """
        Rota la imagen por un ángulo dado.

        Parámetros:
        - angle: Ángulo en grados (positivo = antihorario, negativo = horario)
        - image: Imagen opcional para procesar en lugar de self.logo
        - reshape: Si es True, redimensiona la imagen para contener la imagen rotada completa

        Retorna:
        - Imagen rotada
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)

        # Rotar imagen
        rotated = rotate(image_copy, angle, reshape=reshape)

        return rotated

    def plot_histogram(self, image=None):
        """
        Genera y muestra los histogramas de las capas roja, verde y azul de la imagen.

        Parámetros:
        - image: Imagen opcional para procesar en lugar de self.logo
        """
        img = self.logo if image is None else image
        image_copy = np.copy(img)

        # Verificar si la imagen es a color
        if len(image_copy.shape) != 3 or image_copy.shape[2] < 3:
            plt.figure(figsize=(8, 6))
            plt.hist(image_copy.flatten(), bins=256, color="gray", alpha=0.7)
            plt.title("Histograma - Escala de Grises")
            plt.xlabel("Valor de Intensidad")
            plt.ylabel("Frecuencia")
            plt.show()
            return

        # Separar los canales de color
        red_channel = image_copy[:, :, 0].flatten()
        green_channel = image_copy[:, :, 1].flatten()
        blue_channel = image_copy[:, :, 2].flatten()

        # Crear una figura con 3 subgráficos
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

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
