import numpy as np


def array_manipulation():
    # Creating array_a with specific values
    array_a = np.array([2, 3, 5, 1, 4, 7, 9, 8, 6, 10])
    print(f"Array A: {array_a}")

    # Creating array_b with a range from 11 to 20
    array_b = np.array(range(11, 21))
    print(f"Array B: {array_b}")

    # Concatenating array_a and array_b into array_c
    array_c = np.concatenate((array_a, array_b))
    print(f"Concatenated Array C: {array_c}")

    # Finding the minimum value of array_c
    array_c_min = np.amin(array_c)
    print(f"Minimum value in Array C: {array_c_min}")

    # Finding the maximum value of array_c
    array_c_max = np.amax(array_c)
    print(f"Maximum value in Array C: {array_c_max}")

    # Getting the length (size) of array_c
    numpy_len_array_c = array_c.size
    print(f"Size of Array C: {numpy_len_array_c}")

    # Calculating the mean using standard sum and length
    normal_mean_array_c = sum(array_c) / len(array_c)
    print(f"Mean of Array C (manual calculation): {normal_mean_array_c}")

    # Calculating the mean using NumPy
    numpy_mean_array_c = np.mean(array_c)
    print(f"Mean of Array C (NumPy): {numpy_mean_array_c}")

    # Calculating the sum of all elements in array_c
    sum_array_c = sum(array_c)
    print(f"Sum of Array C: {sum_array_c}")

    # Creating a new array with elements greater than 5
    array_d = np.array([x for x in array_c if x > 5])
    print(f"Array D (elements > 5): {array_d}")

    # Creating a new array with elements between 5 and 15 (exclusive)
    array_e = np.array([x for x in array_c if 5 < x < 15])
    print(f"Array E (5 < elements < 15): {array_e}")

    # Replacing values at index positions 4 to 6 with 7
    array_c[4:7] = 7
    print(f"Array C after replacing indices 4 to 6 with 7: {array_c}")

    # Getting unique values in array_c (like mode)
    mode_array_c = np.unique(array_c)
    print(f"Unique values in Array C: {mode_array_c}")

    # Sorting array_c in ascending order
    array_c.sort()
    print(f"Sorted Array C: {array_c}")

    # Multiplying all elements of array_c by 10
    array_c_mult = array_c * 10
    print(f"Array C multiplied by 10: {array_c_mult}")

    # Multiplying elements at indices 5 to 7 by 10
    array_c[5:8] *= 10
    print(f"Array C after multiplying indices 5 to 7 by 10: {array_c}")

    # Multiplying elements at indices 13 to 15 by 10
    array_c[13:16] *= 10
    print(f"Array C after multiplying indices 13 to 15 by 10: {array_c}")


array_manipulation()

