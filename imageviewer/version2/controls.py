import tkinter as tk
from tkinter import Frame, Scale, messagebox, filedialog, ttk
from layout import setup_layout


def setup_file_controls(self):
    self.file_section = Frame(self.control_frame, bg="#e0e0e0")
    self.file_section.pack(fill="x", pady=5)

    self.file_label = tk.Label(
        self.file_section, text="Archivo:", bg="#e0e0e0", font=('Arial', 10, 'bold'))
    self.file_label.pack(anchor="w", padx=5, pady=5)

    self.file_separator = Frame(self.file_section, height=2, bg="#b0b0b0")
    self.file_separator.pack(fill="x", padx=5, pady=2)

    # Botones de archivo
    self.file_buttons_frame = Frame(self.file_section, bg="#e0e0e0")
    self.file_buttons_frame.pack(fill="x", padx=5, pady=5)

    self.open_btn = tk.Button(
        self.file_buttons_frame, text="Explorar", width=10)
    self.open_btn.pack(side="left", padx=5)


def setup_controls(self):
    setup_file_controls(self)
