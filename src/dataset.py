from consts import data_root_path

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

            self.names = dict([worker[1], int(worker[0])] for worker in _names)

            self.workers_count = len(self.names) 



    