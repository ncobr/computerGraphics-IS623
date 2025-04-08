import tkinter as tk
import os
from tkinter import filedialog, Scale, messagebox, ttk, Frame
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from imageProcessor import ImageProcessor
from layout import setup_layout
from controls import setup_controls


class ImageViewerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de imagenes v2")
        self.root.geometry("1200x800")
        self.root.configure(background="#f0f0f0")

        self.current_image_path = ''
        self.second_image_path = ''
        self.original_image = None
        self.current_image = None
        self.second_image = None
        self.processor = ImageProcessor()

        setup_layout(self)
        setup_controls(self)
