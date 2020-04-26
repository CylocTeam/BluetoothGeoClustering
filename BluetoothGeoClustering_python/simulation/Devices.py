import numpy as np
import pandas as pd


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
        return np.min(np.max(0, np.random.normal(self.velocity, self.noise_addition*sigma_vel, 1)), 4)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_noise_addition(self, noise_addition):
        self.noise_addition = noise_addition


