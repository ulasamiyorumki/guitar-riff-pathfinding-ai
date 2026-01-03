import tkinter as tk
from gui.app import GuitarAIApp

def main():
    root = tk.Tk()
    app = GuitarAIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()