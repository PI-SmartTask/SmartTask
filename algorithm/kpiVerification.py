import csv
import pandas as pd
import sys
import json

def analyze(file, holidays, teams):
    print(f"Analyzing file: {file}")
    df = pd.read_csv(file, encoding='ISO-8859-1')

    missed_work_days = 0
    missed_vacation_days = 0
    missed_team_min = 0
    workHolidays = 0
    consecutiveDays = 0
    total_morning = 0
    total_afternoon = 0
    total_tm_fails = 0
    single_team_violations = 0
    two_team_shift_distribution = {}

    holiday_cols = [f'Dia {d}' for d in holidays if f'Dia {d}' in df.columns]
    dia_cols = [col for col in df.columns if col.startswith("Dia ")]

    for _, row in df.iterrows():
        worked_days = sum(row[col] in ['M_A', 'T_A', 'M_B', 'T_B'] for col in dia_cols)
        print(f"Worked days: {worked_days}")
        vacation_days = sum(row[col] == 'F' for col in dia_cols)

        missed_work_days += abs(223 - worked_days)
        missed_vacation_days += abs(30 - vacation_days)

        numHolidays = sum(row[col] in ['M_A', 'T_A', 'M_B', 'T_B'] for col in holiday_cols)
        if numHolidays > 22:
            workHolidays += numHolidays - 22

        work_sequence = [
            1 if row[col] in ['M_A', 'T_A', 'M_B', 'T_B'] else 0
            for col in dia_cols
        ]

        streak = 0
        fails = 0
        for day in work_sequence:
            if day == 1:
                streak += 1
                if streak >= 6:
                    fails += 1
            else:
                streak = 0
        consecutiveDays += fails

        tm_fails = 0
        for i in range(len(dia_cols) - 1):
            today = row[dia_cols[i]]
            tomorrow = row[dia_cols[i + 1]]
            if today in ['T_A', 'T_B'] and tomorrow in ['M_A', 'M_B']:
                tm_fails += 1

        total_tm_fails += tm_fails

        emp_id = row['funcionario']
        allowed_teams = teams.get(emp_id, [])
        team_counts = {1: 0, 2: 0}

        for col in dia_cols:
            shift_val = row[col]
            if shift_val in ['M_A', 'T_A']:
                team = 1
            elif shift_val in ['M_B', 'T_B']:
                team = 2
            else:
                continue
            team_counts[team] += 1


        if len(allowed_teams) == 1:
            allowed_team = allowed_teams[0]
            other_team = 2 if allowed_team == 1 else 1
            if team_counts[other_team] > 0:
                single_team_violations += 1
        elif len(allowed_teams) == 2:
            morning_shifts = sum(row[col] in ['M_A', 'M_B'] for col in dia_cols)
            afternoon_shifts = sum(row[col] in ['T_A', 'T_B'] for col in dia_cols)
            two_team_shift_distribution[emp_id] = {
                "morningShifts": morning_shifts,
                "afternoonShifts": afternoon_shifts
            }

        total_morning += sum(row[col] in ['M_A', 'M_B'] for col in dia_cols)
        total_afternoon += sum(row[col] in ['T_A', 'T_B'] for col in dia_cols)

    total_shifts = total_morning + total_afternoon
    percentages = []
    if total_shifts > 0:
        morning_percentage = (total_morning / total_shifts) * 100
        afternoon_percentage = (total_afternoon / total_shifts) * 100
        percentages.append(min(morning_percentage, afternoon_percentage))

    shift_balance = min(percentages) if percentages else 0

    for col in dia_cols:
        M_A = sum(row[col] == 'M_A' for _, row in df.iterrows())
        T_A = sum(row[col] == 'T_A' for _, row in df.iterrows())
        M_B = sum(row[col] == 'M_B' for _, row in df.iterrows())
        T_B = sum(row[col] == 'T_B' for _, row in df.iterrows())
        if M_A < 2:
            missed_team_min += (2 - M_A)
        if T_A < 2:
            missed_team_min += (2 - T_A)
        if M_B < 1:
            missed_team_min += 1
        if T_B < 1:
            missed_team_min += 1

    return {
        "missedWorkDays": missed_work_days,
        "missedVacationDays": missed_vacation_days,
        "missedTeamMin": missed_team_min,
        "workHolidays": workHolidays,
        "consecutiveDays": consecutiveDays,
        "shiftBalance": round(shift_balance, 2),
        "tmFails": total_tm_fails,
        "singleTeamViolations": single_team_violations,
        "twoTeamShiftDistribution": two_team_shift_distribution,
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kpiVerification.py <file>")
        sys.exit(1)
    holidays = [1, 107, 109, 114, 121, 161, 170, 226, 276, 303, 333, 340, 357]
    file = sys.argv[1]
    teams = {
        1: [1], 2: [1], 3: [1], 4: [1],
        5: [1, 2], 6: [1, 2], 7: [1], 8: [1],
        9: [1], 10: [2], 11: [2, 1], 12: [2]
    }
    data = analyze(file, holidays, teams)

    print(json.dumps(data, indent=4))
