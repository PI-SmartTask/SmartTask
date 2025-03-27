import copy
import random
import csv

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains.copy()
        self.constraints = constraints

    def check_constraints(self, var, value, assignment):
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        for constraint in self.constraints:
            if not constraint(var, temp_assignment):
                return False
        return True

    def propagate(self, domains, var, value):
        temp_assignment = {v: domains[v][0] if len(domains[v]) == 1 else None for v in self.variables}
        temp_assignment[var] = value

        for v in self.variables:
            if temp_assignment[v] is None:
                new_domain = []
                for val in domains[v]:
                    if self.check_constraints(v, val, temp_assignment):
                        new_domain.append(val)
                if not new_domain:
                    return False
                domains[v] = new_domain
        return True

    def select_variable(self, domains):
        unassigned_vars = [v for v in domains if len(domains[v]) > 1]
        return min(unassigned_vars, key=lambda var: len(domains[var]))

    def search(self, domains=None):
        if domains is None:
            domains = copy.deepcopy(self.domains)

        if any(len(lv) == 0 for lv in domains.values()):
            return None

        if all(len(lv) == 1 for lv in domains.values()):
            assignment = {v: lv[0] for v, lv in domains.items()}
            violations = [not self.check_constraints(var, assignment[var], assignment) for var in assignment]
            return {"assignment": assignment, "violations": violations}

        var = self.select_variable(domains)

        for val in domains[var]:
            new_domains = copy.deepcopy(domains)
            new_domains[var] = [val]
            if self.propagate(new_domains, var, val):
                solution = self.search(new_domains)
                if solution is not None:
                    return solution
        return None


def enforce_morning_afternoon_combination(assignment, num_days, num_employees):
    """Garante que em certos dias haja pelo menos um M e um T nos turnos de manhã e tarde."""
    specific_days = random.sample(range(1, num_days + 1), k=5)  # Selecionar 5 dias aleatórios
    for day in specific_days:
        morning_employees = [f"E{e}_{day}" for e in range(1, num_employees + 1) if assignment[f"E{e}_{day}"] == "M"]
        afternoon_employees = [f"E{e}_{day}" for e in range(1, num_employees + 1) if assignment[f"E{e}_{day}"] == "T"]

        if not morning_employees or not afternoon_employees:
            # Ajustar aleatoriamente um funcionário para garantir combinação M e T
            if not morning_employees and afternoon_employees:
                random.choice(afternoon_employees).replace("T", "M")
            elif not afternoon_employees and morning_employees:
                random.choice(morning_employees).replace("M", "T")
def balance_shifts_per_day(assignment, num_employees, num_days):
    """Balanceia os turnos para garantir uma melhor distribuição entre M e T em cada dia."""
    for day in range(1, num_days + 1):
        morning_count = sum(1 for e in range(1, num_employees + 1) if assignment[f"E{e}_{day}"] == "M")
        afternoon_count = sum(1 for e in range(1, num_employees + 1) if assignment[f"E{e}_{day}"] == "T")

        # Balanceamento: se há mais turnos de manhã que tarde, troque alguns M por T
        if morning_count > afternoon_count:
            for e in range(1, num_employees + 1):
                if assignment[f"E{e}_{day}"] == "M":
                    assignment[f"E{e}_{day}"] = "T"
                    break  # Ajuste apenas um por loop para balancear gradualmente

        # Se há dias com 100% M, tente garantir pelo menos 1 turno T
        if all(assignment[f"E{e}_{day}"] == "M" for e in range(1, num_employees + 1)):
            random_employee = random.choice([e for e in range(1, num_employees + 1)])
            assignment[f"E{random_employee}_{day}"] = "T"

    return assignment


def fill_last_days(assignment, num_employees, num_days):
    """Garante que os últimos dias tenham turnos alocados e evita sequências inválidas."""
    for day in range(num_days - 3, num_days + 1):  # Últimos 3 dias do mês
        employees_working = [assignment.get(f"E{e}_{day}", None) for e in range(1, num_employees + 1)]

        if all(shift == "0" or shift == "F" for shift in employees_working):
            # Se ninguém está trabalhando nesse dia, escalar funcionários alternando turnos M e T
            for e in range(1, num_employees + 1):
                prev_shift = assignment.get(f"E{e}_{day - 1}", None)
                # Evitar T -> M
                if prev_shift == "T":
                    assignment[f"E{e}_{day}"] = random.choice(["T", "F", "0"])
                else:
                    assignment[f"E{e}_{day}"] = random.choice(["M", "T"])

    return assignment


