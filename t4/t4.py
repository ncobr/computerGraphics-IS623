import numpy as np
import random
import sys


class ArrayManipulation:
    def __init__(self):
        pass

    def one_dimensional_array(self):
        return np.array(range(1, 11))

    def multi_dimensional_array(self):
        return np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def array_basic_operations(self):
        array1 = np.array(range(1, 6))
        array2 = np.array(range(1, 6))
        result_array = array1 + array2
        return array1, array2, result_array

    def array_math_funcs(self):
        array = np.array(range(1, 11))
        exponent_array = np.exp(array)
        return exponent_array

    def array_indexing_slicing(self):
        array = np.array(range(1, 11))
        odd_numbers = array[1::2]
        return odd_numbers

    def random_data_generator(self):
        return np.random.randint(2, size=(10))

    def agregattion_funcs(self):
        array = np.array(range(1, 6))
        median = sum(array) / len(array)
        return median

    def array_fabric_funcs(self):
        array = np.full(5, 7)
        return array

    def alignment_broadcasting(self):
        array1 = np.array(range(1, 4))
        array2 = np.array(range(4, 7))
        array_broadcasting = array1 + array2
        return array1, array2, array_broadcasting

    def transformations_resize(self):
        array = np.array(range(1, 7))
        array_reshape = array.reshape(2, 3)
        return array, array_reshape


class Menu:
    def __init__(self, arrayManipulation):
        self.arrayManipulation = arrayManipulation
        self.options = {
            1: self.one_dimensional_array,
            2: self.multi_dimensional_array,
            3: self.array_basic_operations,
            4: self.array_math_funcs,
            5: self.array_indexing_slicing,
            6: self.random_data_generator,
            7: self.agregattion_funcs,
            8: self.array_fabric_funcs,
            9: self.alignment_broadcasting,
            10: self.transformations_resize,
            11: self.exit_menu,
        }

    def one_dimensional_array(self):
        print(f"\nOne dimensional array: {
              self.arrayManipulation.one_dimensional_array()}\n")

    def multi_dimensional_array(self):
        print(
            f"Multi-dimensional array:\n{self.arrayManipulation.multi_dimensional_array()}\n")

    def array_basic_operations(self):
        array1, array2, result_array = self.arrayManipulation.array_basic_operations()
        print(f"\nArray 1: {array1}\nArray 2: {
              array2}\nSum of the arrays: {result_array}\n")

    def array_math_funcs(self):
        exponent_array = self.arrayManipulation.array_math_funcs()
        print(f"\nExponent array: {exponent_array}\n")

    def array_indexing_slicing(self):
        print(f"\nArray of odd numbers: {
              self.arrayManipulation.array_indexing_slicing()}")

    def random_data_generator(self):
        print(f"\nArray of 10 random numbers between 0 and 1: {
              self.arrayManipulation.random_data_generator()}\n")

    def agregattion_funcs(self):
        print(f"\nMedian: {self.arrayManipulation.agregattion_funcs()}\n")

    def array_fabric_funcs(self):
        print(f"\nArray filled with 7: {
              self.arrayManipulation.array_fabric_funcs()}\n")

    def alignment_broadcasting(self):
        array1, array2, array_broadcasting = self.arrayManipulation.alignment_broadcasting()
        print(f"\nArray 1: {array1}\nArray 2: {
              array2}\nSum of arrays (Broadcasting): {array_broadcasting}\n")

    def transformations_resize(self):
        array, array_reshape = self.arrayManipulation.transformations_resize()
        print(f"\nArray: {array}\nArray after reshape:\n{array_reshape}\n")

    def exit_menu(self):
        sys.exit()

    def display_menu(self):
        while True:
            print("---      Menu        ---")
            print("1. One-dimensional array")
            print("2. Multi-dimensional array")
            print("3. Basic array operations")
            print("4. Array Math Functions")
            print("5. Array Indexing and Slicing")
            print("6. Random Data Generator")
            print("7. Aggregation and Reduction Functions")
            print("8. Array Fabric Functions")
            print("9. Alignment and Broadcasting")
            print("10. Transformations and Resizing")
            print("11. Exit")

            try:
                option = int(input("Select an option (1/11): "))
                if option in self.options:
                    self.options[option]()
                else:
                    print("Invalid option, try again.")
            except ValueError:
                print("Invalid option, please enter a number between 1 and 11.")


if __name__ == "__main__":
    arrayManipulation = ArrayManipulation()
    menu = Menu(arrayManipulation)
    menu.display_menu()
