import numpy as np
import matplotlib.pyplot as plt
import math
import sys


class TaylorSeries:
    def __init__(self) -> None:
        pass

    def exponential_series(self, x, n):
        exp = 0
        for i in range(n):
            exp += x**i / math.factorial(i)
        return exp

    def sin_series(self, x, n):
        sin_x = 0
        for i in range(n):
            sin_x += ((-1)**i / math.factorial(2 * i + 1)) * (x**(2 * i + 1))
        return sin_x

    def cos_series(self, x, n):
        cos_x = 0
        for i in range(n):
            cos_x += ((-1)**i / math.factorial(2 * i)) * (x**(2 * i))
        return cos_x

    def tan_series(self, x, n):
        tan_x = 0
        coeff = [1, 1/3, 2/15, 17/315, 62/2835, 1382/155925]
        for i in range(min(n, len(coeff))):
            tan_x += coeff[i] * x**(2*i + 1)
        return tan_x

    def ln_series(self, x, n):
        if x <= -1:
            raise ValueError(
                "Taylor series for ln(1 + x) is not defined for x <= -1.")

        ln_x = 0
        for i in range(1, n + 1):
            ln_x += ((-1)**(i + 1)) * (x**i) / i
        return ln_x


def plot_taylor_series():
    taylor = TaylorSeries()
    x_values = np.linspace(-1, 2, 100)  # Rango de valores de x
    n_terms = 5  # Número de términos de la serie de Taylor

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))  # Crear subplots

    functions = [
        ("Exponential (e^x)", taylor.exponential_series, np.exp, x_values),
        ("Sine (sin x)", taylor.sin_series, np.sin,
         np.linspace(-2 * np.pi, 2 * np.pi, 100)),
        ("Cosine (cos x)", taylor.cos_series, np.cos,
         np.linspace(-2 * np.pi, 2 * np.pi, 100)),
        ("Tangent (tan x)", taylor.tan_series, np.tan,
         np.linspace(-np.pi / 3, np.pi / 3, 100)),
        ("Natural Log (ln(1+x))", taylor.ln_series,
         np.log1p, np.linspace(-0.9, 1, 100)),
    ]

    for i, (title, taylor_func, real_func, x_vals) in enumerate(functions):
        row, col = divmod(i, 3)  # Ubicación en la cuadrícula de subplots
        y_taylor = np.array([taylor_func(x, n_terms) for x in x_vals])
        y_real = real_func(x_vals)
        error_abs = np.abs(y_real - y_taylor)

        axs[row, col].plot(x_vals, y_real, label="Real Function (python methods)",
                           linestyle="dashed", color="blue")
        axs[row, col].plot(
            x_vals, y_taylor, label=f"Taylor Series (n={n_terms}) (manual Function)", color="red")
        axs[row, col].plot(
            x_vals, error_abs, label="Absolute Error", color="green", linestyle="dotted")

        axs[row, col].set_title(title)
        axs[row, col].legend()
        axs[row, col].grid()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_taylor_series()

