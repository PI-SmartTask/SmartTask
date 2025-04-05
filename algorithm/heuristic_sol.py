import numpy as np
import time
import csv

# Definindo as preferências dos trabalhadores
Prefs = [
    [0], [0], [1], [1], [0, 1], [0, 1], [1], [0], [1], [0], [1], [1], [0, 1], [0, 1], [0, 1]
]

nTrabs = len(Prefs)  # Número de trabalhadores (baseado no número de preferências)
nDias = 365  # Número de dias no ano
nDiasFerias = 30  # Número de dias de férias por trabalhador
nDiasTrabalho = 223  # Número de dias de trabalho no ano
nDiasTrabalhoFDS = 22  # Número máximo de dias trabalhados nos finais de semana
nDiasSeguidos = 5  # Número máximo de dias seguidos de trabalho
nMinTrabs = 2  # Número mínimo de turnos que um trabalhador deve fazer
nMaxFolga = 142  # Número máximo de dias de folga
nTurnos = 2  # Número de turnos por dia (Manhã e Tarde)

# Inicializando matrizes de férias e finais de semana
Ferias = np.zeros((nTrabs, nDias), dtype=bool)  # Matriz indicando os dias de férias
fds = np.zeros((nTrabs, nDias), dtype=bool)  # Matriz indicando os dias de finais de semana
init = np.arange(0, nTrabs * 23, 23)[:, None] + np.arange(nDiasFerias)  # Dias de férias
Ferias[np.arange(nTrabs)[:, None], init] = True  # Marca os dias de férias na matriz
dias = np.where(~Ferias)  # Dias disponíveis para trabalho
fds[:, 3::7] = fds[:, 4::7] = True  # Marca os finais de semana (sexta e sábado) como dias de folga

# Gerar horários de trabalho, garantindo que cada trabalhador tenha 142 dias de folga
horario = np.zeros((nTrabs, nDias, nTurnos), dtype=int)
for i in range(nTrabs):
    dias_disponiveis = np.where(~Ferias[i])[0]
    trabalho_indices = np.random.choice(dias_disponiveis, nDiasTrabalho, replace=False)
    turnos = np.random.choice(nTurnos, len(trabalho_indices))
    horario[i, trabalho_indices, turnos] = 1


# Função para o critério 1 (Limite de dias seguidos de trabalho)
def criterio1(horario, nDiasSeguidos):
    f1 = np.zeros(horario.shape[0], dtype=int)
    for i in range(horario.shape[0]):
        seq = np.sum(horario[i], axis=1)
        count = 0
        for day in seq:
            if day == 1:
                count += 1
                if count >= nDiasSeguidos:
                    f1[i] += 1
            else:
                count = 0
    return f1


# Função para o critério 2 (Limite de dias de trabalho nos finais de semana)
def criterio2(horario, fds, nDiasTrabalhoFDS):
    return np.maximum(np.sum(np.sum(horario * fds[:, :, None], axis=1), axis=1) - nDiasTrabalhoFDS, 0)


# Função para o critério 3 (Número mínimo de turnos de trabalho)
def criterio3(horario, nMinTrabs):
    return np.sum(np.sum(horario, axis=(0, 2)) < nMinTrabs)


# Função para o critério 4 (Limite de folgas)
def criterio4(horario, nMaxFolga):
    folgas = nDias - np.sum(horario, axis=(1, 2))
    return np.abs(folgas - nMaxFolga)


# Função otimizada para o critério 5 (Proibição de "T_A" seguido de "M_A" ou "T_B" seguido de "M_B")
def criterio5(horario, Prefs):
    f5 = np.zeros(horario.shape[0], dtype=int)
    for i in range(horario.shape[0]):
        if 0 in Prefs[i] or 1 in Prefs[i]:
            for d in range(nDias - 1):
                # Para a equipe A: "T_A" seguido de "M_A" no próximo dia
                if 0 in Prefs[i]:
                    if horario[i, d, 1] == 1 and horario[i, d + 1, 0] == 1:
                        f5[i] += 1

                        # Para a equipe B: "T_B" seguido de "M_B" no próximo dia
                if 1 in Prefs[i]:
                    if horario[i, d, 1] == 1 and horario[i, d + 1, 0] == 1:
                        f5[i] += 1

    return f5


# Função para calcular todos os critérios de uma vez
def calcular_criterios(horario, fds, nDiasSeguidos, nDiasTrabalhoFDS, nMinTrabs, nMaxFolga):
    f1 = criterio1(horario, nDiasSeguidos)
    f2 = criterio2(horario, fds, nDiasTrabalhoFDS)
    f3 = criterio3(horario, nMinTrabs)
    f4 = criterio4(horario, nMaxFolga)
    f5 = criterio5(horario, Prefs)  # Calcular o novo critério
    return f1, f2, f3, f4, f5


