import numpy as np
import seaborn as sns
from DataFuncs import DataFuncs
from matplotlib import pyplot as plt


class PlotFuncs:
    def __init__(self, tag_measurements, win_size_seconds):
        self.win_size_seconds = win_size_seconds
        self.tag_measurements = tag_measurements

    def set_window_size_second(self, win_size_second):
        self.win_size_second = win_size_second

    def boxplot_func(self, show_measurements, title, y_label, plot_hue):
        plt.figure()
        if not plot_hue:
            ax = sns.boxplot(x=np.round(show_measurements["distance"] * 4) / 4, y=show_measurements[y_label]
                             ).set_title(title)
        else:
            ax = sns.boxplot(x=np.round(show_measurements["distance"] * 4) / 4, y=show_measurements[y_label],
                             hue=show_measurements["DisplayName"]).set_title(title)

    def violinplot_func(self, show_measurements, title, y_label, plot_hue):
        plt.figure()
        if not plot_hue:
            ax = sns.violinplot(x=np.round(show_measurements["distance"] * 4) / 4,
                                y=show_measurements[y_label]).set_title(title)
        else:
            ax = sns.violinplot(x=np.round(show_measurements["distance"] * 4) / 4,
                                y=show_measurements[y_label], hue=show_measurements["DisplayName"]).set_title(title)

    def plot_data(self, func, plot_func='violinplot', obstacle='No Obstacle', plot_hue=0):
        DataFuncsObj = DataFuncs()
        tag_rolling = DataFuncsObj.run_rolling_func_df_2_columns(self.tag_measurements, func, 'DisplayName',
                                                                 'distance', 'rssi', self.win_size_seconds)
        show_measurements = tag_rolling.where(tag_rolling.obstacle == obstacle)
        show_measurements = show_measurements.dropna(how='any').reset_index(drop=True)
        title = obstacle + " " + func + " - All setups"
        ylabel = func + "_rssi"
        if plot_func == 'violinplot':
            self.violinplot_func(show_measurements, title, ylabel, plot_hue)
        else:
            self.boxplot_func(show_measurements, title, ylabel, plot_hue)
