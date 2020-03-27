import pandas as pd
import requests
import copy
import params
import devices_to_ble_id
import DataParser

# Experiment times
rel_time = pd.to_datetime("2020-03-27 14:00:00") #Local time! :D
window_size_minutes = 120
sd = pd.DataFrame([])
# load all data
for key in bleId:
    current_df = DataParser.url2df(url= params.url + bleId[key])
    #allScannedDevicesInTime parse the data
    current_sd = DataParser.allScannedDevicesInTime(current_df, rel_time, window_size_minutes, display_error=0)
    sd = pd.concat([sd, current_sd], ignore_index=True)
print('done loading experiment data')
