import numpy as np
import pandas as pd
import time
import psychopy.tools.coordinatetools as coor
from scipy.spatial import distance
from simulation.Device import Device
# pd.options.mode.chained_assignment = None  # default='warn'

simulation_default_time = 1000



class Simulation:
    def __init__(self, simulation_duration=-1, grid_res_m=0.1, grid_size_m=100, fps=1):
        self.fps = fps
        self.grid_res = grid_res_m
        self.simulation_duration = simulation_duration
        self.grid_size = grid_size_m + 1
        self.devices = pd.DataFrame(columns=['device', 'device_id', 'start_time', 'duration', 'x', 'y'])
        self.devices_location = []
        self.theta_direction_options = np.arange(0, 360, 90)
        self.simulation_data_path = 'simulation_data.pkl'

    def set_simulation_data_path(self, path):
        self.simulation_data_path = path

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
        self.grid_size = grid_size + 1

    def set_fps(self, fps):
        self.fps = fps

    def set_optional_theta_vec_degree(self, azimuth_vec):
        self.theta_direction_options = azimuth_vec

    def set_optional_theta_res_degree(self, res):
        self.theta_direction_options = np.arange(0, 360, res)

    def set_device_location(self, device_id, x, y):
        ind = (np.where(self.devices['device_id'] == device_id)[0]).item()
        self.devices.loc[ind, 'x'] = x
        self.devices.loc[ind, 'y'] = y

    def get_devices(self):
        return self.devices

    def get_current_simulation_duration(self):
        if self.simulation_duration == -1:
            max_times = self.devices['start_time'] + self.devices['duration']
            max_times = max_times.loc[self.devices['duration'] != -1]
            if not np.empty(max_times):
                self.simulation_duration = np.max(max_times)
            else:
                self.simulation_duration = simulation_default_time
        return self.simulation_duration

    def add_device(self, device, start_time=0, duration=-1, x=-1, y=-1):
        """
        add_device adds device to simulation devices.
        Input:
            device - device from device format.
            start_time - The time to add the device to the simulation.
                         The time is from the beginning of the simulation in seconds.
            duration - The duration time the device is in the simulation.
                         The time is from the start_time  in seconds.
                         -1 till the end of the simulation.
            x,y - current location of the added device. -1 for random point.
        """
        data = {'device': [device],
                'start_time': [start_time],
                'duration': [duration],
                'device_id': [self.devices.shape[0]],
                'x': [x],
                'y': [y]}
        self.devices = self.devices.append(pd.DataFrame(data=data), ignore_index=True)

    def check_locations(self):
        """
        check_locations generate random locations if needed (For x,y = -1).
        """
        loc_options = np.arange(0, self.grid_size, self.grid_res)
        for device in (self.devices.iterrows()):
            device = device[1]
            if device['x'] == -1:
                x = np.random.choice(loc_options)
                self.set_device_location(device['device_id'], x, device['y'])
            if device['y'] == -1:
                y = np.random.choice(loc_options)
                self.set_device_location(device['device_id'], device['x'], y)

    def update_device_location(self, device_id):

        device = self.devices.loc[self.devices['device_id'] == device_id]
        try:
            r = device.device[0].get_velocity() / self.fps
        except Exception as c:
            r = device.device.get_velocity() / self.fps
        theta = np.random.choice(self.theta_direction_options)
        x_add, y_add = coor.pol2cart(theta, r, units='deg')
        x = min(max(0, device['x'][0] + x_add), self.grid_size-1)
        y = min(max(0, device['y'][0] + y_add), self.grid_size-1)
        self.set_device_location(device_id, x, y)

        pass

    def update_devices_locations(self):
        for device_id in pd.unique(self.devices['device_id']):
            self.update_device_location(device_id)

    def run_simulation(self):
        device_class = Device()
        self.devices_location = pd.DataFrame(columns=['device_id', 'x', 'y', 'time'])
        time_vec = np.arange(0, self.get_current_simulation_duration(), 1 / self.fps)
        self.check_locations()
        for time in time_vec:
            # current_df = pd.DataFrame(columns=['device_id', 'x', 'y', 'time'])
            current_df = self.devices[['device_id', 'x', 'y']]
            current_df.insert(2, "time", np.ones_like(current_df.x)*time, True)
            self.devices_location = self.devices_location.append(current_df, ignore_index=True)
        #     Make a step
            self.update_devices_locations()
        print(self.devices_location)
        self.generate_receptions()

    def generate_receptions(self):
        data_variables = pd.read_pickle(self.simulation_data_path)
        for time in pd.unique(self.devices_location['time']):
            current_ind = self.devices_location['time'] == time
            current_devices = self.devices_location.loc[current_ind]
            points = np.hstack((current_devices['x'], current_devices['y']))
            distance_map = distance(points, points, 'euclidean')
            pass


if __name__ == "__main__":
    sim = Simulation(10)
    sim.add_device(Device(1, 0), 0, 10, 1, 5)
    sim.add_device(Device(1.3, 0), 0, 10, 2, 5)
    sim.run_simulation()
