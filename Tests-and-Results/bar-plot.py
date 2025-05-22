import matplotlib.pyplot as plt
import numpy as np
import os

# Dados brutos
scenarios = ["Normal", "+2 B", "+4 B", "+4 B +2 A"]
metrics = ["Execution time (s)", "Minimuns left", "Shift balance"]

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

# Criar diretório para salvar os gráficos
output_dir = "bar_charts"
os.makedirs(output_dir, exist_ok=True)

# Gerar gráfico de barras para cada cenário
for i, scenario in enumerate(scenarios):
    values1 = alg1_data[i]
    values2 = alg2_data[i]

    x = np.arange(len(metrics))  # posições das métricas
    width = 0.35  # largura das barras

    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(x - width/2, values1, width, label='Greedy Randomized', color='tab:blue')
    bars2 = ax.bar(x + width/2, values2, width, label='ILP', color='tab:orange')

    # Títulos e eixos
    ax.set_ylabel('Valor')
    ax.set_title(f'{scenario} - Comparação de Algoritmos (Valores Reais)')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()

    # Mostrar os valores acima das barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    # Salvar gráfico
    filename = scenario.replace(" ", "_").replace("+", "plus").replace("B", "Bteam").replace("A", "Ateam")
    filepath = os.path.join(output_dir, f"bar_real_{filename}.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

print(f"Gráficos salvos em: {output_dir}/")
