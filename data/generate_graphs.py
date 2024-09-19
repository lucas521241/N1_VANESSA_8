# generate_graphs.py
import pandas as pd
import matplotlib.pyplot as plt

def plot_accuracy():
    df_accuracy = pd.read_csv('data/accuracy_data.csv')
    plt.figure(figsize=(10, 5))
    plt.plot(df_accuracy['Accuracy'], marker='o')
    plt.title('Acurácia do Modelo ao Longo do Tempo')
    plt.xlabel('Número de Treinamentos')
    plt.ylabel('Acurácia')
    plt.grid(True)
    plt.savefig('data/accuracy_plot.png')
    plt.show()

def plot_winner_distribution():
    df_results = pd.read_csv('data/results_data.csv')
    plt.figure(figsize=(10, 5))
    df_results['winner'].value_counts().plot(kind='bar')
    plt.title('Distribuição de Vitórias')
    plt.xlabel('Vencedor')
    plt.ylabel('Número de Vitórias')
    plt.grid(True)
    plt.savefig('data/winner_distribution.png')
    plt.show()

if __name__ == "__main__":
    plot_accuracy()
    plot_winner_distribution()
