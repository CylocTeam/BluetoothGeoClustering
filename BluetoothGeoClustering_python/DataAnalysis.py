import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

all_tag_measurements = pd.read_pickle(r'tag_measurements_2020_03_28.pkl')

# Plots:
show_measurements = all_tag_measurements.where(all_tag_measurements.obstacle == 'No Obstacle')
sns.set(style="darkgrid")
ax = sns.boxplot(x=show_measurements["distance"], y=show_measurements["rssi"])

# plt.figure()
# plt.boxplot(pd.DataFrame([show_measurements.distance,show_measurements.rssi]))

pass












unique_scan_deviceUID = pd.unique(show_measurements.scannedDeviceEddystoneUid)
color_dict = {k: (v + 1) * 45 for v, k in enumerate(unique_scan_deviceUID)}
color_vec = [color_dict[uid] for uid in show_measurements.scannedDeviceEddystoneUid]

plt.interactive(True)
for UID, size_scatter in zip(unique_scan_deviceUID, 5*np.linspace(10, 1, unique_scan_deviceUID.shape[0])):
    current_show_measurements = show_measurements.where(show_measurements.scannedDeviceEddystoneUid == UID)
    plt.figure()
    plt.scatter(show_measurements.distance, show_measurements.rssi, label=UID[-12:])
    # ax.legend()
    plt.grid(True)
    plt.xlabel = 'Distance[m]'
    plt.ylabel = 'rssi [dB]'
    plt.title = current_show_measurements.DisplayName[0] + "; scan:" +UID[-12:]
    plt.show()