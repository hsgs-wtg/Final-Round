import numpy as np
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path

from consts import SHIFTS, JOBS, JOBLIST
from dataset import Dataset

from constraints import resolve_constraints, constraint_cardinality
from objective import add_objective_func

data = None

def load_input():
    # Modify data
    global data
    data = Dataset("duLieu1")

def create_aux_vars(model, vars):
    hire_vars = model.addMVar(shape = (data.workers_count), vtype = GRB.BINARY)
    
    model.addConstrs(hire_vars[i] == gp.or_(vars[i].reshape(-1).tolist()) for i in range(data.workers_count))

    return hire_vars

def run(model, vars):
    r = 0
    D = 3
    for shift in range(SHIFTS):
        # Check if this is the last shift of the day
        if shift % 3 == 0:
            while r < shift + D:
                # Load r
                constraint_cardinality(model, vars, data, r)
                r += 1

        # Process current shift
        model.optimize()

        # Lock current choice
        model.addConstr(vars[:, shift, :, :] == vars.x[:, shift, :, :])

def print_output(result):
    for assignment in result:
        person, shift, pipeline, job = assignment
        day, group = shift // 3, shift % 3
        print(f"{day+1:02d}.06.2023 Ca_{group+1} V{person+1:02d} Day_chuyen_{pipeline+1} {JOBLIST[job]}")
    
def main():
    load_input()

    env = gp.Env(empty = True)
    env.setParam('OutputFlag', 0)
    env.start()
    model = gp.Model("job_scheduling_01", env = env)
    
    vars = model.addMVar(shape = (data.workers_count, SHIFTS, data.pipeline, JOBS), vtype = GRB.BINARY)

    vars_auxiliary = create_aux_vars(model, vars)

    resolve_constraints(model, vars, data)
    add_objective_func(model, vars, vars_auxiliary, data)

    run(model, vars)

    result = (vars.x + 0.2).astype(int).nonzero()
    result_zip = list(zip(*result))

    print_output(result_zip)


if __name__ == "__main__":
    main()
