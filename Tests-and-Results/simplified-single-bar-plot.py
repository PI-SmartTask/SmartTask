import matplotlib.pyplot as plt
import numpy as np
import os

# Dados brutos
scenarios = ["Normal", "+2 B", "+4 B", "+4 B +2 A"]
metrics = ["Minimuns left", "Shift balance"]  # só as duas métricas que você quer

alg1_data = [
    [1, 35, 48.54],
    [1, 16, 48.59],
    [1, 0, 48.04],
    [5, 2, 48.63]
]

alg2_data = [
    [2, 80, 49.22],
    [2, 24, 49.55],
    [5, 0, 48.15],
    [8, 0, 48.60]
]

# Criar diretório para salvar o gráfico
output_dir = "bar_charts"
os.makedirs(output_dir, exist_ok=True)

# Preparar dados para o gráfico (somente as colunas 1 e 2)
num_scenarios = len(scenarios)
num_metrics = len(metrics)  # agora 2

# Para organizar no eixo x: combina cenário + métrica
x_labels = []
for sc in scenarios:
    for mt in metrics:
        x_labels.append(f"{sc} - {mt}")

# Extrair só as colunas 1 e 2 dos dados
alg1_values = []
alg2_values = []
for i in range(num_scenarios):
    alg1_values.append(alg1_data[i][1])  # Minimuns left
    alg1_values.append(alg1_data[i][2])  # Shift balance
    alg2_values.append(alg2_data[i][1])
    alg2_values.append(alg2_data[i][2])

x = np.arange(len(x_labels))
width = 0.4

fig, ax = plt.subplots(figsize=(14, 6))  # largura menor pois são menos barras

bars1 = ax.bar(x - width/2, alg1_values, width, label='Greedy Randomized', color='tab:blue')
bars2 = ax.bar(x + width/2, alg2_values, width, label='ILP', color='tab:orange')

# Configurações do eixo x
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=45, ha='right')

# Eixos e título
ax.set_ylabel('Valor')
ax.set_title('Comparação dos Algoritmos (Minimuns left e Shift balance)')
ax.legend()

# Mostrar valores em cima das barras
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7)

plt.tight_layout()

# Salvar gráfico
filepath = os.path.join(output_dir, "minimuns_shift_balance_all_scenarios.png")
plt.savefig(filepath, dpi=300)
plt.close()

print(f"Gráfico salvo em: {filepath}")
