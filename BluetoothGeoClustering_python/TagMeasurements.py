import numpy as np
import pandas as pd
import params
from datetime import datetime
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
        sd = pd.DataFrame([])
        for key in self.relevant_keys:
            current_df = DataParser_funcs.url2df(url=params.url + dicts.bleId[key])
            # allScannedDevicesInTime parse the data
            current_sd = DataParser_funcs.allScannedDevicesInTime(current_df, rel_time, window_size_minutes,
                                                                  display_error=0)
            if current_sd.shape[0] != 0:
                current_sd['DisplayName'] = key
            sd = pd.concat([sd, current_sd], ignore_index=True)

        return sd

    def tag_measurements(self):
        tag_measurements = pd.DataFrame([])
        for setup in self.setups:
            for obstacle in self.obstacles:
                current_sub_experiment = self.experiment_file.where(
                    np.logical_and(self.experiment_file.obstacle == obstacle, self.experiment_file.setup == setup))
                current_sub_experiment = current_sub_experiment.dropna(how='all').reset_index(drop=True)
                type(current_sub_experiment.start_time[0])
                if not type(current_sub_experiment.start_time[0]) is float:
                    for distance_ind in range(current_sub_experiment.shape[0]):
                        # extract time of subset
                        start_time = current_sub_experiment.start_time[distance_ind]
                        end_time = current_sub_experiment.end_time[distance_ind]
                        date_exp = current_sub_experiment.date[distance_ind].to_pydatetime()
                        window_size_timedelta = (datetime.combine(date_exp, end_time) - \
                                                 datetime.combine(date_exp, start_time))
                        window_size_minutes = window_size_timedelta.seconds / 60
                        rel_datetime = datetime.combine(date_exp, start_time)
                        rel_time = pd.Timestamp(rel_datetime)
                        # extract measurements of subset
                        current_meas = self.get_measurements(rel_time, window_size_minutes)
                        current_meas['setup'] = setup
                        current_meas['obstacle'] = obstacle
                        current_meas['distance'] = current_sub_experiment.distance[distance_ind]
                        tag_measurements = pd.concat([tag_measurements, current_meas], ignore_index=True)
                        print(setup + " " + obstacle + " " + current_sub_experiment.distance[distance_ind] + "m")

        return tag_measurements
