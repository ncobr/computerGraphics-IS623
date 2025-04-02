import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, filedialog, Scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageViewerUi(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.parent.title("Image viewer")
        self.parent.geometry("1000x700")
