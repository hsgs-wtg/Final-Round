import numpy as np
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path

from consts import SHIFTS, JOBS
from dataset import Dataset

from constraints import resolve_constraints
from objective import add_objective_func

data = None

def load_input():
    # Modify data
    global data
    data = Dataset("duLieu1")

    print(data.names)
    print(data.skills)
    print(data.shift_time)

def main():
    load_input()

    model = gp.Model("job_scheduling_01")
    
    vars = model.addMVar(shape = (data.workers_count, SHIFTS, data.pipeline, JOBS), vtype = GRB.BINARY)
    resolve_constraints(model, vars, data)
    add_objective_func(model, vars, data)

    model.optimize()

if __name__ == "__main__":
    main()
