import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import exposure


class ImageProcessor:
    def __init__(self, logo_path, img1_path, img2_path):
        """
        Inicializa el procesador de imágenes con una imagen dada.
        """
        self.logo = np.array(plt.imread(logo_path))
        self.img1 = np.array(plt.imread(img1_path))
        self.img2 = np.array(plt.imread(img2_path))

        if self.logo.dtype == np.uint8:
            self.logo = self.logo / 255.0

        if self.img1.dtype == np.uint8:
            self.img1 = self.img1 / 255.0

        if self.img2.dtype == np.uint8:
            self.img2 = self.img2 / 255.0

    def show_image(self, matrix):
        """
        Muestra la imagen en un gráfico de Matplotlib.
        """
        plt.imshow(matrix, cmap="gray")
        plt.axis("off")
        plt.show()

    def invert_colors(self):
        """
        Invierte los colores de la imagen.
        """
        print("\nInvertiendo los colores de la imagen")
        return 1 - self.logo

    def red_layer(self):
        """
        Extrae la capa roja de la imagen.
        """
        print("\nExtrayendo la capa roja de la imagen")
        image_copy = np.copy(self.logo)
        image_copy[:, :, 1] = 0  # Eliminar verde
        image_copy[:, :, 2] = 0  # Eliminar azul
        return image_copy

    def green_layer(self):
        """
        Extrae la capa verde de la imagen.
        """
        print("\nExtrayendo la capa verde de la imagen")
        image_copy = np.copy(self.logo)
        image_copy[:, :, 0] = 0  # Eliminar rojo
        image_copy[:, :, 2] = 0  # Eliminar azul
        return image_copy

    def blue_layer(self):
        """
        Extrae la capa azul de la imagen.
        """
        print("\nExtrayendo la capa azul de la imagen")
        image_copy = np.copy(self.logo)
        image_copy[:, :, 0] = 0  # Eliminar rojo
        image_copy[:, :, 1] = 0  # Eliminar verde
        return image_copy

    def magenta_layer(self):
        """
        Extrae la capa magenta de la imagen (rojo y azul a máximo, verde a 0).
        """
        print("\nExtrayendo la capa magenta de la imagen")
        image_copy = np.copy(self.logo)
        row = image_copy.shape[0]
        col = image_copy.shape[1]
        image_copy[:, :, 0] = np.ones((row, col)) * 255
        image_copy[:, :, 2] = np.ones((row, col)) * 255
        return image_copy

    def cyan_layer(self):
        """
        Extrae la capa cyan de la imagen (verde y azul a máximo, rojo a 0).
        """
        print("\nExtrayendo la capa cyan de la imagen")
        image_copy = np.copy(self.logo)
        row = image_copy.shape[0]
        col = image_copy.shape[1]
        image_copy[:, :, 1] = np.ones((row, col)) * 255
        image_copy[:, :, 2] = np.ones((row, col)) * 255
        return image_copy

    def yellow_layer(self):
        """
        Extrae la capa amarilla de la imagen (rojo y verde a máximo, azul a 0).
        """
        print("\nExtrayendo la capa amarilla de la imagen")
        image_copy = np.copy(self.logo)
        row = image_copy.shape[0]
        col = image_copy.shape[1]
        image_copy[:, :, 0] = np.ones((row, col)) * 255
        image_copy[:, :, 1] = np.ones((row, col)) * 255
        return image_copy

    def combine_layers(self, red_img, green_img, blue_img):
        """
        Combina las tres capas de la imagen (rojo, verde y azul)
        en una imagen final.
        """
        print("\nCombinando capas de la imagen")
        return np.stack(
            (red_img[:, :, 0], green_img[:, :, 1], blue_img[:, :, 2]), axis=-1
        )

    def fusion_images(self):
        print("\nFusionando imagenes")
        return self.img1 + self.img2

    def fusion_images_eq(self):
        print("\nFusionando imagenes con equalizacion")
        alpha = 0.5
        return (self.img1 * alpha) + (self.img2 * (1 - alpha))

    def factor_image(self, factor):
        print("\nAplicando factor a la imagen")
        # self.logo / 255.0
        factor = float(factor)
        factores_image = self.logo + factor
        return factores_image

    def grayscale_average(self):
        print("\nAplicando escala de grises (Avarage)")
        return np.mean(self.logo, axis=2)

    def grayscale_luminosity(self):
        print("\nAplicando escala de grises (Luminosity)")
        return 0.21 * self.logo[:, :, 0] + 0.72 * self.logo[:, :, 1] + 0.07 * self.logo[:, :, 2]

    def grayscale_midgray(self):
        print("\nAplicando escala de grises (Midgray)")
        return (np.max(self.logo, axis=2) + np.min(self.logo, axis=2)) / 2


