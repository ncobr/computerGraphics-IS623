import numpy as np
import matplotlib.pyplot as plt


def resize_image(image_matrix, new_height, new_width):
    if len(image_matrix.shape) == 3:
        oh, ow, _ = image_matrix.shape
    else:
        oh, ow = image_matrix.shape

    re_image_matrix = np.array([
        np.array([image_matrix[(oh*h // new_height)][(ow*w // new_width)]
                 for w in range(new_width)])
        for h in range(new_height)
    ])

    return re_image_matrix


def punto_1(img1, img2, img3, img4, color):
    """
    Punto 1 del parcial:
        Funcion que recibe como parametro 4 imagenes y un color
        y luego fuciona las cuatro imagenes y las une con un borde
        del color especificado

    Params:
        img1 (str): Ruta de la primera imagen
        img2 (str): Ruta de la segunda imagen
        img3 (str): Ruta de la tercera imagen
        img4 (str): Ruta de la cuarta imagen
        color (int): Color del borde

    Returns:
        bordered_image (np.array): Imagenes combinadas y con borde
    """

    # Lectura de imagenes
    img1 = np.array(plt.imread(img1))
    img2 = np.array(plt.imread(img2))
    img3 = np.array(plt.imread(img3))
    img4 = np.array(plt.imread(img4))

    # Se ponen las imagenes al mismo tamaño para evitar erores
    img1_resize = resize_image(img1, 1000, 1000)
    img2_resize = resize_image(img2, 1000, 1000)
    img3_resize = resize_image(img3, 1000, 1000)
    img4_resize = resize_image(img4, 1000, 1000)

    result_image_top = np.concatenate((img1_resize, img2_resize), axis=1)
    result_image_bottom = np.concatenate((img3_resize, img4_resize), axis=1)
    result_image = np.concatenate(
        (result_image_top, result_image_bottom), axis=0)

    border_size = 100
    h, w, c = result_image.shape
    # Se llena el borde con el color
    bordered_image = np.full(
        (h + 2 * border_size, w + 2 * border_size, c), color, dtype=np.uint8)

    bordered_image[border_size:border_size + h,
                   border_size:border_size + w] = result_image

    plt.imshow(bordered_image)
    plt.title("Punto 1: Unión de 4 imágenes con borde")
    plt.axis("off")
    plt.show()
    return bordered_image


def punto_2(img1, img2):
    """
    Punto 2 del parcial:
        esta funcion recibe como paramentro dos imagenes
        y luego las fusiona

    Params:
        img1 (str): Ruta de la primera imagen
        img2 (str): Ruta de la segunda imagen

    Returns:
        img1 (np.array): imagen 1 modificada, fusionando con la segunda
    """
    logo = np.array(plt.imread(img2))
    print(img1.shape)
   # y1, x1 = 500, 300  # Top-left corner
   # y2, x2 = 1500, 1800  # Botto,-right corner
   # cropped_img = img1[y1:y2, x1:x2]

   # for i in range(cropped_img.shape[0], cropped_img.shape[1]):
   #     img1[y1:y2, x1:x2] = logo

    hL, wL = img1.shape[:2]
    hS, wS = logo.shape[:2]

    y1, x1 = (hL - hS) // 2, (wL - wS) // 2
    y2, x2 = y1 + hS, x1 + wS

    factor = 0.5
    img1[y1:y2, x1:x2] = logo

    plt.imshow(img1)
    plt.title("Punto 2: Fusion de imagenes")
    plt.axis("off")
    plt.show()
    return img1


"""
Cada imagen esta guradada en el directorio "src"
"""
img1 = "src/img1.jpg"
img2 = "src/img2.jpg"
img3 = "src/img3.jpg"
img4 = "src/img4.jpg"
logo = "src/logo.jpg"

color = int(input("Inserte un color para el borde de la imagen (0-255): "))

# punto_1(img1, img2, img3, img4, color=123)
# Uso (reciclo) la imagen resultante del punto 1 para el punto 2
img_for_p2 = punto_1(img1, img2, img3, img4, color)
punto_2(img_for_p2, logo)
