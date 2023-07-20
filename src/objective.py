import numpy as np
import gurobipy as gp

def add_hourly_wage(model, vars, data):
    hourly_wage = data.hourly_wage

    return vars.sum() * hourly_wage

def add_objective_func(model, vars, data):
    hourly_expr = add_hourly_wage(model, vars, data)

    model.setObjectiveN(hourly_expr, 0, weight = 1)
