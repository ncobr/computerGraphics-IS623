from re import X
import numpy as np
import matplotlib.pyplot as plt

# Array de una dimension
# arr_1d = np.array([1, 2, 3, 4, 5])
# print("Array de una dimension", arr_1d)
# arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
# print("Array de dos dimensiones", arr_2d)
# arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
# print("Array de tres dimensiones", arr_3d)

# diangonal = np.diag([1, 2, 3, 4, 5])
# print("Matriz con una diagonal\n", diangonal, "\n")

# random_matrix = np.random.random((4, 4))
# print("Matriz con datos aleatorios\n", random_matrix, "\n")

# linspace_matrix = np.linspace(0, 1, 10)
# print("Matriz con valores de 0 a 1\n", linspace_matrix, "\n")

# x = np.linspace(0, 10, 100)
# print(x, "\n")
#
# y = np.random.randint(1, 10, 21)
# y = np.sin(x)
# plt.plot(x, y)
# plt.grid()
# plt.show()

img1 = np.array(plt.imread("../../../Imágenes/wallpapers/b.jpg"))/255
img2 = img1 * 3

# plt.figure(1)
# plt.imshow(img1)
# plt.figure(2)
# plt.imshow(img2)
# plt.show()
# print(img1)

imgn1 = np.array(plt.imread(
    "../../../Imágenes/wallpapers/1.jpg"))/255
imgn2 = np.array(plt.imread(
    "../../../Imágenes/wallpapers/2.jpg"))/255


centr = imgn1[134:300, 400:900]

plt.imshow(centr)
plt.show()
