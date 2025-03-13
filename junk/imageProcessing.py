import numpy as np
import matplotlib.pyplot as plt


def capaImg(img: np.array, capa: int) -> np.array:
    fil, col, cap = img.shape
    imgCapa = np.zeros((fil, col, 3))
    imgCapa[:, :, capa] = img[:, :, capa]
    return imgCapa


def brightnessImg(img: np.array, factor: float) -> np.array:
    imgCopy: np.array = np.copy(img)
    return (imgCopy+factor)


def adjustChannel(img: np.array, factor: float, capa: int) -> np.array:
    imgCopy: np.array = np.copy(img)
    imgCopy[:, :, capa] = imgCopy[:, :, capa] + factor
    return imgCopy


def contrastImg(img: np.array, factor: float, capa: int):
    if (capa == 0):
        img = factor*np.log10(1 + img)
    else:
        img = factor*np.exp(img - 1)
    return img


def imgInvert(imagen: np.array) -> np.array:
    filtro = []
    for i in imagen:
        for r, g, b in i:
            rojo = r*0.2989
            verde = g*0.5870
            azul = b*0.1140
            numero = [int(rojo + verde + azul)]
            filtro.append(numero)
    # Usamos los valores en imagen.shape para conocer el ancho x alto originales
    # y reformateamos la lista para que use esas dimensiones
    result = np.reshape(filtro, imagen.shape[:2])
    return result
