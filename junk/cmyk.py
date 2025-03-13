
import matplotlib.pyplot as plt
import numpy as np
from skimage import io


factor=255
image_mcyk = io.imread("utplogo.jpg")/255.0
print("- Dimensiones de la imagen:")
print(image_mcyk.shape)
filas = image_mcyk.shape[0]
columnas = image_mcyk.shape[1]
print(filas)
print(columnas)

plt.figure()
plt.subplot(221)
plt.imshow(image_mcyk, vmin=0, vmax=1)
plt.title("imagen original")

image_magenta = np.copy(image_mcyk)
image_magenta[:, :, 0] = np.ones((filas, columnas)) * factor
image_magenta[:, :, 2] = np.ones((filas, columnas))*factor
plt.subplot(222)

plt.title("Imagen canal Magenta")
plt.imshow(image_magenta)

image_cyan = np.copy(image_mcyk)
image_cyan[:, :, 1] = np.ones((filas, columnas)) * factor
image_cyan[:, :, 2] = np.ones((filas, columnas))*factor
plt.subplot(223)
plt.title("Imagen canal Cyan")
plt.imshow(image_cyan)

image_yellow = np.copy(image_mcyk)
image_yellow[:, :, 0] = np.ones((filas, columnas))*factor
image_yellow[:, :, 1] = np.ones((filas, columnas)) *factor
plt.subplot(224)

plt.title("Imagen canal yellow")
plt.imshow(image_yellow)
plt.show()
