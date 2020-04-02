import os
import glob
import pandas as pd
import useful_dbs.BBIL.db_params as db_params

all_files = pd.DataFrame([])
# dir all csv files
for exp_folder in db_params.exp_folders:
    exp_files = pd.DataFrame([])
    for data_kind in db_params.data_folders:
        current_folder = os.path.join(db_params.main_folder, exp_folder, data_kind)
        files = glob.glob(current_folder + "\*_data.csv")
        for file in files:
            curr_table = pd.read_csv(file)
            curr_table = curr_table.rename(columns={'Datetime': 'time'})
            curr_table.data_kind = data_kind
            curr_table.time = pd.to_datetime(curr_table.time)
            # start_ind = -file[::-1].find('_', 9)
            # end_ind = -len('_data.csv')
            # curr_table['DisplayName'] = file[start_ind:end_ind] + "_phone_BBIL"
            curr_table['DisplayName'] = [str(edgenodeid) + "_phone_BBIL" for edgenodeid in curr_table.edgenodeid]
            curr_table['setup'] = 'Phone in hand'
            curr_table.loc[curr_table.isSameRoom == 0, 'obstacle'] = 'Obstacle: wall'
            curr_table.loc[curr_table.isSameRoom == 1, 'obstacle'] = 'No Obstacle'

            all_files = pd.concat([all_files, curr_table], ignore_index=True)
            exp_files = pd.concat([exp_files, curr_table], ignore_index=True)
            print(file)
    exp_files.to_pickle('tag_measurements_BBIL' + exp_folder + '.pkl')
all_files.to_pickle('tag_measurements_BBIL_all.pkl')
