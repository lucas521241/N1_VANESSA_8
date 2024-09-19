# main.py
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.game import TicTacToe
from lib.ai import TicTacToeAI
import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root, ai, mode):
        self.root = root
        self.ai = ai
        self.mode = mode
        self.game = TicTacToe()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player = 'X'  # Inicializa o jogador
        self.game_data = []
        self.game_count = 0  # Contador de jogos
        self.accuracy_data = []  # Dados de acurácia
        self.results_data = []  # Dados dos resultados
        self.create_board()
        if self.mode == 'AIvsAI':
            self.root.after(500, self.ai_vs_ai_game)  # Inicia o jogo IA vs IA

    def create_board(self):
        for r in range(3):
            for c in range(3):
                button = tk.Button(self.root, text=' ', font='normal 20 bold', height=2, width=5,
                                   command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button
        train_button = tk.Button(self.root, text='Treinar IA', font='normal 20 bold', height=2, width=10, command=self.train_ai)
        train_button.grid(row=3, column=1)
        reset_button = tk.Button(self.root, text='Reiniciar', font='normal 20 bold', height=2, width=10, command=self.reset_game)
        reset_button.grid(row=3, column=2)
        self.status_label = tk.Label(self.root, text=f"Partida: {self.game_count + 1}", font='normal 20 bold')
        self.status_label.grid(row=4, column=0, columnspan=3)
        self.message_label = tk.Label(self.root, text="", font='normal 20 bold')
        self.message_label.grid(row=5, column=0, columnspan=3)

    def on_click(self, r, c):
        if self.game.board[r][c] == ' ' and self.game.current_winner is None:
            self.game.make_move((r, c), self.player)
            self.buttons[r][c].config(text=self.player)
            self.game_data.append((self.game.board.copy(), (r, c), self.player))
            if self.game.current_winner:
                self.message_label.config(text=f"Jogador {self.player} venceu!")
                self.results_data.append({'game': self.game_count + 1, 'winner': self.player})
                self.root.after(1000, self.reset_game)
            elif not self.game.empty_squares():
                self.message_label.config(text="Empate!")
                self.results_data.append({'game': self.game_count + 1, 'winner': 'Draw'})
                self.root.after(1000, self.reset_game)
            else:
                self.player = 'O' if self.player == 'X' else 'X'
                if self.player == 'O' and self.game.empty_squares() and self.mode == 'AI':
                    self.root.after(500, self.ai_move)  # IA joga após 500ms

    def ai_move(self):
        move = self.ai.predict_move(self.game.board)
        while self.game.board[move[0]][move[1]] != ' ':
            move = (random.randint(0, 2), random.randint(0, 2))  # Randomiza se o movimento não for válido
        self.game.make_move(move, self.player)
        self.buttons[move[0]][move[1]].config(text=self.player)
        self.game_data.append((self.game.board.copy(), move, self.player))
        if self.game.current_winner:
            self.message_label.config(text=f"Jogador {self.player} venceu!")
            self.results_data.append({'game': self.game_count + 1, 'winner': self.player})
            self.root.after(1000, self.reset_game)
        elif not self.game.empty_squares():
            self.message_label.config(text="Empate!")
            self.results_data.append({'game': self.game_count + 1, 'winner': 'Draw'})
            self.root.after(1000, self.reset_game)
        else:
            self.player = 'X' if self.player == 'O' else 'O'
            if self.mode == 'AIvsAI':
                self.root.after(500, self.ai_vs_ai_game)

    def ai_vs_ai_game(self):
        if self.game.empty_squares() and self.game.current_winner is None:
            self.ai_move()
        else:
            if not self.game.current_winner:
                self.message_label.config(text="Empate!")
                self.results_data.append({'game': self.game_count + 1, 'winner': 'Draw'})
            self.reset_game()
            self.root.after(500, self.ai_vs_ai_game)  # Continua jogando infinitamente

    def train_ai(self):
        self.ai.collect_data(self.game_data)
        if not self.ai.data:
            print("Nenhum dado coletado para treinar o modelo.")
            return
        self.ai.train_model()
        self.accuracy_data.append(self.ai.model.score(self.ai.X_train, self.ai.y_train))
        self.save_data()

    def reset_game(self):
        self.game = TicTacToe()
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=' ')
        self.player = 'X'
        self.game_data = []
        self.game_count += 1
        self.status_label.config(text=f"Partida: {self.game_count + 1}")
        self.message_label.config(text="")
        if self.game_count % 100 == 0:
            self.train_ai()
        if self.mode == 'AIvsAI':
            self.root.after(500, self.ai_vs_ai_game)

    def save_data(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            print("Pasta 'data' criada.")
        
        print(f"Dados de acurácia: {self.accuracy_data}")
        if self.accuracy_data:
            df_accuracy = pd.DataFrame(self.accuracy_data, columns=['Accuracy'])
            df_accuracy.to_csv('data/accuracy_data.csv', index=False)
            print("Arquivo 'accuracy_data.csv' salvo com sucesso.")
        else:
            print("Nenhum dado de acurácia para salvar.")

        print(f"Dados de resultados: {self.results_data}")
        if self.results_data:
            df_results = pd.DataFrame(self.results_data)
            df_results.to_csv('data/results_data.csv', index=False)
            print("Arquivo 'results_data.csv' salvo com sucesso.")
        else:
            print("Nenhum dado de resultados para salvar.")
        
        self.plot_data()


    def plot_data(self):
        df_accuracy = pd.read_csv('data/accuracy_data.csv')
        df_results = pd.read_csv('data/results_data.csv')

        plt.figure(figsize=(10, 5))
        plt.plot(df_accuracy['Accuracy'], marker='o')
        plt.title('Acurácia do Modelo ao Longo do Tempo')
        plt.xlabel('Número de Treinamentos')
        plt.ylabel('Acurácia')
        plt.grid(True)
        plt.savefig('data/accuracy_plot.png')
        plt.show()

        plt.figure(figsize=(10, 5))
        df_results['winner'].value_counts().plot(kind='bar')
        plt.title('Distribuição de Vitórias')
        plt.xlabel('Vencedor')
        plt.ylabel('Número de Vitórias')
        plt.grid(True)
        plt.savefig('data/winner_distribution.png')
        plt.show()

class StartScreen:
    def __init__(self, root, ai):
        self.root = root
        self.ai = ai
        self.create_start_screen()

    def create_start_screen(self):
        tk.Label(self.root, text="Escolha o modo de jogo", font='normal 20 bold').pack(pady=20)
        tk.Button(self.root, text="Jogar contra Pessoa", font='normal 20 bold', command=self.start_human_game).pack(pady=10)
        tk.Button(self.root, text="Jogar contra IA", font='normal 20 bold', command=self.start_ai_game).pack(pady=10)
        tk.Button(self.root, text="IA vs IA", font='normal 20 bold', command=self.start_ai_vs_ai_game).pack(pady=10)

    def start_human_game(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("Jogo da Velha - Humano vs Humano")
        TicTacToeGUI(root, self.ai, mode='Human')
        root.mainloop()

    def start_ai_game(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("Jogo da Velha - Humano vs IA")
        TicTacToeGUI(root, self.ai, mode='AI')
        root.mainloop()

    def start_ai_vs_ai_game(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("Jogo da Velha - IA vs IA")
        TicTacToeGUI(root, self.ai, mode='AIvsAI')
        root.mainloop()

def main():
    ai = TicTacToeAI()
    try:
        ai.load_model()
    except:
        pass

    root = tk.Tk()
    root.title("Jogo da Velha")
    StartScreen(root, ai)
    root.mainloop()

if __name__ == "__main__":
    main()

