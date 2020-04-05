% This script parses BLE Beacon Indoor Localization Dataset (BBIL Dataset).
% The parsing is divided into two stages:
% 1) Parse RSSI Data of each user's BLE beacon (Transmitter), as received by the Raspberry Pis (receivers).
% 2) Union of the data of all users into a matrix of dimensions:
%       num_of_ble_beacon_measurements x num_of_raspberry_pi_edge_nodes

% Writer: Yehav Alkaher.
% Date: 31.3.2020
%%
clear all; close all; clc;
%%
dir_path = 'C:\Projects\BLE_RSSI\Datasets\BLE Beacon Indoor Localization Dataset (BBIL Dataset)\';
experiment_dirs = {'experiment1\', 'experiment2\'};
folder_names = {'train\', 'test\', 'valid\'};
%% 1. Parse AP locations into sessions:
%% 1.a. Set Room Separation:
%% 1.a.i. exp 1:
exp_idx = 1;
edges_details_path = [dir_path, experiment_dirs{exp_idx}, 'edges.csv'];
edges_details = readtable(edges_details_path);
I_room = imread([dir_path, experiment_dirs{exp_idx}, 'room.png']);

Conference_Room.exp1.rangex = [edges_details.edge_x(1), edges_details.edge_x(3)];
Conference_Room.exp1.rangey = [4.765, max(edges_details.edge_y)];

open('experiment1.fig'); suptitle('True locations of devices and edgenode locations'); title('(results of section 1.b.)')
figure; image(fliplr(I_room)); title('Map of Location 1')

x_sorted = unique(sort(edges_details.edge_x));
b_x = 35;
a_x = (2535-35)/(x_sorted(end) - x_sorted(1));

y_sorted = unique(sort(edges_details.edge_y));
b_y = 1166;
a_y = (176 - 1166)/(y_sorted(end-1) - y_sorted(1));

hold on;
scatter(b_x + a_x*edges_details.edge_x, b_y + a_y*edges_details.edge_y, 'sb')
scatter(b_x + a_x*linspace(edges_details.edge_x(1), edges_details.edge_x(3),1e3),b_y + a_y*4.765*ones(1e3,1),'g')
hold off;
%% 1.a.ii. exp 2:
exp_idx = 2;
edges_details_path = [dir_path, experiment_dirs{exp_idx}, 'edges.csv'];
edges_details = readtable(edges_details_path);
I_room = imread([dir_path, experiment_dirs{exp_idx}, 'room.png']);

open('experiment2.fig'); suptitle('True locations of devices and edgenode locations'); title('(results of section 1.b.)')
figure; image(imrotate(I_room,90,'bilinear')); title('Map of Location 1'); set(gca,'yDir','normal')
%% 1.b. Parse RSSI Data of each user's BLE beacon, as received by the Raspberry Pis:
for exp_idx = 1:length(experiment_dirs)
    % Edges Deteail per beaconid:
    edges_details_path = [dir_path, experiment_dirs{exp_idx}, 'edges.csv'];
    edges_details = readtable(edges_details_path);
    beaconid_vec = unique(edges_details.beaconid);
    
    figure;
    hold on
    scatter(edges_details.edge_x, edges_details.edge_y, 'sb','LineWidth',2)
    
    for folder_idx = 1:length(folder_names)
        target_dir = ['Parsed_Data\' experiment_dirs{exp_idx}, folder_names{folder_idx}];
        if ~exist(target_dir)
            mkdir(target_dir)
            copyfile(edges_details_path, ['Parsed_Data\' experiment_dirs{exp_idx}]);
            copyfile([dir_path, experiment_dirs{exp_idx}, 'room.png'], ['Parsed_Data\' experiment_dirs{exp_idx}]);
        end
        
        for b_id_idx = 1:length(beaconid_vec)
            beaconid = beaconid_vec(b_id_idx);
            edgenodeid_vec = unique(edges_details(edges_details.beaconid == beaconid,:).edgenodeid);
            
            data_filenames_per_beaconid = dir([dir_path, experiment_dirs{exp_idx}, folder_names{folder_idx}, '\*', num2str(beaconid) ,'_data.csv']);
            data_filenames_per_beaconid = {data_filenames_per_beaconid.name}.';
            for data_idx = 1:length(data_filenames_per_beaconid)
                data_per_beacon_id = readtable([dir_path, experiment_dirs{exp_idx}, folder_names{folder_idx}, data_filenames_per_beaconid{data_idx}],'Delimiter',',');
                data_per_beacon_id.distance = -1*ones(size(data_per_beacon_id.realx));
                data_per_beacon_id.isSameRoom = 1*ones(size(data_per_beacon_id.realx));
                
                for edge_idx = 1:length(edgenodeid_vec)
                    edgenodeid = edgenodeid_vec(edge_idx);
                    
                    beacon_edge_details = edges_details((edges_details.beaconid == beaconid) & (edges_details.edgenodeid == edgenodeid),:);
                    
                    row_indices = find(data_per_beacon_id.edgenodeid == edgenodeid);
                    data_per_beacon_id_edge = data_per_beacon_id(row_indices, :);
                    dist_from_edge_vec = sqrt( (data_per_beacon_id_edge.realx - beacon_edge_details.edge_x).^2 + (data_per_beacon_id_edge.realy - beacon_edge_details.edge_y).^2 );
                    data_per_beacon_id.distance(row_indices) = dist_from_edge_vec;
                    
                    if exp_idx == 1
                        is_same_room_vec =...
                            ((data_per_beacon_id_edge.realx >= Conference_Room.exp1.rangex(1)) .*...
                            (data_per_beacon_id_edge.realx <= Conference_Room.exp1.rangex(2)) .*...
                            (data_per_beacon_id_edge.realy >= Conference_Room.exp1.rangey(1)) .*...
                            (data_per_beacon_id_edge.realy <= Conference_Room.exp1.rangey(2)));
                        data_per_beacon_id.isSameRoom(row_indices) = is_same_room_vec;
                    end
                end
                
                scatter(data_per_beacon_id.realx, data_per_beacon_id.realy, [], data_per_beacon_id.isSameRoom);
                writetable(data_per_beacon_id, [target_dir, data_filenames_per_beaconid{data_idx}],'Delimiter',',')
            end
        end
    end
    
    hold off
end

%% 2. Parse RSSI Data of each user's BLE beacon, as received by the Raspberry Pis:
for exp_idx = 1:length(experiment_dirs)
    % Edges Deteail per beaconid:
    edges_details_path = [dir_path, experiment_dirs{exp_idx}, 'edges.csv'];
    edges_details = readtable(edges_details_path);
    edgenodeid_vec = sort(unique(edges_details.edgenodeid));
    
    for folder_idx = 1:length(folder_names)
        target_dir = ['Parsed_Data\' experiment_dirs{exp_idx}, folder_names{folder_idx}];
        data_filenames_per_beaconid = dir([target_dir, '\*.csv']);
        data_filenames_per_beaconid = {data_filenames_per_beaconid.name}.';
        
        exp_ble_rssi_mat = edgenodeid_vec;
        exp_room_index_vec = [];
        exp_distance_mat = [];
        exp_user_loc_mat = [];
        exp_user_beacon_id_vec = [];
        
        for data_idx = 1:length(data_filenames_per_beaconid)
            data_per_beacon_id = readtable([target_dir, data_filenames_per_beaconid{data_idx}],'Delimiter',',');
            date_time_values = unique(data_per_beacon_id.Datetime);
            
            exp_ble_rssi_sub_mat = nan+zeros(length(edgenodeid_vec), length(date_time_values));
            exp_room_index_sub_vec = data_per_beacon_id(1:size(data_per_beacon_id,1)/size(date_time_values,1):end,:).isSameRoom.';
            exp_user_beacon_id_sub_vec = data_per_beacon_id(1:size(data_per_beacon_id,1)/size(date_time_values,1):end,:).beaconid.';
            exp_distance_sub_mat = nan+zeros(length(edgenodeid_vec), length(date_time_values));
            exp_user_loc_sub_mat = [...
                data_per_beacon_id(1:size(data_per_beacon_id,1)/size(date_time_values,1):end,:).realx.';...
                data_per_beacon_id(1:size(data_per_beacon_id,1)/size(date_time_values,1):end,:).realy.'];
            
            for edgenodeid_idx = 1:length(edgenodeid_vec)
                data_per_edgenodeid = data_per_beacon_id(data_per_beacon_id.edgenodeid == edgenodeid_vec(edgenodeid_idx),:);
                if ~isempty(data_per_edgenodeid)
                    exp_ble_rssi_sub_mat(edgenodeid_idx, :) = data_per_edgenodeid.rssi.';
                    exp_distance_sub_mat(edgenodeid_idx, :) = data_per_edgenodeid.distance.';
                end
            end
            
            exp_ble_rssi_mat = [exp_ble_rssi_mat, exp_ble_rssi_sub_mat];
            exp_room_index_vec = [exp_room_index_vec, exp_room_index_sub_vec];
            exp_distance_mat = [exp_distance_mat, exp_distance_sub_mat];
            exp_user_loc_mat = [exp_user_loc_mat, exp_user_loc_sub_mat];
            exp_user_beacon_id_vec = [exp_user_beacon_id_vec, exp_user_beacon_id_sub_vec];
        end
        
        save([experiment_dirs{exp_idx}(1:end-1), '_', folder_names{folder_idx}(1:end-1), '_ble_rssi_mat.mat'],'exp_ble_rssi_mat','exp_room_index_vec','exp_distance_mat','exp_user_beacon_id_vec','exp_user_loc_mat');
    end
end