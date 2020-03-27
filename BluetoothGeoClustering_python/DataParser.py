import pandas as pd
import requests
import copy


class DataParser:
    def url2df(self, url):
        # extract data from url
        f = requests.get(url)
        df_raw = pd.read_json(f.text)
        df_raw.scannedDevicesMinTimestamp = pd.to_datetime(df_raw.scannedDevicesMinTimestamp) + \
                                            pd.offsets.Hour(3)  # Israel Summer Time
        df_raw.scannedDevicesMaxTimestamp = pd.to_datetime(df_raw.scannedDevicesMaxTimestamp) + \
                                            pd.offsets.Hour(3)  # Israel Summer Time
        df_raw = df_raw.rename(columns={'scannedDevicesMinTimestamp': 'scannedDevicesMinTime',
                                        'scannedDevicesMaxTimestamp': 'scannedDevicesMaxTime'})
        df_raw = df_raw.sort_values("scannedDevicesMaxTime")  # sorting by last time!
        return df_raw

    def scannedDevices2df(self, scannedDevices):
        df_sd = pd.json_normalize(scannedDevices)
        if df_sd.empty:
            #         print('No scans avaliable')
            return df_sd
        df_sd = df_sd.rename(columns={'timestamp': 'time'})
        df_sd.time = pd.to_datetime(df_sd.time) + pd.offsets.Hour(3)  # Israel Summer Time
        df_sd = df_sd.sort_values("time")
        return df_sd

    def allScannedDevicesInTime(self, df, rel_time, window_size_minutes=0, display_error=1):
        # parse the data
        sd = pd.DataFrame()
        id_suffix = df.scanningDeviceEddystoneUid[0][-12:]
        time_window = pd.offsets.Minute(window_size_minutes)
        mask = (df.scannedDevicesMinTime <= rel_time) & (
                df.scannedDevicesMaxTime >= rel_time + time_window)
        # time_window = pd.offsets.Minute(window_size_minutes / 2)
        # mask = (df.scannedDevicesMinTime <= rel_time + time_window) & (
        #         df.scannedDevicesMaxTime >= rel_time - time_window)
        if not any(mask) & display_error:
            print('No date at this time from: ' + id_suffix)
            return sd
        for row in df[mask].index:
            sd_new = self.scannedDevices2df(df.scannedDevices[row])
            if sd_new.empty & display_error:
                print('No scans avaliable from: ' + id_suffix)
                continue
            sd = pd.concat([sd, sd_new], ignore_index=True)
        return sd
