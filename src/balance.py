import numpy as np
import gurobipy as gp
from gurobipy import GRB
from consts import SHIFTS


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
        shift_dissat = shift_dissat.reshape((SHIFTS, 1))
        return shift_dissat

    def __init__(self):
        self.shift_dissat = self.generate_dissat()

    def calculate_dissat(self, vars):
        dissat = vars.sum(axis=(2, 3))@self.shift_dissat
        return dissat

    # Vars can be a double array, or a GRBVar array
    @classmethod
    def exclude_dissat(dissat, vars_auxiliary):
        hired = (vars_auxiliary.x + 0.2).astype(int).nonzero()
        dissat_active = dissat[hired]
        return dissat_active, dissat_active.shape[0]

    def dissat_stats(self, schedule, vars_auxiliary):
        dissat = self.calculate_dissat(schedule)
        cr_dissat, cr_size = self.exclude_dissat(dissat, vars_auxiliary)
        avg_dissat = cr_dissat.sum() / cr_size
        return avg_dissat, cr_dissat.min(), cr_dissat.max()

    # Should have called model.optimize() first
    def optimize_delta(self, model, vars, vars_auxiliary, acp):
        dissat_functions = self.calculate_dissat(vars)
        last_accepted: np.ndarray = vars.x
        iteration = 0
        while True:
            iteration += 1
            print(f"{iteration = }")
            avg_dissat, min_dissat, max_dissat = self.dissat_stats(
                vars.x, vars_auxiliary)
            print(self.dissat_stats(vars.x, vars_auxiliary))
            delta = (max_dissat - min_dissat) * .9

            lb = avg_dissat - delta/2
            ub = avg_dissat + delta/2

            constr_lb = model.addConstr(dissat_functions >= lb)
            constr_ub = model.addConstr(dissat_functions <= ub)
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
    @classmethod
    def get_acceptance_function(model, vars, vars_auxiliary):
        cost = model.objVal
        max_allowed_cost = cost * 1.1

        def acp():
            return model.objVal <= max_allowed_cost
        return acp