# Função para identificar as equipes com base nas preferências
def identificar_equipes(Prefs):
    equipe_A = []
    equipe_B = []
    ambas = []

    for i, pref in enumerate(Prefs):
        if 0 in pref and 1 in pref:
            ambas.append(i)
        elif 0 in pref:
            equipe_A.append(i)
        elif 1 in pref:
            equipe_B.append(i)

    return equipe_A, equipe_B, ambas


# Função para salvar o calendário de turnos em um CSV
def salvar_csv(horario, Ferias, nTurnos, nDias, Prefs):
    with open("calendario_turnos.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Gera as linhas dos funcionários
        for e in range(nTrabs):
            employee_schedule = []
            equipe = 'A' if 0 in Prefs[e] else 'B' if 1 in Prefs[e] else 'Ambas'
            for d in range(nDias):
                shift = "Fe" if Ferias[e, d] else "0"
                if not Ferias[e, d]:
                    if horario[e, d, 0] == 1:
                        shift = f"M_{equipe}"
                    elif horario[e, d, 1] == 1:
                        shift = f"T_{equipe}"
                employee_schedule.append(shift)

            csvwriter.writerow([f"Empregado{e + 1}"] + employee_schedule)


start_time = time.time()
f1_opt, f2_opt, f3_opt, f4_opt, f5_opt = calcular_criterios(horario, fds, nDiasSeguidos, nDiasTrabalhoFDS, nMinTrabs,
                                                            nMaxFolga)

equipe_A, equipe_B, ambas = identificar_equipes(Prefs)

print("Trabalhadores na equipe A:", equipe_A)
print("Trabalhadores na equipe B:", equipe_B)
print("Trabalhadores nas equipes A e B:", ambas)


# Função para imprimir os resultados
def print_result(label, data):
    print(f"{label}:\n{data}\n")


print_result("Valores iniciais dos critérios 1, 2, 4 e 5", np.array([f1_opt, f2_opt, f4_opt, f5_opt]))

# Início da otimização
t, cont = 0, 0
while t < 240000 and (np.any(f1_opt) or np.any(f2_opt) or np.any(f4_opt) or np.any(f5_opt)):
    cont += 1
    i = np.random.randint(nTrabs)
    aux = np.random.choice(len(dias[1][dias[0] == i]), 2, replace=False)
    dia1, dia2 = dias[1][dias[0] == i][aux]
    turno1, turno2 = np.random.choice(nTurnos, 2, replace=False)

    pode_trabalhar_A = 0 in Prefs[i]
    pode_trabalhar_B = 1 in Prefs[i]

    if horario[i, dia1, turno1] != horario[i, dia2, turno2]:
        hor = horario.copy()
        if pode_trabalhar_A and pode_trabalhar_B:
            hor[i, dia1, turno1], hor[i, dia2, turno2] = hor[i, dia2, turno2], hor[i, dia1, turno1]
        elif pode_trabalhar_A:
            hor[i, dia1, turno1] = 1
            hor[i, dia2, turno2] = 0
        elif pode_trabalhar_B:
            hor[i, dia1, turno1] = 0
            hor[i, dia2, turno2] = 1

        f1, f2, f3, f4, f5 = calcular_criterios(hor, fds, nDiasSeguidos, nDiasTrabalhoFDS, nMinTrabs, nMaxFolga)

        if np.all(f1 == 0) and np.all(f2 == 0) and f3 == 0 and np.all(f4 == 0) and np.all(f5 == 0):
            f1_opt, f2_opt, f3_opt, f4_opt, f5_opt, horario = f1, f2, f3, f4, f5, hor
            print("\nSolução perfeita encontrada!")
            break

        if f1[i] + f2[i] + f3 + f4[i] + f5[i] < f1_opt[i] + f2_opt[i] + f3_opt + f4_opt[i] + f5_opt[i]:
            f1_opt[i], f2_opt[i], f3_opt, f4_opt[i], f5_opt[i], horario = f1[i], f2[i], f3, f4[i], f5[i], hor

    t += 1

execution_time = time.time() - start_time

print_result("Número de iterações realizadas", cont)
print_result("Valores finais dos critérios 1, 2, 4 e 5", np.array([f1_opt, f2_opt, f4_opt, f5_opt]))
print_result("Valor final do critério 3", f3_opt)
print(f"Tempo de execução: {execution_time:.2f} segundos")

salvar_csv(horario, Ferias, nTurnos, nDias, Prefs)