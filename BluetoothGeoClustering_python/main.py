import pandas as pd
import numpy as np
import scipy.io
import devices_ble_id_excel_dicts as dicts
from TagMeasurements import TagMeasurements
from DataParser import DataParser
import plotly.express as px
import plotly.graph_objects as go

from matplotlib import pyplot as plt

# Experiment times
rel_time = pd.to_datetime("2020-03-27 14:00:00")  # Local time! :D
window_size_minutes = 120
DataParser_funcs = DataParser()

# Analyze experiment
# Get BLE data
# PAY ATTENTION: tag_measurements function will delete all row in excel that contains nan
all_tag_measurements = pd.DataFrame([])
for name in dicts.name_to_displayname:
    # name = "yanay"
    TG = TagMeasurements(name)
    TG.set_relevant_keys()
    current_tag_meas = TG.tag_measurements()
    all_tag_measurements = pd.concat([all_tag_measurements, current_tag_meas], ignore_index=True)
    print('Done tagging: ' + name + "'s data")

time_str = str(pd.Timestamp.now().to_numpy())
ind = -time_str[::-1].find('.') - 1
time_str = time_str[:ind]
time_str = time_str.replace(':', '_')
time_str = time_str.replace('-', '_')
time_str = time_str.replace('T', '__')
all_tag_measurements.to_pickle('tag_measurements_' + time_str[:ind] + '.pkl')
# scipy.io.savemat('tag_measurements_' + time_str[:ind] + '.mat', mdict={'all_tag_measurements': all_tag_measurements})

# b = pd.read_pickle('my_file.pkl')

# Plots:
show_measurements = all_tag_measurements.where(all_tag_measurements.obstacle == 'No Obstacle')
unique_scan_deviceUID = pd.unique(show_measurements.scannedDeviceEddystoneUid)
color_dict = {k: (v + 1) * 45 for v, k in enumerate(unique_scan_deviceUID)}
color_vec = [color_dict[uid] for uid in show_measurements.scannedDeviceEddystoneUid]
# fig = go.Figure()
# for UID in unique_scan_deviceUID:
#     current_show_measurements = show_measurements.where(show_measurements.scannedDeviceEddystoneUid == UID)
#     fig.add_trace(go.Scatter(x=current_show_measurements.distance, y=current_show_measurements.rssi,
#                     mode='markers',
#                     name = UID[-12:]))
#                      marker=dict(color=color_vec)))
# fig.show()
plt.interactive(True)
for UID, size_scatter in zip(unique_scan_deviceUID, 5*np.linspace(10, 1, unique_scan_deviceUID.shape[0])):
    current_show_measurements = show_measurements.where(show_measurements.scannedDeviceEddystoneUid == UID)
    fig, ax = plt.subplots()
    ax.scatter(show_measurements.distance, show_measurements.rssi, label=UID[-12:])
    # ax.legend()
    ax.grid(True)
    ax.xlabel = 'Distance[m]'
    ax.ylabel = 'rssi [dB]'
    ax.title = current_show_measurements.DisplayName[0] + "; scan:" +UID[-12:]
    ax.show()

pass
