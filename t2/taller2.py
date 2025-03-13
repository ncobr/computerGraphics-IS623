import random
import sys


class Exercises:
    """
    Clase que contiene los métodos para resolver los ejercicios.
    Agrega nuevos métodos según sea necesario.
    """

    def __init__(self):
        pass

    def basic_calculator(self, option, a, b):
        if option > 4 or option < 1:
            print("Opción no válida. Intente nuevamente.")
        elif option == 1:
            return a + b
        elif option == 2:
            return a - b
        elif option == 3:
            return a * b
        elif option == 4:
            return a / b

    def list_filter(self, numlist):
        numlist = list(map(int, numlist.split()))
        filterlist = []
        for i in numlist:
            if not i % 2 == 0:
                filterlist.append(i)
        return filterlist

    def celcius_to_fahrenheit(self, celcius_list):
        celcius_list = list(map(float, celcius_list.split()))
        fahrenheit_list = list(
            map(lambda celcius: (celcius * 9/5) + 32, celcius_list))
        return fahrenheit_list

    def grading_system(self, grades_list):
        grades_list = list(map(float, grades_list.split()))
        converted_grades_list = []
        for grade in grades_list:
            if grade >= 0 and grade < 2.5:
                converted_grades_list.append("F")
            elif grade > 2.5 and grade < 5.0:
                converted_grades_list.append("D")
            elif grade > 5.0 and grade < 7.5:
                converted_grades_list.append("C")
            elif grade > 7.5 and grade < 10.0:
                converted_grades_list.append("B")
            elif grade == 10.0:
                converted_grades_list.append("A")
            elif grade < 0 or grade > 10.0:
                print(f"La nota ingresada {grade}, no es válida")

        return converted_grades_list

    def word_count(self, text):
        text = text.lower()
        words = text.split()
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        return word_count

    def find_in_list(self, word, text_list):
        text_list = list(map(str, text_list.split()))
        for index, item in enumerate(text_list):
            if item == word:
                return index
        return -1

    def validate_brackets(self, brackets_list):
        count = 0

        for char in brackets_list:
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1
            if count < 0:
                return False
        return count == 0

    def sort_tuple(self, names_ages):
        return sorted(names_ages, key=lambda x: (x[1], x[0]))

    def password_generator(self, length):
        letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        numbers = "0123456789"
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?/\\"
        chars = letters + numbers + symbols

        return "".join(random.choice(chars) for _ in range(length))


class Agenda:
    def __init__(self):
        self.agenda = {}

    def add_contact(self):
        name = input("Ingrese el nombre del contacto: ")
        telephone = input("Ingrese el número de teléfono: ")

        if name in self.agenda:
            print("El contacto ya existe.")
        else:
            self.agenda[name] = telephone
            print(f"Contacto {name} agregado correctamente.")

    def search_contact(self):
        name = input("Ingrese el nombre del contacto a buscar: ")
        if name in self.agenda:
            print(f"{name}: {self.agenda[name]}")
        else:
            print("El contacto no existe.")

    def del_contacto(self):
        name = input("Ingrese el nombre del contacto a eliminar: ")
        if name in self.agenda:
            del self.agenda[name]
            print(f"Contacto {name} eliminado correctamente.")
        else:
            print("El contacto no existe.")

    def show_contactos(self):
        if not self.agenda:
            print("La agenda está vacía.")
        else:
            print("\nAgenda telefónica:")
            for name, telephone in self.agenda.items():
                print(f"{name}: {telephone}")
            print()

    def agenda_telefonica(self):
        while True:
            print("\n--- AGENDA TELEFÓNICA ---")
            print("1. Agregar contacto")
            print("2. Buscar contacto")
            print("3. Eliminar contacto")
            print("4. Mostrar contactos")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.add_contact()
            elif opcion == "2":
                self.search_contact()
            elif opcion == "3":
                self.del_contacto()
            elif opcion == "4":
                self.show_contactos()
            elif opcion == "5":
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción inválida, intente de nuevo.")


class Menu:
    """
    Clase que gestiona el menú de opciones para ejecutar los métodos de Exercises.
    """

    def __init__(self, exercises, agenda):
        self.exercises = exercises
        self.agenda = agenda
        self.options = {
            1: self.basic_calculator,
            2: self.list_filter,
            3: self.celcius_to_fahrenheit,
            4: self.grading_system,
            5: self.word_count,
            6: self.find_in_list,
            7: self.validate_brackets,
            8: self.sort_tuple,
            9: self.password_generator,
            10: self.agenda_telefonica,
            11: self.exit_menu,
        }

    def basic_calculator(self):
        option = int(input(
            "Ingrese la operación a realizar (1: Suma, 2: Resta, 3: Multiplicación, 4: División): "))
        a = float(input("Ingrese el primer número: "))
        b = float(input("Ingrese el segundo número: "))
        print(f"El resultado de la operación es: {
              self.exercises.basic_calculator(option, a, b)}")

    def list_filter(self):
        numlist = input(
            "Ingrese los números de la lista separados por un espacio: ")
        print(f"La lista sin números pares es: {
              self.exercises.list_filter(numlist)}")

    def celcius_to_fahrenheit(self):
        celcius_list = input(
            "Ingrese los grados celcius separados por un espacio: ")
        print(f"Los grados celcius convertidos a fahrenheit son: {
              self.exercises.celcius_to_fahrenheit(celcius_list)}")

    def grading_system(self):
        grades_list = input("Ingrese las notas separadas por un espacio: ")
        print(f"Los resultados de la calificación son: {
              self.exercises.grading_system(grades_list)}")

    def word_count(self):
        text = input("Ingrese el texto: ")
        print(f"El conteo de palabras es: {self.exercises.word_count(text)}")

    def find_in_list(self):
        word = input("Ingrese la palabra: ")
        text_list = input(
            "Ingrese la lista de palabras separadas por un espacio: ")
        print(f"La palabra está en la posición: {
              self.exercises.find_in_list(word, text_list)}")

    def validate_brackets(self):
        brackets_list = input("Ingrese la cadena de paréntesis: ")
        print(f"Validez de la cadena es: {
              self.exercises.validate_brackets(brackets_list)}")

    def sort_tuple(self):
        names_ages = [("Jose", 25), ("Maria", 30), ("Pedro", 20), ("Luis", 28)]
        print(f"Usando la lista de ejemplo: {names_ages}")
        print(f"La lista ordenada es: {self.exercises.sort_tuple(names_ages)}")

    def password_generator(self):
        length = int(input("Ingrese la longitud deseada: "))
        print(f"El password generado es: {
              self.exercises.password_generator(length)}")

    def agenda_telefonica(self):
        self.agenda.agenda_telefonica()

    def exit_menu(self):
        sys.exit()

    def display_menu(self):
        """
        Muestra el menú principal y ejecuta la opción seleccionada.
        """
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Calculadora básica")
            print("2. Filtro de lista")
            print("3. Convertir Celsius a Fahrenheit")
            print("4. Sistema de calificación")
            print("5. Contar palabras")
            print("6. Buscar en lista")
            print("7. Validar paréntesis")
            print("8. Ordenar tupla")
            print("9. Generador de contraseñas")
            print("10. Agenda telefónica")
            print("11. Salir")

            try:
                opcion = int(input("Seleccione una opción: "))
                if opcion in self.options:
                    self.options[opcion]()
                else:
                    print("Opción inválida, intente de nuevo.")
            except ValueError:
                print("Opción no válida, ingrese un número.")


if __name__ == "__main__":
    exercises = Exercises()
    agenda = Agenda()
    menu = Menu(exercises, agenda)
    menu.display_menu()
