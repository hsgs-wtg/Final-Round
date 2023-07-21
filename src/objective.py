import numpy as np
import gurobipy as gp
from gurobipy import GRB

def add_hourly_wage(model, vars, data):
    hourly_wage = data.hourly_wage

    return vars.sum() * hourly_wage

def add_constant_wage(model, vars, data):
    starting_wage = data.starting_wage

    return vars.sum() * starting_wage

def add_objective_func(model, vars, vars_aux, data):
    starting_expr = add_constant_wage(model, vars_aux, data)
    hourly_expr = add_hourly_wage(model, vars, data)

    if data.subtask == "a":
        pass
    else:
        model.setObjective(starting_expr + hourly_expr, GRB.MINIMIZE)
