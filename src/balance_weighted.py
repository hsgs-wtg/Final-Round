import balance

# Pipeline | shift
def generate_dissat_weighted(data):
    # shift
    shift_dissat = balance.shift_dissat
    # pipeline | shift
    shift_time = data.shift_time
    return shift_time * shift_dissat

# weighted must be called
shift_dissat_weighted = None

def calculate_dissat(vars):
    