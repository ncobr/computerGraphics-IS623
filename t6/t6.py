import matplotlib.pyplot as plt
import numpy as np
import random
import math


def create_array_A():
    array_A = np.array(range(1, 16))
    array_A_reshape = array_A.reshape(3, 5)
    print(f"\nArray A:\n{array_A}\nReshaped array A (3x5):\n{
          array_A_reshape}\n")

    sum_array_A = np.sum(array_A)
    product_array_A = np.prod(array_A)
    # mean_array_A = sum(array_A) / len(array_A)
    mean_array_A = np.mean(array_A)

    print(f"\nSum of array A: {sum_array_A}\nProduct of array A: {
        product_array_A}\nMean of array A: {mean_array_A}\n")

    slicing_A = array_A_reshape[1, 1:3]
    print(f"Selecting, second and third elements of second row: {slicing_A}")

    # array_B = array_A[array_A > 7]
    array_B = np.array([x for x in array_A if x > 7])
    print(f"\nArray B: {array_B}")

    array_C = (np.array(range(1, 10))).reshape(3, 3)
    print(f"\nArray C: {array_C}")
    array_C_determinant = np.linalg.det(array_C)
    array_C_inverse = np.linalg.inv(array_C)
    print(f"Array C determinant: {array_C_determinant}")
    print(f"Array C inverse: {array_C_inverse}")

    array_D = np.random.randint(100, size=100)
    array_D_min = np.amin(array_D)
    array_D_max = np.amax(array_A)
    array_D_mean = np.mean(array_D)
    array_D_std = np.std(array_D)
    print(f"\nArray D: {array_D}")
    print(f"Min of array D: {array_D_min}")
    print(f"Max of array D: {array_D_max}")
    print(f"Mean of array D: {array_D_mean}")
    print(f"Standard deviation of array D: {array_D_std}")

    x = np.linspace(-(2 * np.pi), (2 * np.pi), 256, endpoint=True)
    c, s = np.cos(x), np.sin(x)
    plt.plot(x, c, color="blue", linewidth=2.5, linestyle="-")
    plt.plot(x, s, color="red", linewidth=2.5, linestyle="-")
    plt.show()

    disp_D_x = len(array_D)
    plt.plot(range(len(array_D)), array_D,
             color="blue", linewidth=2.5, linestyle="dotted")
    plt.show()

    plt.hist(array_D, bins=10, color="blue", edgecolor="black", alpha=0.5)
    plt.show()

    image = np.array(plt.imread("image.jpg"))
    image_gray = np.mean(image, axis=2)
    plt.imshow(image_gray, cmap="gray")
    plt.axis("off")
    plt.show()


create_array_A()
