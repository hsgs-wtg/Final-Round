import numpy as np
from consts import data_root_path, JOBS, JOBLIST, SHIFTS

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
        self.shift_time = []
        self.names = {}
        self.hourly_wage = 0
        self.with_skills = []

        self.load_input()

    def load_input(self):
        # Load data from self.data_path
        
        # Load workers from 01_nhan_su.txt
        with open(self.data_path / "01_nhan_su.txt", "r") as f:
            f.readline() # Comment line
            _names = [line.strip().split() for line in f.readlines()]

            self.names = dict([worker[1], int(worker[0]) - 1] for worker in _names)

            self.workers_count = len(self.names)
            self.skills = [
                [
                    [0] * JOBS for _ in range(self.pipeline)
                ] for _ in range(self.workers_count)
            ]

        self.with_skills = [[[] for _ in range(JOBS)] for _ in range(self.pipeline)]
        # Load skills of workers from ky_nang_Day_chuyen_?_?.txt
        for pipeline_idx in range(1, self.pipeline + 1):
            for job_idx in range(JOBS):
                job = JOBLIST[job_idx]
                with open(self.data_path / f"ky_nang_Day_chuyen_{pipeline_idx}_{job}.txt", "r") as f:
                    worker_list = [line.strip() for line in f.readlines()]
                    for worker_name in worker_list:
                        worker = self.names[worker_name]
                        self.skills[worker][pipeline_idx - 1][job_idx] = 1
                        self.skills[worker][job_idx] = 1
                    
                    for worker_name in worker_list:
                        self.with_skills[pipeline_idx - 1][job_idx].append(
                            self.names[worker_name])
                    self.with_skills[pipeline_idx-1][job_idx] = np.array(
                        self.with_skills[pipeline_idx-1][job_idx])

        # Load time of pipelines from lenh_san_xuat_Day_chuyen_?.txt
        self.shift_time = np.ndarray(shape=(self.pipeline, SHIFTS))
        for pipeline_idx in range(1, self.pipeline+1):
            with open(self.data_path / f"lenh_san_xuat_Day_chuyen_{pipeline_idx}.txt", "r") as f:
                f.readline() # Comment line
                _time = [line.strip().split() for line in f.readlines()]
                
                shift_start_time = [6,14,22]


                for i in range(len(_time)):
                    
                    start_day = int(_time[i][0][8:10])
                    start_hour = int(_time[i][1][0:2])

                    end_day = int(_time[i][2][8:10])
                    end_hour = int(_time[i][3][0:2])

                    if(end_day > start_day):
                        end_hour += 24

                    if(start_hour<shift_start_time[0]):
                        self.shift_time[pipeline_idx-1][3*(start_day-2)+2] += shift_start_time[0]-start_hour

                    for i in range(3):
                        st = shift_start_time[i]
                        en = shift_start_time[(i+1)%3]+(i==2)*24

                        self.shift_time[pipeline_idx-1][3*(start_day-1)+i] += max(0,min(en,end_hour)-max(st,start_hour))   
        
        match self.data_path[-1]:
            case "1":
                self.pipeline_req = ((1, 2, 2), )
            case "2":
                self.pipeline_req = ((1, 2, 2), (2, 2, 2), (1, 2, 3))
