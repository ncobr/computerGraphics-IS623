import tkinter as tk
import os
from tkinter import filedialog, Scale, messagebox, ttk, Frame


def setup_layout(self):
    self.image_frame = Frame(self.root, bg="#e0e0e0")
    self.image_frame.pack(side="left", fill="both",
                          expand=True, padx=10, pady=10)

    self.info_frame = Frame(self.image_frame, bg="#e0e0e0")
    self.info_frame.pack(side="top", fill="x")

    self.path_label = tk.Label(
        self.info_frame, text="Ruta: ", bg="#e0e0e0")
    self.path_label.pack(side="left", padx=5)

    self.path_entry = tk.Entry(self.info_frame, width=50)
    self.path_entry.pack(side="left", padx=5, fill="x", expand=True)

    self.image_container = Frame(self.image_frame, bg="#d0d0d0")
    self.image_container.pack(side="top", fill="both", expand=True, pady=5)

    self.image_label = tk.Label(self.image_container, bg="#d0d0d0")
    self.image_label.pack(pady=10)

    self.control_outer_frame = Frame(self.root, bg="#e0e0e0", width=300)
    self.control_outer_frame.pack(side="right", fill="y", padx=10, pady=10)
    self.control_outer_frame.pack_propagate(False)

    # Creamos un canvas con scrollbar para los controles
    self.control_canvas = tk.Canvas(
        self.control_outer_frame, bg="#e0e0e0")
    self.control_scrollbar = tk.Scrollbar(self.control_outer_frame, orient="vertical",
                                          command=self.control_canvas.yview)
    self.control_scrollbar.pack(side="right", fill="y")
    self.control_canvas.pack(side="left", fill="both", expand=True)
    self.control_canvas.configure(yscrollcommand=self.control_scrollbar.set)

    # Marco interior para todos los controles
    self.control_frame = Frame(self.control_canvas, bg="#e0e0e0")
    self.control_canvas.create_window(
        (0, 0), window=self.control_frame, anchor="nw")

    # Configurar el evento de redimensionamiento
    self.control_frame.bind("<Configure>", lambda e: self.control_canvas.configure(
        scrollregion=self.control_canvas.bbox("all")))
