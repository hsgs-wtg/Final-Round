import numpy as np
from consts import SHIFTS

# Constraint 1: A person can only do jobs he knows

def constraint_suitable_jobs(model, vars, skills):
    model.addConstr(vars.sum(axis = 1) <= np.array(skills) * SHIFTS)
    
# Constraint 2: A person cannot work right after the night shift

def constraint_night_shift(model, vars):
    pass

# Constraint 3: A person can only do one shift in one day

def constraint_one_shift(model, vars):
    pass

# Constraint 4: A person can only work in 24 days

def constraint_24_days(model, vars):
    pass

# Resolve constraints

def resolve_constraints(model, vars, data):
    constraint_suitable_jobs(model, vars, data.skills)
    constraint_night_shift(model, vars)
    constraint_one_shift(model, vars)
    constraint_24_days(model, vars)
