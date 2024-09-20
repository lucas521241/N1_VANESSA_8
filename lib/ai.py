import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TicTacToeAI:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.data = []
        self.X_train = None
        self.y_train = None

    def board_to_features(self, board):
        # Converter o tabuleiro para um formato numérico
        features = []
        for row in board:
            for cell in row:
                if cell == 'X':
                    features.append(1)
                elif cell == 'O':
                    features.append(-1)
                else:
                    features.append(0)
        return np.array(features)

    def collect_data(self, game_data):
        for board, move, player in game_data:
            self.data.append((self.board_to_features(board), move[0] * 3 + move[1]))

    def train_model(self):
        if not self.data:
            print("Nenhum dado coletado para treinar o modelo.")
            return
        X, y = zip(*self.data)
        X = np.array(X)
        y = np.array(y)
        self.X_train, X_test, self.y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(self.X_train, self.y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Acurácia do modelo: {accuracy}")

        # Salvar acurácia em um CSV
        accuracy_data = pd.DataFrame({'Accuracy': [accuracy]})
        if not os.path.exists('data'):
            os.makedirs('data')
        accuracy_data.to_csv('data/accuracy_data.csv', mode='a', header=not os.path.exists('data/accuracy_data.csv'), index=False)

        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(self.model, 'models/model.pkl')
        print("Modelo salvo em 'models/model.pkl'.")
        logging.info(f'Modelo treinado com acurácia de {accuracy}')

    def load_model(self):
        try:
            self.model = joblib.load('models/model.pkl')
            print("Modelo carregado de 'models/model.pkl'.")
        except FileNotFoundError:
            print("Arquivo 'models/model.pkl' não encontrado. Treine o modelo primeiro.")

    def predict_move(self, board):
        if not hasattr(self.model, "tree_"):
            raise ValueError("O modelo não foi treinado ainda. Treine o modelo antes de usá-lo.")
        features = self.board_to_features(board)
        move = self.model.predict([features])[0]
        logging.info(f'IA escolheu a posição {divmod(move, 3)} com base na árvore de decisão.')
        return divmod(move, 3)

    def visualize_tree(self):
        if self.model and self.X_train is not None:
            tree_rules = export_text(self.model, feature_names=[f'feature_{i}' for i in range(self.X_train.shape[1])])
            logging.info(f'Árvore de Decisão:\n{tree_rules}')
        else:
            logging.warning("Modelo não treinado ou dados de treinamento ausentes.")
