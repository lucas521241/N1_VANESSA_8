import tkinter as tk
from lib.ai import TicTacToeAI
from main import TicTacToeGUI

def main():
    root = tk.Tk()
    root.title("Jogo da Velha - IA vs IA")
    ai = TicTacToeAI()
    TicTacToeGUI(root, ai, mode='AIvsAI')
    root.mainloop()

if __name__ == "__main__":
    main()
