import numpy as np
import sys


class ArrayManipulation:
    def __init__(self) -> None:
        pass

    def array_create_properties(self):
        array = np.array(range(1, 11))
        array_reshape = array.reshape(2, 5)
        return array, array_reshape, array.shape, array.size, array.ndim

    def array_basic_operations(self):
        array1 = np.array(range(1, 6))
        array2 = np.array(range(6, 11))
        array_sum = array1 + array2
        array_product = array1 * array2
        array1_self_sum = np.sum(array1)
        array2_self_sum = np.sum(array2)
        return array1, array2, array_sum, array_product, array1_self_sum, array2_self_sum

    def array_indexing_slicing(self):
        array = np.array(range(1, 11))
        array_index_dict = {x: array[x] for x in range(array.size)}
        array_slice = array[2:7]
        return array, array_index_dict, array_slice

    def array_broadcasting_ufunc(self):
        array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        array_scalar_sum = array + 10
        array_ufunc = np.sqrt(array)
        return array, array_scalar_sum, array_ufunc

    def array_reshape_linear_algebra(self):
        array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        array_transpose = array.T
        array_determinant = np.linalg.det(array)
        # Corregido: no se puede reshape a (3,2) porque la matriz es 3x3
        array_reshape = array.reshape(3, 3)
        dot_transpose = np.dot(array, array_transpose)
        return array, array_transpose, array_determinant, array_reshape, dot_transpose

    def array_data_manipulation(self):
        array1 = np.array(range(1, 11))
        array1.fill(np.nan)
        array2 = np.nan_to_num(array1, nan=0)
        return array1, array2

    def array_save_load(self):
        array = np.array(range(1, 11))
        np.save("array.npy", array)
        array_load = np.load("array.npy")
        return array, array_load


class Menu:
    def __init__(self, arrayManipulation):
        self.arrayManipulation = arrayManipulation
        self.options = {
            1: self.array_create_properties,
            2: self.array_basic_operations,
            3: self.array_indexing_slicing,
            4: self.array_broadcasting_ufunc,
            5: self.array_reshape_linear_algebra,
            6: self.array_data_manipulation,
            7: self.array_save_load,
            8: self.exit_menu,
        }

    def array_create_properties(self):
        array, array_reshape, shape, size, ndim = self.arrayManipulation.array_create_properties()
        print(f"\nCreate array: {array}")
        print(f"Array after reshape:\n{array_reshape}")
        print(f"The shape of the array is:\n{shape}")
        print(f"The size of the array is:\n{size}")
        print(f"The dimension of the array is:\n{ndim}\n")

    def array_basic_operations(self):
        array1, array2, array_sum, array_product, array1_self_sum, array2_self_sum = self.arrayManipulation.array_basic_operations()
        print(f"\nArray 1: {array1}")
        print(f"Array 2: {array2}")
        print(f"Sum of arrays 1 and 2: {array_sum}")
        print(f"Product of arrays: {array_product}")
        print(f"Sum of elements of array 1: {array1_self_sum}")
        print(f"Sum of elemtents of array 2: {array2_self_sum}\n")

    def array_indexing_slicing(self):
        array, array_index_dict, array_slice = self.arrayManipulation.array_indexing_slicing()
        print(f"\nArray: {array}")
        print("Indexing array (The first index of an array is 0):")
        for index, value in array_index_dict.items():
            print("index: {} value: {}".format(index, value))
        print(f"Slicing array [2:7]: {array_slice}\n")

    def array_broadcasting_ufunc(self):
        array, array_scalar_sum, array_ufunc = self.arrayManipulation.array_broadcasting_ufunc()
        print(f"\nArray:\n{array}")
        print(f"Scalar sum (Adding the scalar 10 to all elements of the array):\n{
              array_scalar_sum}")
        print(f"Ufunc (Appling the sqrt function to all elements of the array):\n{
              array_ufunc}")

    def array_reshape_linear_algebra(self):
        array, array_transpose, array_determinant, array_reshape, dot_transpose = self.arrayManipulation.array_reshape_linear_algebra()
        print(f"\nArray:\n{array}")
        print(f"Transpose of array:\n{array_transpose}")
        print(f"Array determinant:\n{array_determinant}")
        print(f"Array reshape:\n{array_reshape}")
        print(f"Dot product of array and its transpose:\n{dot_transpose}")

    def array_data_manipulation(self):
        array1, array2 = self.arrayManipulation.array_data_manipulation()
        print(f"\nArray 1: {array1}")
        print(f"Array 2: {array2}")

    def array_save_load(self):
        array, array_load = self.arrayManipulation.array_save_load()
        print(f"\nArray: {array}")
        print(f"Array load: {array_load}")

    def exit_menu(self):
        sys.exit()

    def display_menu(self):
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Creación de Arrays")
            print("2. Operaciones básicas de Arrays")
            print("3. Indexación y Slicing de Arrays")
            print("4. Broadcasting y U-Functions")
            print("5. Reshape y Linear Algebra")
            print("6. Array data manipulation")
            print("7. Save and Load Arrays")
            print("8. exit")

            try:
                option = int(input("Select an option: (1/8)"))
                if option in self.options:
                    self.options[option]()
                else:
                    print("Invalid option, try again.")
            except ValueError:
                print("Invalid option, please enter a number between 1 and 8.")


if __name__ == "__main__":
    array_manipulation = ArrayManipulation()
    menu = Menu(array_manipulation)
    menu.display_menu()
