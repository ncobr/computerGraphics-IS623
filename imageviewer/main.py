import tkinter as tk
from gui.main_window import ImageViewerUi
from core.image_controller import ImageControl


def main():
    root = tk.Tk()
    controller = ImageControl()
    app = ImageViewerUi(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()
