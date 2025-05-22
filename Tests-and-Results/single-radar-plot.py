import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Dados brutos
scenarios = ["Normal", "+2 B", "+4 B", "+4 B +2 A"]
metrics = ["Execution time", "Minimuns left", "Shift balance"]

# Dados dos dois algoritmos: [Exec time, Minimuns left, Shift balance]
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

# Combinar todos os dados para normalização
combined = np.array(alg1_data + alg2_data)
scaler = MinMaxScaler()
normalized = scaler.fit_transform(combined)

# Separar os dados normalizados
alg1_norm = normalized[:4]
alg2_norm = normalized[4:]

# Setup do radar
labels = metrics
num_vars = len(labels)

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Fechar o radar

# Criar o gráfico
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Cores para os cenários
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

for i in range(4):
    values1 = alg1_norm[i].tolist()
    values2 = alg2_norm[i].tolist()
    values1 += values1[:1]
    values2 += values2[:1]

    ax.plot(angles, values1, label=f"Alg1 - {scenarios[i]}", linestyle='solid', color=colors[i])
    ax.plot(angles, values2, label=f"Alg2 - {scenarios[i]}", linestyle='dashed', color=colors[i])

# Ajustes visuais
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_ylim(0, 1)

# Título e legenda
plt.title("Radar Chart - Comparação dos Algoritmos por Métrica e Cenário", size=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)

plt.tight_layout()
plt.show()
