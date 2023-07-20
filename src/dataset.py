from consts import data_root_path, JOBS, JOBLIST

class Dataset:
    def __init__(self, folder):
        assert folder in ("duLieu1", "duLieu2")
        self.data_path = data_root_path / folder
        
        pipelines = {
            "duLieu1": 1,
            "duLieu2": 3,
        }
        self.pipeline = pipelines[folder]

        self.workers_count = 0
        self.skills = []

        self.names = {}

        self.load_input()

    def load_input(self):
        # Load data from self.data_path
        
        # Load workers from 01_nhan_su.txt
        with open(self.data_path / "01_nhan_su.txt", "r") as f:
            f.readline() # Comment line
            _names = [line.strip().split() for line in f.readlines()]

            self.names = dict([worker[1], int(worker[0]) - 1] for worker in _names)

            self.workers_count = len(self.names)
            self.skills = [[0] * JOBS for _ in range(self.workers_count)]

        # Load skills of workers from ky_nang_Day_chuyen_?_?.txt
        for pipeline_idx in range(1, self.pipeline + 1):
            for job_idx in range(JOBS):
                job = JOBLIST[job_idx]
                with open(self.data_path / f"ky_nang_Day_chuyen_{pipeline_idx}_{job}.txt", "r") as f:
                    worker_list = [line.strip() for line in f.readlines()]
                    for worker_name in worker_list:
                        worker = self.names[worker_name]
                        self.skills[worker][job_idx] = 1
