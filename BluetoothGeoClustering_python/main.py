import pandas as pd
import numpy as np
import params
import devices_ble_id_excel_dicts as dicts
from DataParser import DataParser
from TagMeasurements import TagMeasurements

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
ind = -time_str[::-1].find('.') -1
all_tag_measurements.to_pickle('tag_measurements_'+time_str[:ind]+'.pkl')

# b = pd.read_pickle('my_file.pkl')




