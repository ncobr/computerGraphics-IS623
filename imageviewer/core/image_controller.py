import numpy as np
from core.image_loader import ImageLoader
from core.image_processor import ImageProcessor


class ImageControl:
    def __init__(self):
        self.loader = ImageLoader()
        self.processor = ImageProcessor
        self.original_image = None
        self.current_image = None

    def load_image(self, filepath):
        image_data = self.loader.load(filepath)
        if image_data is not None:
            self.original_image = np.copy(image_data)
            self.current_image = np.copy(image_data)
            return self.current_image
        return None

    def get_original_image(self):
        return np.copy(self.original_image) if self.original_image is not None else None

    def get_current_image(self):
        """Devuelve una copia de la imagen actual"""
        return np.copy(self.current_image) if self.current_image is not None else None

    def process_image(self, operation, params=None):
        if self.original_image is None:
            return None

        operations = {
            "brightness": self.processor.brightness,
            "contrast": self.processor.adjust_contrast,
            "rotate": self.processor.rotate_image,
            'filter_red': self.processor.red_layer,
            'filter_green': self.processor.green_layer,
            'filter_blue': self.processor.blue_layer,
            'filter_cyan': self.processor.cyan_layer,
            'filter_magenta': self.processor.magenta_layer,
            'filter_yellow': self.processor.yellow_layer,
            'invert': self.processor.invert_colors,
            'grayscale_avg': self.processor.grayscale_average,
            'binarize': self.processor.binarize_image,
        }

        if operation not in operations:
            return None

        if operation in ['brightness', 'contrast', 'rotate', 'zoom', 'binarize']:
            self.current_image = operations[operation](
                params, self.original_image)
        else:
            self.current_image = operations[operation](self.original_image)

        return self.current_image

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = np.copy(self.original_image)
            return self.current_image
        return None

    def save_image(self, filepath):
        if self.current_image is not None:
            self.loader.save(filepath, self.current_image)
            return True
        return False
