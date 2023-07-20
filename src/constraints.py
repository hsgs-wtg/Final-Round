import numpy as np
from consts import SHIFTS

# Constraint 1: A person can only do jobs he knows

def constraint_suitable_jobs(model, vars, skills):
    model.addConstr(vars.sum(axis = 1) <= np.array(skills) * SHIFTS)
    
# Constraint 2: A person cannot work right after the night shift

def constraint_night_shift(model, vars):
    night_shifts = vars[:, 2:vars.shape[1]-1:3].sum(axis=-1)
    first_shifts = vars[:, 5::3].sum(axis=-1)
    model.addConstr(night_shifts + first_shifts <= 1)

# Constraint 3: A person can only do one shift in one day

def constraint_one_shift(model, vars):
    shifts1 = vars[:, 0::3].sum(axis=(-1, -2))
    shifts2 = vars[:, 1::3].sum(axis=(-1, -2))
    shifts3 = vars[:, 2::3].sum(axis=(-1, -2))
    model.addConstr(shifts1 + shifts2 + shifts3 <= 1)

# Constraint 4: A person can only work in 24 days

def constraint_24_days(model, vars):
    persons = vars.sum(axis=(2, 3))
    model.addConstr(persons <= 24)

# Resolve constraints

def resolve_constraints(model, vars, data):
    constraint_suitable_jobs(model, vars, data.skills)
    constraint_night_shift(model, vars)
    constraint_one_shift(model, vars)
    constraint_24_days(model, vars)
