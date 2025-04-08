import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor:
    def __init__(self):
        pass

    def load_image(self, path):
        try:
            image = np.array(plt.imread(path))
            return image
        except Exception as e:
            raise Exception(f"Error al cargar la imagen: {str(e)}")

    def to_uint8(self, image):
        if image.dtype != np.uint8:
            if image.max() > 1.0:
                return np.clip(image, 0, 255).astype(np.uint8)
            else:
                return (image * 255).clip(0, 255).astype(np.uint8)
        return image

    def adjust_brightness(self, image, factor):
        adjusted = image + (factor * 255)
        return np.clip(adjusted, 0, 255).astype(image.dtype)

    def adjust_contrast(self, image, factor):
        mean = np.mean(image)
        adjusted = (image - mean) * factor + mean
        return np.clip(adjusted, 0, 255).astype(image.dtype)

    def to_grayscale(self, image):
        if len(image.shape) == 2:
            return image

        return np.mean(image, axis=2)

    def filter_channels(self, image, r_active, g_active, b_active, c_active, m_active, y_active):
        if len(image.shape) != 3:
            return image  # No es una imagen a color

        result = np.copy(image)
        if not r_active:
            result[:, :, 0] = 0
        if not g_active:
            result[:, :, 1] = 0
        if not b_active:
            result[:, :, 2] = 0
        if not c_active:
            result[:, :, 0] = 255  # Rojo al máximo (ausencia de cian)
        if not m_active:
            result[:, :, 1] = 255  # Verde al máximo (ausencia de magenta)
        if not y_active:
            result[:, :, 2] = 255  # Azul al.maxcdn (ausencia de amarillo)

        return result

    def negative_image(self, image):
        return 255 - image

    def binarize(self, image, threshold):
        if len(image.shape) == 3:
            gray = self.to_grayscale(image)
        else:
            gray = image

        # Aplicar umbral
        binary = np.zeros_like(gray)
        binary[gray > threshold] = 255

        return binary
