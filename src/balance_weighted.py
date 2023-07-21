import numpy as np
import balance


class BalanceWeighted:
    # shift+pipeline
    @staticmethod
    def generate_dissat_weighted(data):
        # shift
        shift_dissat = balance.BalanceUnweighted().shift_dissat.flatten()
        # pipeline | shift
        shift_time = data.shift_time
        # pipeline | shift
        result = (shift_time + 2) * shift_dissat
        # shift | pipeline
        result = result.transpose((1, 0))
        # shift+pipeline
        result = result.reshape((-1, 1))
        return result

    def __init__(self, data):
        self.shift_pl_dissat = self.generate_dissat_weighted(data)

    def calculate_dissat(self, vars):
        # person | shift | pipeline
        dissat = vars.sum(axis=3)
        # person | shift+pipeline
        dissat = np.array([[[pipeline.item() for pipeline in shift]
                          for shift in person] for person in dissat])
        dissat = np.reshape(dissat, (dissat.shape[0], -1))
        dissat = dissat@self.shift_pl_dissat
        return dissat.flatten()

    def dissat_stats(self, schedule, vars_auxiliary):
        dissat = self.calculate_dissat(schedule)
        cr_dissat, cr_size = balance.exclude_dissat(dissat, vars_auxiliary)
        avg_dissat = cr_dissat.sum() / cr_size
        return avg_dissat, cr_dissat.min(), cr_dissat.max()
