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
name = "yanay"
TG = TagMeasurements(name)
TG.set_relevant_keys()
TG.tag_measurements()







