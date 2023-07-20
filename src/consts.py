from pathlib import Path

root_path = Path(__file__).parent.parent
data_root_path = root_path / "data"

ALLOWED_DAYS = 24
SHIFTS = 28 * 3
JOBS = 3 

JOBLIST = ["Rot", "Pallet", "May_dong_hop"]

# --- Parameters --- #

WAGE = (1600, 10)
