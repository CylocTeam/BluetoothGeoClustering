import numpy as np
import pandas as pd
import params
import devices_ble_id_excel_dicts as dicts
from DataParser import DataParser

DataParser_funcs = DataParser()
class TagMeasurements:
    def __init__(self, name):
        self.name = name
        self.experiment_file = pd.read_excel(params.excels_folder + name + '.xlsx')
        self.obstacles = np.unique(self.experiment_file.obstacle)
        self.setups = np.unique(self.experiment_file.setup)
        self.relevant_keys = []

    def set_relevant_keys(self):
        display_name = dicts.name_to_displayname[self.name]
        relevant_keys = [key for key in dicts.bleId.keys() if display_name.lower() in key.lower()]
        self.relevant_keys = relevant_keys

    def get_measurements(self, rel_time, window_size_minutes):
        for key in self.relevant_keys:
            current_df = DataParser_funcs.url2df(url=params.url + dicts.bleId[key])
            # allScannedDevicesInTime parse the data
            current_sd = DataParser_funcs.allScannedDevicesInTime(current_df, rel_time, window_size_minutes,
                                                                  display_error=0)
            sd = pd.concat([sd, current_sd], ignore_index=True)
        return sd

  
