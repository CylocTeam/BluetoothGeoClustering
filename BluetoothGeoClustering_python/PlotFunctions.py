import numpy as np
import seaborn as sns
from DataFuncs import DataFuncs
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


class PlotFuncs:
    def __init__(self, tag_measurements, win_size_seconds):
        self.win_size_seconds = win_size_seconds
        self.tag_measurements = tag_measurements
        self.axes_size = 5
        self.res_meter = 0.5

    def set_minor_axes_size(self, axis_size):
        self.axes_size = axis_size

    def set_window_size_second(self, win_size_second):
        self.win_size_second = win_size_second

    def set_resolution(self, res_meter):
        self.res_meter = res_meter

    def boxplot_func(self, show_measurements, title, y_label, plot_hue):
        plt.figure()
        if not plot_hue:
            ax = sns.boxplot(x=np.round(show_measurements["distance"] /self.res_meter) *self.res_meter, y=show_measurements[y_label]
                             ).set_title(title)
        else:
            ax = sns.boxplot(x=np.round(show_measurements["distance"] * 4) / 4, y=show_measurements[y_label],
                             hue=show_measurements["DisplayName"]).set_title(title)
        ax.axes.yaxis.set_major_locator(MultipleLocator(self.axes_size))

    def violinplot_func(self, show_measurements, title, y_label, plot_hue):
        plt.figure()
        if not plot_hue:
            ax = sns.violinplot(x=np.round(show_measurements["distance"] * 4) / 4,
                                y=show_measurements[y_label]).set_title(title)
        else:
            ax = sns.violinplot(x=np.round(show_measurements["distance"] * 4) / 4,
                                y=show_measurements[y_label], hue=show_measurements["DisplayName"]).set_title(title)
        ax.axes.yaxis.set_major_locator(MultipleLocator(self.axes_size))

    def plot_data(self, func, plot_func='violinplot', obstacle='No Obstacle', plot_hue=0, percent=90, margin=0,
                  top_percent=80, bottom_percent=20, roll_by_2=1):
        DataFuncsObj = DataFuncs()
        DataFuncsObj.set_percent(percent)
        DataFuncsObj.set_margin(margin)
        DataFuncsObj.set_bottom_percent(bottom_percent)
        DataFuncsObj.set_top_percent(top_percent)
        if roll_by_2:
            tag_rolling = DataFuncsObj.run_rolling_func_df_2_columns(self.tag_measurements, func, 'DisplayName',
                                                                     'distance', 'rssi', self.win_size_seconds)
        else:
            tag_rolling = DataFuncsObj.run_rolling_func_df(self.tag_measurements, func, 'DisplayName',
                                                           'rssi', self.win_size_seconds)
        show_measurements = tag_rolling.where(tag_rolling.obstacle == obstacle)
        show_measurements = show_measurements.dropna(how='any').reset_index(drop=True)
        title = obstacle + " " + func + " - All setups"
        ylabel = func + "_rssi"
        if plot_func == 'violinplot':
            self.violinplot_func(show_measurements, title, ylabel, plot_hue)
        else:
            self.boxplot_func(show_measurements, title, ylabel, plot_hue)

# import pandas as pd
# norm_distance = 1  # m
# setup = 'Phone in hand'
# DataFuncsObj = DataFuncs()
# all_tag_measurements = pd.read_pickle(r'tag_measurements_2020_03_28.pkl')
# all_tag_measurements = all_tag_measurements.dropna(how='any').reset_index(drop=True)
# plot_data = DataFuncsObj.normalize_by_distance(all_tag_measurements, norm_distance, setup)
# PlotFuncsObj = PlotFuncs(plot_data, 60)
# PlotFuncsObj.plot_data('mean', plot_func='boxplot',obstacle='No Obstacle', plot_hue=1)
