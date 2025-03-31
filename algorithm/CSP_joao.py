import copy
import random
import csv
import time

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def check_constraints(self, var, value, assignment):
        temp_assignment = assignment.copy()
        temp_assignment[var] = value

        for constraint_key, constraint_func in self.constraints.items():
            if isinstance(constraint_key, tuple):
                v1, v2 = constraint_key
                if v1 in temp_assignment and v2 in temp_assignment:
                    val1 = temp_assignment[v1]
                    val2 = temp_assignment[v2]
                    if not constraint_func(val1, val2):
                        return False
            else:
                if not constraint_func(var, temp_assignment):
                    return False
        return True

    def propagate(self, domains, var, value):
        domains[var] = [value]
        queue = [(var, value)]
        while queue:
            curr_var, curr_val = queue.pop(0)
            for other_var in self.variables:
                if other_var == curr_var or len(domains[other_var]) == 1:
                    continue
                new_domain = []
                for val in domains[other_var]:
                    temp_assignment = {v: domains[v][0] if len(domains[v]) == 1 else None
                                       for v in self.variables}
                    temp_assignment[curr_var] = curr_val
                    temp_assignment[other_var] = val
                    if self.check_constraints(other_var, val, temp_assignment):
                        new_domain.append(val)
                if not new_domain:
                    return False
                if len(new_domain) < len(domains[other_var]):
                    domains[other_var] = new_domain
                    if len(new_domain) == 1:
                        queue.append((other_var, new_domain[0]))
        return True

    def select_variable(self, domains):
        unassigned_vars = [v for v in domains if len(domains[v]) > 1]
        if not unassigned_vars:
            return None
        return min(unassigned_vars, key=lambda var: len(domains[var]))

    def search(self, domains=None, timeout=300):  # 5-minute timeout
        start_time = time.time()
        if domains is None:
            domains = copy.deepcopy(self.domains)

        def timed_search(domains, depth=0):
            if time.time() - start_time > timeout:
                return None

            if any(len(lv) == 0 for lv in domains.values()):
                return None

            if all(len(lv) == 1 for lv in domains.values()):
                assignment = {v: lv[0] for v, lv in domains.items()}
                return {"assignment": assignment}

            var = self.select_variable(domains)
            if var is None:
                return None

            for val in domains[var]:
                new_domains = copy.deepcopy(domains)
                new_domains[var] = [val]
                if self.propagate(new_domains, var, val):
                    solution = timed_search(new_domains, depth + 1)
                    if solution is not None:
                        return solution
            return None

        return timed_search(domains)


def employee_scheduling():
    tic = time.time()
    num_employees = 12
    num_days = 365
    holidays = {1, 50, 100, 150, 200, 250, 300, 350}
    employees = [f"E{e}" for e in range(1, num_employees + 1)]
    vacations = {emp: set(random.sample(range(1, num_days + 1), 30)) for emp in employees}

    variables = [f"{emp}_{d}" for emp in employees for d in range(1, num_days + 1)]

    domains = {
        var: ["F"] if int(var.split('_')[1]) in vacations[var.split('_')[0]]
        else (["0"] if int(var.split('_')[1]) in holidays else random.sample(["M", "T", "0"], 3))
        for var in variables
    }

    constraints = {
        (v1, v2): (lambda x1, x2: not (x1 == "T" and x2 == "M"))
        for v1 in variables for v2 in variables
        if v1.split('_')[0] == v2.split('_')[0] and int(v1.split('_')[1]) + 1 == int(v2.split('_')[1])
    }

    csp = CSP(variables, domains, constraints)

    # Per-employee constraints
    for emp in employees:
        emp_vars = [f"{emp}_{d}" for d in range(1, num_days + 1)]
        for start in range(num_days - 5):
            window_vars = emp_vars[start:start + 6]
            handle_ho_constraint(csp, window_vars, lambda values: not all(v in ["M", "T"] for v in values))
        # Adjusted total shift limit for a year (e.g., 240 shifts, ~2/3 of days)
        handle_ho_constraint(csp, emp_vars, lambda values: values.count("M") + values.count("T") <= 223)
        handle_ho_constraint(csp, [var for var in emp_vars if int(var.split('_')[1]) in holidays],
                             lambda values: values.count("M") + values.count("T") <= 22) # No shifts on holidays

    # Per-day staffing constraints with feasibility check
    for day in range(1, num_days + 1):
        day_vars = [f"{emp}_{day}" for emp in employees]
        available = sum(1 for var in day_vars if "F" not in domains[var])  # Non-vacation employees
        if available >= 6:
            handle_ho_constraint(csp, day_vars, lambda values: values.count("M") >= 3 and values.count("T") >= 3)
        else:
            min_shifts = max(0, available // 2)  # Adjust based on available employees
            handle_ho_constraint(csp, day_vars, lambda values: values.count("M") >= min_shifts and values.count("T") >= min_shifts)

    solution = csp.search(timeout=300)  # 5-minute timeout
    if solution and solution["assignment"]:
        assignment = solution["assignment"]
        generate_calendar(assignment, num_employees, num_days)
        print(f"Solution found in {time.time() - tic:.2f} seconds.")
    else:
        print("No solution found within 5 minutes or constraints too restrictive.")


def handle_ho_constraint(csp, variables, constraint_func):
    def constraint(var, assignment):
        values = [assignment.get(v, None) for v in variables]
        if None in values:
            return True
        return constraint_func(values)

    constraint_key = f"multi_{'_'.join(variables)}"
    csp.constraints[constraint_key] = constraint


def generate_calendar(assignment, num_employees, num_days):
    with open("calendario_turnos.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([str(day) for day in range(1, num_days + 1)])

        for e in range(1, num_employees + 1):
            employee_schedule = [assignment.get(f"E{e}_{d}", "-") for d in range(1, num_days + 1)]
            csvwriter.writerow([f"E{e}"] + employee_schedule)
        
        # Verify per-day staffing
        for day in range(1, num_days + 1):
            day_assignments = [assignment.get(f"E{e}_{day}", "-") for e in range(1, num_employees + 1)]
            m_count = day_assignments.count("M")
            t_count = day_assignments.count("T")
            print(f"Day {day}: {m_count} morning shifts (M), {t_count} afternoon shifts (T)")


if __name__ == "__main__":
    employee_scheduling()