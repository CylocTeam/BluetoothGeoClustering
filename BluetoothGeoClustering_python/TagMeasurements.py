import numpy as np
import pandas as pd
import params
import devices_ble_id_excel_dicts as dicts


class TagMeasurements:
    def __init__(self, name):
        self.name = name
        self.experiment_file = pd.read_excel(params.excels_folder + name + '.xlsx')
        self.obstacles = np.unique(self.experiment_file.obstacle)
        self.setup = np.unique(self.experiment_file.setup)
    def get_relevant_keys(self):
        display_name = dicts.name_to_displayname[self.name]
        relevant_keys = [key for key in dicts.bleId.keys() if display_name.lower() in key.lower()]