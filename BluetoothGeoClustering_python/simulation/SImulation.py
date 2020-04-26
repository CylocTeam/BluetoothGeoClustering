import numpy as np
import pandas as pd
from simulation.Device import Device

class Simulation:
    def __init__(self, simulation_duration=1000, grid_res_m=0.1, grid_size_m=100, fps=1):
        self.fps = fps
        self.grid_res = grid_res_m
        self.simulation_duration = simulation_duration
        self.grid_size = grid_size_m
        self.devices = pd.DataFrame(columns=['device', 'start_time', 'end_time'])

    def set_simulation_duration(self, duration):
        self.simulation_duration = duration

    def set_grid_resolution(self,res_m):
        self.grid_res = res_m

    def set_grid_size(self, grid_size):
        self.grid_size = grid_size

    def set_fps(self,fps):
        self.fps = fps

    def add_device(self, device, start_time=0, end_time=1000):
        """
        add_device adds device to simulation devices.
        Input:
            device - device from device format.
            start_time - The time to add the device to the simulation.
                         The time is from the beginning of the simulation in seconds.
            end_time - The time to remove the device from the simulation.
                         The time is from the beginning of the simulation in seconds.
                         -1 till the end of the simulation.
        """
        df_current = pd.DataFrame(columns=['device', 'start_time', 'end_time'])
        df_current['device'] = device
        df_current[start_time] = start_time
        df_current[end_time] = end_time
        self.devices = self.devices.append(df_current, ignore_index=True)

    def run_simulation(self):
        device_class = Device()
        

