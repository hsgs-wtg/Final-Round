import numpy as np
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path

from consts import SHIFTS, JOBS
from dataset import Dataset

from constraints import resolve_constraints

data = None

def load_input():
    # Modify data
    global data
    data = Dataset("duLieu1")

    print(data.names)
    print(data.skills)

def main():
    load_input()
    return

    model = gp.Model("job_scheduling_01")
    
    vars = model.addMVar(shape = (data.workers_count, SHIFTS, JOBS), vtype = GRB.BINARY)
    resolve_constraints(model, vars, data)

if __name__ == "__main__":
    main()
