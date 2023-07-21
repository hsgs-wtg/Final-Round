import numpy as np
import gurobipy as gp
from gurobipy import GRB
from consts import SHIFTS


def generate_dissat() -> np.ndarray:
    shift_dissat = np.ones(shape=SHIFTS)

    def night_shift():
        shift_dissat[2::3] *= 1.5

    def weekend():
        # Saturday x1.1
        shift_dissat[6::21] *= 1.1
        shift_dissat[7::21] *= 1.1
        shift_dissat[8::21] *= 1.1
        # Sunday x1.7
        shift_dissat[9::21] *= 1.7
        shift_dissat[10::21] *= 1.7
        shift_dissat[11::21] *= 1.7

    night_shift()
    weekend()
    shift_dissat = shift_dissat.reshape((SHIFTS, 1))
    return shift_dissat


shift_dissat = generate_dissat()

# Vars can be a double array, or a GRBVar array


def calculate_dissat(vars):
    dissat = vars.sum(axis=(2, 3))@shift_dissat
    # print(f"{dissat=}")
    return dissat


def exclude_dissat(dissat, vars_auxiliary):
    hired = (vars_auxiliary.x + 0.2).astype(int).nonzero()
    dissat_active = dissat[hired]
    print("DEBUG:", vars_auxiliary.x, dissat_active)
    return dissat_active, dissat_active.shape[0]


def dissat_stats(schedule, vars_auxiliary):
    dissat = calculate_dissat(schedule)
    cr_dissat, cr_size = exclude_dissat(dissat, vars_auxiliary)
    avg_dissat = cr_dissat.sum() / cr_size
    return avg_dissat, cr_dissat.min(), cr_dissat.max()

# Should have called model.optimize() first
def optimize_delta(model, vars, vars_auxiliary, acp):
    dissat_functions = calculate_dissat(vars)
    last_accepted: np.ndarray = vars.x
    iteration = 0
    while True:
        iteration += 1
        print(f"{iteration = }")
        avg_dissat, min_dissat, max_dissat = dissat_stats(vars.x, vars_auxiliary)
        # print(dissat_stats(vars.x, vars_auxiliary))
        delta = (max_dissat - min_dissat) * .9

        lb = avg_dissat - delta/2
        ub = avg_dissat + delta/2

        hired = (vars_auxiliary.x + 0.2).astype(int)

        constr_lb = model.addConstr(dissat_functions >= lb * hired)
        constr_ub = model.addConstr(dissat_functions <= ub * hired)
        model.optimize()
        model.remove((constr_lb, constr_ub))

        if model.status != GRB.OPTIMAL:
            print(f"Broke due to {model.status = }, {delta = }")
            break
        if not acp():
            print(f"Broke due to not accepted, {delta = }")
            break
        if delta < 0.1:
            print(f"{delta = } is feasible")

        last_accepted = vars.x
    return last_accepted

# Should have called model.optimize() first
def get_acceptance_function(model, vars, vars_auxiliary):
    cost = model.ObjVal
    max_allowed_cost = cost * 1.1
    def acp():
        return model.ObjVal <= max_allowed_cost
    return acp
