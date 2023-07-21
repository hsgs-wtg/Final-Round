import numpy as np
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path
import sys

from consts import SHIFTS, JOBS, JOBLIST, root_path
from dataset import Dataset

from constraints import resolve_constraints, constraint_cardinality
from objective import add_objective_func
from balance import optimize_delta, get_acceptance_function

data = None
vision = 1 # day(s)

def load_input(test, subtask):
    # Modify data
    global data
    data = Dataset(f"duLieu{test}", subtask)

def create_aux_vars(model, vars):
    hire_vars = model.addMVar(shape = (data.workers_count), vtype = GRB.BINARY)
    model.addConstr(hire_vars * 24 >= vars.sum(axis = (1, 2, 3)))
    return hire_vars

def run(model, vars, vars_auxiliary):
    r = 0
    D = vision * 3
    for shift in range(SHIFTS):
        print(f"Calculating for {shift = }")
        # Check if this is the last shift of the day
        if shift % 3 == 0:
            while r < shift + D and r < SHIFTS:
                # Load r
                constraint_cardinality(model, vars, data, r)
                r += 1

            # Process current shift
            model.optimize()

            # Check for error code
            if model.status == GRB.INFEASIBLE:
                print("Solution not found")
                exit(0)

        acp = get_acceptance_function(model, vars, vars_auxiliary)    
        result = optimize_delta(model, vars, vars_auxiliary, acp)

        # Lock current choice
        model.addConstr(vars[:, shift, :, :] == (result[:, shift, :, :] + 0.2).astype(int))

def print_output(result, filename = "result.txt"):
    result.sort(key = lambda x: x[1])
    answers = []
    for assignment in result:
        person, shift, pipeline, job = assignment
        day, group = shift // 3, shift % 3
        answers.append(f"{day+1:02d}.06.2023 Ca_{group+1} V{person+1:02d} Day_chuyen_{pipeline+1} {JOBLIST[job]}")
    
    with open(Path(root_path / "result" / filename), "w+") as f:
        f.write("\n".join(answers))
        f.write("\n")

def usage():
    print("Usage: python src/main.py DATA SUBTASK [VISION]")
    print("DATA [1|2]: corresponding to duLieu1 and duLieu2")
    print("SUBTASK [a|b]: corresponding to subtask a and b")
    print("VISION [int]: number of days that can be see ahead")
    exit(0)

def main():
    if len(sys.argv) < 3:
        usage()

    try:
        test = sys.argv[1]
        subtask = sys.argv[2]
        if len(sys.argv) >= 4:
            global vision
            vision = int(sys.argv[3])
        assert test in ('1', '2')
        assert subtask in ('a', 'b')
    except:
        usage()

    load_input(test, subtask)

    env = gp.Env(empty = True)
    env.setParam('OutputFlag', 0)
    env.start()
    model = gp.Model(f"job_scheduling_{test}_{subtask}", env = env)

    vars = model.addMVar(shape = (data.workers_count, SHIFTS, data.pipeline, JOBS), vtype = GRB.BINARY)

    vars_auxiliary = create_aux_vars(model, vars)

    resolve_constraints(model, vars, data)
    add_objective_func(model, vars, vars_auxiliary, data)

    run(model, vars, vars_auxiliary)

    result = (vars.x + 0.2).astype(int).nonzero()
    result_zip = list(zip(*result))

    filename = f"result_data_{test}_part_{subtask}.txt"
    print_output(result_zip, filename)

    print(f"A solution is found (stored in {filename})")


if __name__ == "__main__":
    main()
