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


def calculate_dissat(vars) -> np.ndarray:
    shift_working: np.ndarray = vars.x.sum(axis=(2, 3))
    shift_working = (shift_working + 0.2).astype(int)
    dissat = shift_working@shift_dissat
    return dissat.flatten()
