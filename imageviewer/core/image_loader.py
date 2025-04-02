import numpy as np
import matplotlib.pyplot as plt


class ImageLoader():
    def __init__(self):
        pass

    def load(self, filepath):
        try:
            image = np.array(plt.imread(filepath))
            return image
        except Exception as e:
            print(f"Eroor loading image: {str(e)}")
            return None

    def save(self, filepath, image):
        try:
            plt.imsave(filepath, image, cmap='gray')
            return True
        except Exception as e:
            print(f"Erro saving image: {str(e)}")
            return False
