import matplotlib.pyplot as plt
import numpy as np
import os

# Criar pasta de saída
output_dir = "scenario_bar_charts"
os.makedirs(output_dir, exist_ok=True)

# Algoritmos
algorithms = [
    "ILP",
    "Hill Climbing",
    "Greedy Randomized",
    "Greedy Rand. + HC"
]

# Dados por cenário (valores numéricos, porcentagens convertidas)
base_case_data = {
    "Minimuns": [80, 359, 47, 27],
    "Shift Balance": [30.94, 20.94, 41.05, 44.09],
    "Two Team Preference Level": [100, 0, 72.64, 61.68]
}

case_30_data = {
    "Minimuns": [376, 1015, 372, 362],
    "Shift Balance": [39.91, 33.23, 45.75, 45.11],
    "Two Team Preference Level": [100, 0, 62.18, 62.72]
}

def plot_minimuns():
    x = np.arange(len(algorithms))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, base_case_data["Minimuns"], width, label='Base Case', color='tab:blue')
    bars2 = ax.bar(x + width/2, case_30_data["Minimuns"], width, label='30 Employees', color='tab:orange')

    ax.set_ylabel("Minimuns")
    ax.set_title("Minimuns left to be covered per algorithm")
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y')

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    filepath = os.path.join(output_dir, "minimuns_barplot.png")
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"Gráfico salvo em: {filepath}")

def plot_shift_and_preference():
    x = np.arange(len(algorithms))
    width = 0.18

    fig, ax = plt.subplots(figsize=(12, 6))

    # Shift Balance
    ax.bar(x - 1.5*width, base_case_data["Shift Balance"], width, label='Shift Balance (Base)', color='tab:blue')
    ax.bar(x - 0.5*width, case_30_data["Shift Balance"], width, label='Shift Balance (30 Emp)', color='tab:cyan')

    # Team Preference
    ax.bar(x + 0.5*width, base_case_data["Two Team Preference Level"], width, label='Two Team Preference Level (Base)', color='tab:orange')
    ax.bar(x + 1.5*width, case_30_data["Two Team Preference Level"], width, label='Two Team Preference Level (30 Emp)', color='tab:red')

    # Linha de referência para Shift Balance ideal (50%)
    ax.axhline(y=50, color='red', linestyle='--', linewidth=1.5, label='Shift Balance Ideal (50%)')

    ax.set_ylabel("Percentual (%)")
    ax.set_title("Shift Balance e Two Team Preference Level per algorithm")
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y')

    # Mostrar valores
    all_data = [
        base_case_data["Shift Balance"],
        case_30_data["Shift Balance"],
        base_case_data["Two Team Preference Level"],
        case_30_data["Two Team Preference Level"]
    ]
    shifts = [-1.5*width, -0.5*width, 0.5*width, 1.5*width]
    colors = ['tab:blue', 'tab:cyan', 'tab:orange', 'tab:red']

    for values, shift, color in zip(all_data, shifts, colors):
        for i, val in enumerate(values):
            ax.annotate(f'{val:.1f}%',
                        xy=(x[i] + shift, val),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8,
                        color=color)

    plt.tight_layout()
    filepath = os.path.join(output_dir, "shift_team_barplot.png")
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"Gráfico salvo em: {filepath}")

# Gerar gráficos
plot_minimuns()
plot_shift_and_preference()
