import csv

import pulp
import pandas as pd
from datetime import date, timedelta
import holidays
import random
from tabulate import tabulate

def solve():
    # ==== PARÂMETROS BÁSICOS ====
    ano = 2025
    num_funcionarios = 12
    dias_ano = pd.date_range(start=f'{ano}-01-01', end=f'{ano}-12-31').to_list()
    funcionarios = list(range(num_funcionarios))
    turnos = [0, 1, 2]  # 0 = folga, 1 = manhã, 2 = tarde

    equipe_A = set(range(9))  # Funcionários 0 a 8
    equipe_B = set(range(9, 12))  # Funcionários 9 a 11

    # ==== FERIADOS NACIONAIS + DOMINGOS ====
    feriados = holidays.country_holidays("PT", years=[ano])
    domingos_feriados = [d for d in dias_ano if d.weekday() == 6 or d in feriados]
    is_domingos_feriados = {d: (d in domingos_feriados) for d in dias_ano}

    # ==== FÉRIAS ====
    ferias = {
        f: set(random.sample(dias_ano, 30))
        for f in funcionarios
    }

    # ==== VARIÁVEIS DE DECISÃO ====
    x = {
        f: {
            d: {
                t: pulp.LpVariable(f"x_{f}_{d.strftime('%Y%m%d')}_{t}", cat="Binary")
                for t in turnos
            }
            for d in dias_ano
        }
        for f in funcionarios
    }

    # ==== MODELO ====
    model = pulp.LpProblem("Escala_Trabalho", pulp.LpMinimize)

    # ==== FUNÇÃO OBJETIVO E COBERTURA MÍNIMA SUAVE POR TURNO/EQUIPE ====

    y = {}
    penalizacao_cobertura = []

    for d in dias_ano:
        for equipe, funcionarios_equipe, minimo in [
            ("A", equipe_A, 2), ("B", equipe_B, 1)
        ]:
            for turno_id, turno_nome in [(1, "manha"), (2, "tarde")]:
                var_name = f"y_{turno_nome}_{equipe}_{d.strftime('%Y%m%d')}"
                yvar = pulp.LpVariable(var_name, lowBound=0, cat="Integer")
                y[(turno_nome, equipe, d)] = yvar

                soma_turno = pulp.lpSum(x[f][d][turno_id] for f in funcionarios_equipe)

                # Restricão suave: permitir descumprimento com penalização
                model += (
                    soma_turno + yvar >= minimo,
                    f"minimo_suave_{turno_nome}_{equipe}_{d}"
                )

                fator = 20 if is_domingos_feriados[d] else 10
                penalizacao_cobertura.append(fator * yvar)

    # ==== FUNÇÃO OBJETIVO FINAL ====

    model += (
        pulp.lpSum(penalizacao_cobertura)
    ), "Funcao_objetivo"

    # ==== RESTRIÇÕES ====

    for f in funcionarios:
        for d in dias_ano:
            model += (pulp.lpSum(x[f][d][t] for t in turnos) == 1, f"um_turno_por_dia_{f}_{d}")

    for f in funcionarios:
        model += (pulp.lpSum(x[f][d][1] + x[f][d][2] for d in dias_ano) == 223, f"total_dias_trabalho_{f}")

    for f in funcionarios:
        model += (
            pulp.lpSum(x[f][d][1] + x[f][d][2] for d in domingos_feriados if d in x[f]) <= 22,
            f"limite_domingo_feriado_{f}"
        )

    for f in funcionarios:
        for i in range(len(dias_ano) - 5):
            dias_seq = dias_ano[i:i + 6]
            model += (
                pulp.lpSum(x[f][d][1] + x[f][d][2] for d in dias_seq) <= 5,
                f"limite_5_dias_seguidos_{f}_{dias_ano[i]}"
            )

    for f in funcionarios:
        for i in range(len(dias_ano) - 1):
            d = dias_ano[i]
            d_next = dias_ano[i + 1]
            model += (x[f][d][2] + x[f][d_next][1] <= 1, f"proibe_TM_{f}_{d}")

    for f in funcionarios:
        for d in ferias[f]:
            model += (x[f][d][0] == 1, f"ferias_folga_{f}_{d}")

    for d in dias_ano:
        model += (
            pulp.lpSum(x[f][d][1] + x[f][d][2] for f in funcionarios) >= 2,
            f"cobertura_minima_{d}"
        )

        model += (
            pulp.lpSum(x[f][d][1] for f in funcionarios) >= 2,
            f"minimo_manha_{d}"
        )
        model += (
            pulp.lpSum(x[f][d][2] for f in funcionarios) >= 2,
            f"minimo_tarde_{d}"
        )

    # ==== RESOLUÇÃO ====
    solver = pulp.PULP_CBC_CMD(msg=True, timeLimit=28800, gapRel=0.01)

    status = model.solve(solver)
    print(f"\nstatus : {status} ")

    # ==== EXPORTAÇÃO EM FORMATO LARGO ====

    def get_turno_com_equipa(f, d, turno_str):
        if turno_str == "F":
            if d in ferias[f]:
                return "F"  # Férias
            else:
                return "0"  # Folga

        esta_em_A = f in equipe_A
        esta_em_B = f in equipe_B

        if esta_em_A and not esta_em_B:
            return f"{turno_str}_A"
        elif esta_em_B and not esta_em_A:
            return f"{turno_str}_B"
        else:
            return turno_str  # fallback

    escala = {
        f: {
            d.strftime("%Y-%m-%d"): get_turno_com_equipa(
                f,
                d,
                {0: "F", 1: "M", 2: "T"}[max((t for t in turnos if pulp.value(x[f][d][t]) == 1), default=0)]
            )
            for d in dias_ano
        }
        for f in funcionarios
    }

    df = pd.DataFrame.from_dict(escala, orient="index")
    df.index.name = "funcionario"
    df.reset_index(inplace=True)
    df.to_csv("calendario4.csv", index=False)
    print("Escala exportada para calendario4.csv")


    # ==== VERIFICAÇÕES DE RESTRIÇÕES ====
    # Equipes (use listas, não sets)
    equipe_A = list(range(9))       # Funcionários 0 a 8
    equipe_B = list(range(9, 12))   # Funcionários 9 a 11

    verificacoes = []

    for f in funcionarios:
        escalaf = df[df["funcionario"] == f].drop(columns="funcionario").T
        escalaf.columns = ["turno"]
        escalaf["data"] = pd.to_datetime(escalaf.index)

        escalaf["trabalho"] = escalaf["turno"].str.startswith("M") | escalaf["turno"].str.startswith("T")
        escalaf["domingo_feriado"] = escalaf["data"].isin(domingos_feriados)

        # 1. Domingos e feriados trabalhados
        dom_fer = escalaf.query("trabalho & domingo_feriado").shape[0]

        # 2. Total de dias trabalhados
        total_trabalho = escalaf["trabalho"].sum()

        # 3. Maior sequência de trabalho
        escalaf["grupo"] = (escalaf["trabalho"] != escalaf["trabalho"].shift()).cumsum()
        grupos = escalaf.groupby("grupo")["trabalho"].agg(["first", "size"])
        max_consec = grupos.query("first == True")["size"].max()

        # 4. Transições T->M (qualquer equipe)
        turnos_seq = escalaf["turno"].tolist()
        transicoes_TM = sum(
            1 for i in range(len(turnos_seq) - 1)
            if turnos_seq[i].startswith("T") and turnos_seq[i + 1].startswith("M")
        )



        verificacoes.append([
            f,
            dom_fer,
            total_trabalho,
            max_consec,
            transicoes_TM
        ])

    # ==== TABELA NO TERMINAL ====
    headers = [
        "Funcionário",
        "Dom/Feriado Trabalhados",
        "Dias Trabalhados",
        "Máx Seq. Trabalho",
        "Transições T->M"
    ]

    print("\nResumo das verificações de restrições por funcionário:\n")
    print(tabulate(verificacoes, headers=headers, tablefmt="grid"))

    # ==== VERIFICAÇÃO FINAL: DIAS SEM NENHUMA COBERTURA (0 turnos) ====

    dias_sem_cobertura_total = []

    for d in dias_ano:
        data_str = d.strftime("%Y-%m-%d")
        dia_data = df.set_index("funcionario")[data_str]

        total_manha = dia_data.str.startswith("M").sum()
        total_tarde = dia_data.str.startswith("T").sum()

        if total_manha + total_tarde == 0:
            dias_sem_cobertura_total.append(data_str)

    print("\n🚨 Dias sem nenhuma cobertura (0 turnos manhã e tarde):\n")
    if dias_sem_cobertura_total:
        for dia in dias_sem_cobertura_total:
            print(f"  - {dia}")
    else:
        print("✅ Nenhum dia sem cobertura total.")


    # ==== VERIFICAÇÃO DE COBERTURA POR EQUIPE E TURNO (DETALHADO) ====

    falhas_cobertura_detalhadas = {
        "manha_A": [],
        "tarde_A": [],
        "manha_B": [],
        "tarde_B": []
    }

    for d in dias_ano:
        data_str = d.strftime("%Y-%m-%d")
        dia_data = df.set_index("funcionario")[data_str]

        turnos_A = dia_data.loc[equipe_A]
        turnos_B = dia_data.loc[equipe_B]

        manha_A = turnos_A.str.startswith("M").sum()
        tarde_A = turnos_A.str.startswith("T").sum()
        manha_B = turnos_B.str.startswith("M").sum()
        tarde_B = turnos_B.str.startswith("T").sum()

        if manha_A < 2:
            falhas_cobertura_detalhadas["manha_A"].append((data_str, manha_A))
        if tarde_A < 2:
            falhas_cobertura_detalhadas["tarde_A"].append((data_str, tarde_A))
        if manha_B < 1:
            falhas_cobertura_detalhadas["manha_B"].append((data_str, manha_B))
        if tarde_B < 1:
            falhas_cobertura_detalhadas["tarde_B"].append((data_str, tarde_B))

    # ==== RESUMO DAS FALHAS POR CATEGORIA ====

    print("\n🔍 Falhas específicas de cobertura mínima por equipe e turno:\n")

    for categoria, falhas in falhas_cobertura_detalhadas.items():
        print(f"{categoria}: {len(falhas)} dias")
        for data, valor in falhas[:5]:  # Exibe apenas os 5 primeiros casos como exemplo
            print(f"  - {data}: apenas {valor} turno(s)")
        if len(falhas) > 5:
            print("  ...")
        print()

    schedule = []
    with open('calendario4.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        for row in reader:
            schedule.append(row)
            # print(row)
    return schedule


if __name__ == "__main__":
    print(solve())

