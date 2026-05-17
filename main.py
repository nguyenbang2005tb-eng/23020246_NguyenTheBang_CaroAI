import tkinter as tk
from gui import CaroGUI


def main():
    root = tk.Tk()

    root.title("Caro AI - Minimax vs Alpha-Beta")

    # Tăng kích thước để chứa chế độ so sánh 2 bàn cờ
    root.geometry("1300x820")
    root.minsize(1000, 760)
    root.resizable(True, True)

    app = CaroGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()