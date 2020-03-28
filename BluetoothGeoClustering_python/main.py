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
load_flag = 0
DataParser_funcs = DataParser()

# Analyze experiment
# Get BLE data
# PAY ATTENTION: tag_measurements function will delete all row in excel that contains nan
if not load_flag:
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
    scipy.io.savemat('tag_measurements_' + time_str[:ind] + '.mat',
                     mdict={name: col.values for name, col in all_tag_measurements.items()})








