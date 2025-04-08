from imageViewerUI import ImageViewerUI as ui
import tkinter as tk


def main():
    root = tk.Tk()
    app = ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
