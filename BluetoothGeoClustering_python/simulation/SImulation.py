import numpy as np
import pandas as pd
from simulation.Device import Device

simulation_default_time = 1000


class Simulation:
    def __init__(self, simulation_duration=-1, grid_res_m=0.1, grid_size_m=100, fps=1):
        self.fps = fps
        self.grid_res = grid_res_m
        self.simulation_duration = simulation_duration
        self.grid_size = grid_size_m
        self.devices = pd.DataFrame(columns=['device', 'start_time', 'end_time'])

    def set_simulation_duration(self, duration):
        """
        set_simulation_duration sets the simulation duration.
        Input:
            duration - simulation duration in seconds. -1 for max end time.
        """
        self.simulation_duration = duration

    def set_grid_resolution(self, res_m):
        self.grid_res = res_m

    def set_grid_size(self, grid_size):
        self.grid_size = grid_size

    def set_fps(self, fps):
        self.fps = fps

    def add_device(self, device, start_time=0, duration=-1):
        """
        add_device adds device to simulation devices.
        Input:
            device - device from device format.
            start_time - The time to add the device to the simulation.
                         The time is from the beginning of the simulation in seconds.
            duration - The duration time the device is in the simulation.
                         The time is from the start_time  in seconds.
                         -1 till the end of the simulation.
        """
        df_current = pd.DataFrame(columns=['device', 'start_time', 'duration', 'device_id'])
        df_current['device'] = device
        df_current['start_time'] = start_time
        df_current['duration'] = duration
        df_current['device_id'] = self.devices.shape[0]

        self.devices = self.devices.append(df_current, ignore_index=True)

    def get_current_simulation_duration(self):
        if self.simulation_duration == -1:
            max_times = self.devices['start_time'] + self.devices['duration']
            max_times = max_times.loc[self.devices['duration'] != -1]
            if not np.empty(max_times):
                self.simulation_duration = np.max(max_times)
            else:
                self.simulation_duration = simulation_default_time
        return self.simulation_duration

    def run_simulation(self):
        device_class = Device()
        self.devices_location = pd.df(columns=['device_id', 'x', 'y', 'time'])

    