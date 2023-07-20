from consts import data_root_path

class Dataset:
    def __init__(self, folder):
        assert folder in ("duLieu1", "duLieu2")
        self.data_path = data_root_path / folder
        
        self.workers = 0
        self.skills = []

        self.load_input()

    def load_input(self):
        # Load data from self.data_path
        pass


