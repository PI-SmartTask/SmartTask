import matplotlib.pyplot as plt
import numpy as np
import os

# Dados brutos
scenarios = ["Normal", "+2 B", "+4 B", "+4 B +2 A"]

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
output_dir = "lines_charts"
os.makedirs(output_dir, exist_ok=True)

# Extrair valores por métrica
alg1_time     = [row[0] for row in alg1_data]
alg1_minimuns = [row[1] for row in alg1_data]
alg1_balance  = [row[2] for row in alg1_data]

alg2_time     = [row[0] for row in alg2_data]
alg2_minimuns = [row[1] for row in alg2_data]
alg2_balance  = [row[2] for row in alg2_data]

x = np.arange(len(scenarios))

fig, ax = plt.subplots(figsize=(12, 6))

# Plotar linhas por métrica
ax.plot(x, alg1_time,     marker='o', label='Greedy - Execution time (s)', color='tab:green')
ax.plot(x, alg2_time,     marker='o', label='ILP - Execution time (s)',    color='darkgreen')

ax.plot(x, alg1_minimuns, marker='o', label='Greedy - Minimuns left',      color='tab:blue')
ax.plot(x, alg2_minimuns, marker='o', label='ILP - Minimuns left',         color='tab:cyan')

ax.plot(x, alg1_balance,  marker='o', label='Greedy - Shift balance',      color='tab:orange')
ax.plot(x, alg2_balance,  marker='o', label='ILP - Shift balance',         color='tab:red')

# Linhas de referência
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1.5, label='Ideal Shift Balance = 50')
ax.axhline(y=0,  color='purple', linestyle=':', linewidth=2, label='Ideal Minimuns Left = 0')

# Eixos e título
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.set_ylabel("Valor")
ax.set_title("Metrics comparison of Execution time, shift balance and minimuns left to be completed (Greedy vs ILP)")
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
ax.grid(True)

# Anotações nos pontos
for i in x:
    ax.annotate(f'{alg1_time[i]:.0f}',     (i, alg1_time[i]),     xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)
    ax.annotate(f'{alg2_time[i]:.0f}',     (i, alg2_time[i]),     xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)
    ax.annotate(f'{alg1_minimuns[i]:.0f}', (i, alg1_minimuns[i]), xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)
    ax.annotate(f'{alg2_minimuns[i]:.0f}', (i, alg2_minimuns[i]), xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)
    ax.annotate(f'{alg1_balance[i]:.2f}',  (i, alg1_balance[i]),  xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)
    ax.annotate(f'{alg2_balance[i]:.2f}',  (i, alg2_balance[i]),  xytext=(0, 5), textcoords="offset points", ha='center', fontsize=8)

plt.tight_layout()

# Salvar gráfico
filepath = os.path.join(output_dir, "lineplot_all_metrics_with_ref_lines.png")
plt.savefig(filepath, dpi=300)
plt.close()

print(f"Gráfico salvo em: {filepath}")
