import numpy as np
import gurobipy as gp
from gurobipy import GRB
from consts import SHIFTS

def exclude_dissat(dissat, vars_auxiliary):
    # hired = (vars_auxiliary.x + 0.2).astype(int).nonzero()
    dissat_active = dissat
    return dissat_active, dissat_active.shape[0]

def get_acceptance_function(model, vars, vars_auxiliary):
    cost = model.objVal
    max_allowed_cost = cost * 1.1

    def acp():
        return model.objVal <= max_allowed_cost
    return acp


class BalanceUnweighted:
    @staticmethod
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
        shift_dissat = shift_dissat.reshape((-1, 1))
        return shift_dissat

    def __init__(self):
        self.shift_dissat = self.generate_dissat()

    def calculate_dissat(self, vars):
        dissat = vars.sum(axis=(2, 3))@self.shift_dissat
        return dissat.flatten()

    def dissat_stats(self, schedule, vars_auxiliary):
        dissat = self.calculate_dissat(schedule)
        cr_dissat, cr_size = exclude_dissat(dissat, vars_auxiliary)
        avg_dissat = cr_dissat.sum() / cr_size
        return avg_dissat, cr_dissat.min(), cr_dissat.max()