def enforce_shift_sequence_constraints(assignment, num_employees, num_days):
    """Corrige sequências inválidas T -> M, garantindo conformidade com a restrição."""
    for e in range(1, num_employees + 1):
        for day in range(1, num_days):
            current_shift = assignment[f"E{e}_{day}"]
            next_shift = assignment.get(f"E{e}_{day + 1}", None)

            # Se houver uma sequência T -> M, corrigir o próximo turno
            if current_shift == "T" and next_shift == "M":
                # Forçar o próximo turno a ser "T", "F" ou "0" para evitar T -> M
                assignment[f"E{e}_{day + 1}"] = random.choice(["T", "F", "0"])

    return assignment
def employee_scheduling():
    num_employees = 7
    num_days = 30
    holidays = {7, 14, 21, 28}
    employees = [f"E{e}" for e in range(1, num_employees + 1)]
    vacations = {emp: set(random.sample(range(1, num_days + 1), 5)) for emp in employees}

    variables = [f"E{e}_{d}" for e in range(1, num_employees + 1) for d in range(1, num_days + 1)]
    domains = {var: ["F"] if int(var.split('_')[1]) in vacations[var.split('_')[0]] else ["M", "T", "0"]
               for var in variables}

    constraints = [
        lambda var, assignment: not any(
            assignment.get(var, "0") == "T" and
            assignment.get(f"{var.split('_')[0]}_{int(var.split('_')[1]) - 1}", "0") == "M"
            for var in variables if int(var.split('_')[1]) > 1
        ),
        lambda var, assignment: not any(
            all(assignment.get(f"{var.split('_')[0]}_{d - k}", "0") in ["M", "T"] for k in range(5))
            for d in range(5, num_days + 1) if var == f"{var.split('_')[0]}_{d}"
        ),
        lambda var, assignment: all(
            sum(1 for d in range(1, num_days + 1) if assignment.get(f"E{e}_{d}", "0") in ["M", "T"]) <= 20
            for e in range(1, num_employees + 1)
        ),
        lambda var, assignment: not any(
            assignment.get(var, "0") == "M" and
            assignment.get(f"{var.split('_')[0]}_{int(var.split('_')[1]) + 1}", "0") == "T"
            for var in variables if int(var.split('_')[1]) < num_days
        ),
    ]

    csp = CSP(variables, domains, constraints)
    solution = csp.search()
    if solution:
        assignment = solution["assignment"]

        # Balancear turnos por funcionário e por dia
        assignment = balance_shifts_per_day(assignment, num_employees, num_days)
        assignment = enforce_shift_sequence_constraints(assignment, num_employees, num_days)
        assignment = fill_last_days(assignment, num_employees, num_days)
        print("Solução encontrada:")
        for var, val in assignment.items():
            print(f"{var}: {val}")
        generate_calendar(assignment, num_employees, num_days)
    else:
        print("Nenhuma solução encontrada.")


def generate_calendar(assignment, num_employees, num_days):
    days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    print("\nCalendário:")
    print(" ".join(f"{day:2}" for day in range(1, num_days + 1)))
    print(" ".join(f"{days_of_week[(day - 1) % 7]:3}" for day in range(1, num_days + 1)))

    with open("calendario_turnos.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([str(day) for day in range(1, num_days + 1)])
        csvwriter.writerow([days_of_week[(day - 1) % 7] for day in range(1, num_days + 1)])

        for e in range(1, num_employees + 1):
            employee_schedule = [assignment.get(f"E{e}_{d}", "-") for d in range(1, num_days + 1)]
            print(f"E{e}: " + " ".join(f"{shift:2}" for shift in employee_schedule))
            csvwriter.writerow([f"E{e}"] + employee_schedule)


if __name__ == "__main__":
    employee_scheduling()
