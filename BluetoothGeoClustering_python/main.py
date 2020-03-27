import pandas as pd
import requests
import copy
import params
import devices_ble_id_excel_dicts as dicts
from DataParser import DataParser
import numpy as np

# Experiment times
rel_time = pd.to_datetime("2020-03-27 14:00:00")  # Local time! :D
window_size_minutes = 120

# Analyze experiment
name = "yanay"
experiment_file = pd.read_excel(params.excels_folder+name+'.xlsx')
display_name = dicts.name_to_displayname[name]
relevant_keys = [key for key in dicts.bleId.keys() if display_name.lower() in key.lower()]
sd = pd.DataFrame([])
# load all data
for key in relevant_keys:
    current_df = DataParser.url2df(url=params.url + dicts.bleId[key])
    # allScannedDevicesInTime parse the data
    current_sd = DataParser.allScannedDevicesInTime(current_df, rel_time, window_size_minutes, display_error=0)
    sd = pd.concat([sd, current_sd], ignore_index=True)
print('done loading experiment data')

