# IS623 - Computacion grafica
# Taller numero 1 - Fisica computacional
# Autor: Nicolas Betancur
# Fecha: dom 09 mar 2025 14:33:58 -05
import math
from matplotlib.pyplot import magnitude_spectrum
from scipy.constants import g


class Exercises:
    """
    Clase que contiene métodos para resolver diversos problemas de física computacional.
    """

    def __init__(self):
        pass

    def freeFallCalc(self, h):
        """
        Calcula el tiempo de caída libre de un objeto desde una altura dada.

        Parámetros:
        h (float): Altura desde la que cae el objeto (en metros).

        Retorna:
        float: Tiempo de caída libre (en segundos).
        """
        t = math.sqrt(2*h/g)
        return t

    def speedUnitConversion(self, v, unit):
        """
        Convierte una velocidad entre m/s y km/h.

        Parámetros:
        v (float): Valor de la velocidad.
        unit (str): Unidad de la velocidad, puede ser "m/s" o "km/h".

        Retorna:
        float: Velocidad convertida a la unidad deseada.
        """
        if unit == "m/s":
            return v * 3.6

        if unit == "km/h":
            return v / 3.6

        else:
            raise ValueError(
                "Tipo de unidad no reconocido. Por favor, ingresa 'm/s' o 'km/h'.")

    def displacementCalc(self, u, a, t):
        """
        Calcula el desplazamiento de un objeto con movimiento uniformemente acelerado.

        Parámetros:
        u (float): Velocidad inicial (m/s).
        a (float): Aceleración (m/s^2).
        t (float): Tiempo transcurrido (s).

        Retorna:
        float: Desplazamiento (en metros).
        """
        s = (u * t) + (1/2 * a * t**2)
        return s

    def vectorAddition(self, v1, v2):
        """
        Suma dos vectores de igual longitud.

        Parámetros:
        v1 (str): Componentes del primer vector separados por espacios.
        v2 (str): Componentes del segundo vector separados por espacios.

        Retorna:
        list: Vector resultante de la suma.
        """
        v1 = list(map(float, v1.split()))
        v2 = list(map(float, v2.split()))
        if len(v1) != len(v2):
            raise ValueError("Los vectores deben tener la misma longitud")

        v3 = [v1[i] + v2[i] for i in range(len(v1))]
        return v3

    def scalarVectorProduct(self, v1, v2):
        """
        Calcula el producto escalar entre dos vectores.

        Parámetros:
        v1 (str): Componentes del primer vector separados por espacios.
        v2 (str): Componentes del segundo vector separados por espacios.

        Retorna:
        tuple: (Ángulo en grados, Producto escalar)
        """
        v1 = list(map(float, v1.split()))
        v2 = list(map(float, v2.split()))
        if len(v1) != len(v2):
            raise ValueError("Los vectores deben tener la misma longitud")

        magnitude_v1 = math.sqrt(sum(x**2 for x in v1))
        magnitude_v2 = math.sqrt(sum(x**2 for x in v2))

        cos_theta = (sum(v1[i] * v2[i] for i in range(len(v1)))
                     ) / (magnitude_v1 * magnitude_v2)
        angle = math.degrees(math.acos(cos_theta))

        scalarProduct = magnitude_v1 * magnitude_v2 * cos_theta

        return angle, scalarProduct

    def projectileLaunch(self, v0, theta):
        """
        Calcula el alcance y la altura máxima de un proyectil lanzado con un ángulo dado.

        Parámetros:
        v0 (float): Velocidad inicial (m/s).
        theta (float): Ángulo de lanzamiento (grados).

        Retorna:
        tuple: (Alcance máximo R, Altura máxima H)
        """
        theta_rad = math.radians(theta)

        R = (v0**2 * math.sin(2 * theta_rad)) / g
        H = (v0**2 * math.sin(theta_rad)**2) / (2 * g)

        return R, H


class Menu:
    def __init__(self, exercises):
        self.exercises = exercises
        self.options = {
            1: self.freeFallCalc,
            2: self.speedUnitConversion,
            3: self.displacementCalc,
            4: self.vectorAddition,
            5: self.scalarVectorProduct,
            6: self.projectileLaunch,
            7: self.exitMenu,
        }

    def freeFallCalc(self):
        h = float(input("Ingrese la altura: "))
        ans = self.exercises.freeFallCalc(h)
        print(f"\nEl tiempo de caida libre es: {ans}\n")

    def speedUnitConversion(self):
        v = float(input("Ingrese la velocidad: "))
        unit = input("Ingrese la unidad de velocidad (m/s o km/h): ")
        ans = self.exercises.speedUnitConversion(v, unit)
        print(f"\nLa velocidad {v} en {unit} es: {ans}\n")

    def displacementCalc(self):
        u = float(input("Ingrese la velocidad inicial: "))
        a = float(input("Ingrese la aceleracion: "))
        t = float(input("Ingrese el tiempo: "))
        ans = self.exercises.displacementCalc(u, a, t)
        print(f"\nEl desplazamiento es: {ans}\n")

    def vectorAddition(self):
        v1 = input(
            "Ingrese los componentes del primer vector (separados por un espacio): ")
        v2 = input(
            "Ingrese los componentes del segundo vector (separados por un espacio): ")
        ans = self.exercises.vectorAddition(v1, v2)
        print(f"\nEl vector resultante es: {ans}\n")

    def scalarVectorProduct(self):
        v1 = input(
            "Ingrese los componentes del primer vector (separados por un espacio): ")
        v2 = input(
            "Ingrese los componentes del segundo vector (separados por un espacio): ")
        angle, scalarProduct = self.exercises.scalarVectorProduct(v1, v2)
        print(f"\nAngulo entre los vectores: {angle}°")
        print(f"Producto escalar: {scalarProduct}\n")

        pass

    def projectileLaunch(self):
        v0 = float(input("Ingrese la velocidad inicial: "))
        theta = float(input("Ingrese el angulo de lanzamiento: "))
        R, H = self.exercises.projectileLaunch(v0, theta)
        print(f"Alcance máximo (R): {R:.2f} m")
        print(f"Altura máxima (H): {H:.2f} m")

    def exitMenu(self):
        print("Saliendo del menu...")
        exit()

    def displayMenu(self):
        while True:
            print("\n--- Menu de Opciones ---")
            print("1. Calcular caida libre")
            print("2. Convertir velocidad")
            print("3. Calcular desplazamiento")
            print("4. Sumar vectores")
            print("5. Producto escalar")
            print("6. Lanzamiento de proyectil")
            print("7. Salir")
            try:
                option = int(input("\nSelecciona una opcion (1-7): "))

                if option in self.options:
                    self.options[option]()
                else:
                    print(
                        "Opción no válida. Por favor, selecciona una opción entre 1 y 9.")
            except ValueError:
                print("Por favor ingresa un número válido.")


if __name__ == "__main__":
    exercises = Exercises()
    menu = Menu(exercises)
    menu.displayMenu()
