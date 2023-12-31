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
        result = np.ndarray(shift_time.shape)
        for p in range(shift_time.shape[0]):
            for s in range(shift_time.shape[1]):
                if shift_time[p][s] != 0:
                    result[p][s] = (shift_time[p][s] + 2) * shift_dissat[s]
                else:
                    result[p][s] = 0

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

    def get_tt_dissat(self, data):
        # pipeline
        pipeline_sum = data.pipeline_req.sum(axis=1)
        pc = pipeline_sum.shape[0]
        total = np.sum([self.shift_pl_dissat[p::pc].flatten() * pipeline_sum[p] for p in range(pc)], axis=0)
        return total