class Menu:
    def __init__(self, image_processor):
        """
        Inicializa el menú con un procesador de imágenes.
        """
        self.image_processor = image_processor
        self.options = {
            1: self.invert_colors,
            2: self.show_red_layer,
            3: self.show_green_layer,
            4: self.show_blue_layer,
            5: self.show_magenta_layer,
            6: self.show_cyan_layer,
            7: self.show_yellow_layer,
            8: self.combine_layers,
            9: self.fusion_images,
            10: self.fusion_images_eq,
            11: self.factor_image,
            12: self.grayscale_average,
            13: self.grayscale_luminosity,
            14: self.grayscale_midgray,
            15: self.exit_menu,
        }

    def show_original(self):
        """
        Muestra la imagen original.
        """
        self.image_processor.show_image(self.image_processor.logo)

    def invert_colors(self):
        """
        Muestra la imagen con los colores invertidos.
        """
        inverted = self.image_processor.invert_colors()
        self.image_processor.show_image(inverted)

    def show_red_layer(self):
        """
        Muestra la capa roja de la imagen.
        """
        red = self.image_processor.red_layer()
        self.image_processor.show_image(red)

    def show_green_layer(self):
        """
        Muestra la capa verde de la imagen.
        """
        green = self.image_processor.green_layer()
        self.image_processor.show_image(green)

    def show_blue_layer(self):
        """
        Muestra la capa azul de la imagen.
        """
        blue = self.image_processor.blue_layer()
        self.image_processor.show_image(blue)

    def show_magenta_layer(self):
        """
        Muestra la capa magenta de la imagen.
        """
        magenta = self.image_processor.magenta_layer()
        self.image_processor.show_image(magenta)

    def show_cyan_layer(self):
        """
        Muestra la capa cyan de la imagen.
        """
        cyan = self.image_processor.cyan_layer()
        self.image_processor.show_image(cyan)

    def show_yellow_layer(self):
        """
        Muestra la capa amarilla de la imagen.
        """
        yellow = self.image_processor.yellow_layer()
        self.image_processor.show_image(yellow)

    def combine_layers(self):
        red = self.image_processor.red_layer()
        green = self.image_processor.green_layer()
        blue = self.image_processor.blue_layer()
        combined_img = self.image_processor.combine_layers(red, green, blue)
        self.image_processor.show_image(combined_img)

    def fusion_images(self):
        fusioned = self.image_processor.fusion_images()
        self.image_processor.show_image(fusioned)

    def fusion_images_eq(self):
        fusioned_eq = self.image_processor.fusion_images_eq()
        self.image_processor.show_image(fusioned_eq)

    def factor_image(self):
        factor = input("Ingrese el factor: ")
        factored = self.image_processor.factor_image(factor)
        self.image_processor.show_image(factored)

    def grayscale_average(self):
        avarage = self.image_processor.grayscale_average()
        self.image_processor.show_image(avarage)

    def grayscale_luminosity(self):
        luminosity = self.image_processor.grayscale_luminosity()
        self.image_processor.show_image(luminosity)

    def grayscale_midgray(self):
        midgray = self.image_processor.grayscale_midgray()
        self.image_processor.show_image(midgray)

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
            print("1.  Invertir colores")
            print("2.  Mostrar capa roja")
            print("3.  Mostrar capa verde")
            print("4.  Mostrar capa azul")
            print("5.  Mostrar capa magenta")
            print("6.  Mostrar capa cyan")
            print("7.  Mostrar capa amarilla")
            print("8.  Combinar capas")
            print("9.  combinar imagenes")
            print("10. Combinar imagenes equalizadas")
            print("11. Equalizar imagen")
            print("12. Escala de grises (avarage)")
            print("13. Escala de grises (luminosity)")
            print("14. Escala de grises (midgray)")
            print("15. Salir")

            try:
                option = int(input("\nSelecciona una opción (1-15): "))

                if option in self.options:
                    self.options[option]()  # Ejecuta la opción seleccionada
                else:
                    print(
                        "Opción no válida. Por favor, selecciona una opción entre 1 y 15.")
            except ValueError:
                print("Por favor ingresa un número válido.")


if __name__ == "__main__":
    # Crear el procesador de imágenes y el menú
    logo_path = "utplogo.jpg"
    img1_path = "boat.jpg"
    img2_path = "beach.jpg"
    image_processor = ImageProcessor(logo_path, img1_path, img2_path)
    menu = Menu(image_processor)

    # Ejecutar el menú
    menu.display_menu()
