import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

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

# Setup comum
labels = metrics
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Fechar o radar

# Criar diretório para salvar os gráficos (opcional)
output_dir = "radar_charts"
os.makedirs(output_dir, exist_ok=True)

# Gerar um gráfico para cada cenário
for i, scenario in enumerate(scenarios):
    values1 = alg1_norm[i].tolist()
    values2 = alg2_norm[i].tolist()
    values1 += values1[:1]
    values2 += values2[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Plotar os dois algoritmos
    ax.plot(angles, values1, label="Greedy Randomized", linestyle='solid', color='tab:blue')
    ax.fill(angles, values1, color='tab:blue', alpha=0.25)

    ax.plot(angles, values2, label="ILP", linestyle='dashed', color='tab:orange')
    ax.fill(angles, values2, color='tab:orange', alpha=0.25)

    # Ajustes
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 1)

    ax.set_title(f"{scenario} - Comparação de Algoritmos", size=13, pad=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=9)

    # Salvar o gráfico
    filename = scenario.replace(" ", "_").replace("+", "plus").replace("B", "Bteam").replace("A", "Ateam")
    filepath = os.path.join(output_dir, f"radar_{filename}.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

print(f"Gráficos salvos em: {output_dir}/")
