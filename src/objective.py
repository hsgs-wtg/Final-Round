import numpy as np
import gurobipy as gp
from gurobipy import GRB

from balance import shift_dissat

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
        # Create vars for delta
        vars_delta = model.addMVar(shape = (data.workers_count), vtype = GRB.CONTINUOUS)
        delta_min = model.addVar(vtype = GRB.CONTINUOUS)
        delta_max = model.addVar(vtype = GRB.CONTINUOUS)

        model.addConstr(vars.sum(axis = (2, 3)) @ shift_dissat == vars_delta)
        model.addGenConstrMin(delta_min, vars_delta.tolist())
        model.addGenConstrMax(delta_max, vars_delta.tolist())

        balance_expr = delta_max - delta_min

        weight_wage = 1
        weight_balance = 1

        model.setObjective(hourly_expr * weight_wage + balance_expr * weight_balance, GRB.MINIMIZE)
    else:
        model.setObjective(starting_expr + hourly_expr, GRB.MINIMIZE)
