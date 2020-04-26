import numpy as np
import pandas as pd


class Simulation_Devices:
    def __init__(self):
        self.devices = pd.DataFrame(columns=['device', 'start_time', 'end_time'])

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


class Device:
    def __init__(self, velocity=-1, noise_addition_to_vel=0):
        """
        velocity - wanted velocity in m/s, 0 - for static velocity, -1 for random velocity
        noise_addition_to_vel  - 1 for not steady velocity, 0 for steady
        """
        if velocity != -1:
            self.velocity = velocity
        else:
            # mean human velocity 1.3 m/s and 4 m/s is fast runner
            velocity = np.min(np.max(0, np.random.normal(1.3, 0.3, 1)), 4)
        self.noise_addition = noise_addition_to_vel

    def get_velocity(self, sigma_vel=0.2):
        return np.min(np.max(0, np.random.normal(self.velocity, self.noise_addition * sigma_vel, 1)), 4)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_noise_addition(self, noise_addition):
        self.noise_addition = noise_addition
