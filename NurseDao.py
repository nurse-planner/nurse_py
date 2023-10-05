from ortools.linear_solver import pywraplp
from NurseDto import NurseDto
from Result import Result
from datetime import date, timedelta
import json


def nurse_scheduling(nurseDto: NurseDto):
    convert = {0: "D", 1: "E", 2: "N"}
    totalNurse = nurseDto.chargeNurses + nurseDto.actNurses
    NUM_NURSES = len(nurseDto.chargeNurses) + len(nurseDto.actNurses)
    NUM_DAYS = nurseDto.day
    NUM_SHIFTS = nurseDto.shifts
    MIN_NURSES_PER_SHIFT = 3
    NUM_OFF = max(NUM_NURSES * 0.25, MIN_NURSES_PER_SHIFT)
    START_DATE = nurseDto.startDate
    year, month, days = map(int, START_DATE.split("-"))
    START_DATE = date(year, month, days)
    calendar = [list() for _ in range(NUM_DAYS)]
    for k in range(len(totalNurse)):
        day = totalNurse[k]["off"]
        for d in day:
            calendar[d].append(k)

    experience = [totalNurse[i]["workingYear"] for i in range(len(totalNurse))]

    # Create a solver
    solver = pywraplp.Solver.CreateSolver("GLOP")

    x = {}
    for i in range(NUM_DAYS):
        for j in range(NUM_SHIFTS):
            for k in range(NUM_NURSES):
                x[i, j, k] = solver.IntVar(0, 1, f"x[{i},{j},{k}]")

    for i in range(NUM_DAYS):
        for j in range(NUM_SHIFTS):
            solver.Add(
                sum(x[i, j, k] for k in range(NUM_NURSES)) == MIN_NURSES_PER_SHIFT
            )

    for i in range(NUM_DAYS):
        for k in range(NUM_NURSES):
            solver.Add(sum(x[i, j, k] for j in range(NUM_SHIFTS)) <= 1)

    target_shifts_per_nurse = MIN_NURSES_PER_SHIFT * NUM_SHIFTS * NUM_DAYS / NUM_NURSES


    for i in range(1, NUM_DAYS):
        for k in range(NUM_NURSES):
            solver.Add(x[i, 2, k] + x[i - 1, 2, k] <= 1)
            solver.Add(x[i, 2, k] + x[i - 1, 0, k] <= 1)


    for d in range(NUM_DAYS):
        print("정렬 전 : ", [totalNurse[i]["id"] for i in calendar[d]])
        calendar[d].sort(key = lambda x: totalNurse[x]["workingYear"], reverse=True)
        print("정렬 후 : ", [totalNurse[i]["id"] for i in calendar[d]])
        for p in range(min(len(calendar[d]), 1)):
            k = calendar[d][p]
            solver.Add(sum(x[d, j, k] for j in range(NUM_SHIFTS)) == 0)
        
    

    shift_variation = 0.0
    for k in range(NUM_NURSES):
        # solver.Add(
        #     sum(x[i, j, k] for i in range(NUM_DAYS) for j in range(NUM_SHIFTS))
        #     <= target_shifts_per_nurse * (1 + shift_variation)
        # )
        solver.Add(
            sum(x[i, j, k] for i in range(NUM_DAYS) for j in range(NUM_SHIFTS))
            >= target_shifts_per_nurse * (1 - shift_variation)
        )



    objective = solver.Objective()
    objective.SetMinimization()

    # Solve the problem
    solver.Solve()

    # Print the schedule
    if solver.Solve() == pywraplp.Solver.OPTIMAL:
        for k in range(NUM_NURSES):
            print("간호사가 원하는 휴일 : ", totalNurse[k]["off"])
            cnt = 0
            notWantedCnt = 0
            for i in range(NUM_DAYS):
                for j in range(NUM_SHIFTS):
                    if x[i, j, k].solution_value() == 1:
                        cnt += 1
                        if(i in totalNurse[k]["off"]):
                           notWantedCnt += 1
                        print(f"간호사 {k}는 {i}일에 {convert[j]}당직을 섰습니다.")
            print(f"간호사 {k}의 총 근무 횟수 : ", cnt)
            print(f"간호사 {k}가 원하지 않는 날 당직을 선 회수 {notWantedCnt}/{len(totalNurse[k]['off'])}")
            print()

        rs = []
        for k in range(NUM_NURSES):
            work = dict()
            for i in range(NUM_DAYS):
                work[f"{START_DATE + timedelta(days=i)}"] = ""

                for j in range(NUM_SHIFTS):
                    if x[i, j, k].solution_value() == 1:
                        work[f"{START_DATE + timedelta(days=i)}"] = convert[j]
            rs.append(Result(totalNurse[k]["id"], work).to_dict())

        nurses_json = json.dumps(rs)
        return nurses_json

    solver = None
    # 종료
    return "No Solution"
