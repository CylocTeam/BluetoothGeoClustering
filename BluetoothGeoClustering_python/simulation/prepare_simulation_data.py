import numpy
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import sys

sys.path.insert(0, '..')
import warnings

warnings.filterwarnings("ignore")
from DataFuncs import DataFuncs


def start_pipe(df):
    return df.copy()


def round_distance(df, res):
    df['round_distance'] = np.round(df["distance"] / res_meter) * res_meter
    return df


def rssi_not_db(df):
    df['rssi_not_db'] = np.power(10, df['normalized_rssi'] / 10)
    return df


def agg_funcs_each_distance(df):
    grouped = df.groupby('round_distance')
    simulation_params = grouped['normalized_rssi'].agg([np.mean, np.var, np.ma.count])
    return simulation_params


def normalized_rssi_not_db(df, norm_distance, res_norm):
    round_distance = np.round(df["distance"] / res_norm) * res_norm
    median_rssi = np.median(df['rssi'].loc[round_distance == norm_distance])
    df['normalized_rssi'] = df['rssi'] - median_rssi
    return df


if __name__ == "__main__":
    DB_pickle = r'../useful_dbs/BBIL/tag_measurements_BBIL_all.pkl'
    all_tag_measurements = pd.read_pickle(DB_pickle)
    res_meter = 0.25  # m
    norm_distance = 1  # m
    res_norm = res_meter

    simulation_data = (all_tag_measurements.pipe(start_pipe)
                       .pipe(normalized_rssi_not_db, norm_distance, res_norm)
                       .pipe(rssi_not_db)
                       .pipe(round_distance, res_meter)
                       .pipe(agg_funcs_each_distance))

    simulation_data.to_pickle('simulation_data.pkl')
