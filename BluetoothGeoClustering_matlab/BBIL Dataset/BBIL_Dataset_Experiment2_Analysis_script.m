clear all; close all; clc;
%% Initialization:
load('experiment2_train_ble_rssi_mat.mat');
edgenode_ids = exp_ble_rssi_mat(:, 1);
beacon_ids = unique(exp_user_beacon_id_vec);

% color_map_jet = colormap('jet');
% beacon_id_color_map = color_map_jet(round( size(color_map_jet,1) * beacon_ids/max(beacon_ids) ), :);

beacon_id_color_map = [1 0 0; 1 0 0; 0 1 0; 0 1 0; 0 0 1; 0 0 1; 0 1 1; 0 1 1; 1 0.5 0];
beacon_id_markers = '*ox>^';
%% Parse 'experiment1_train_ble_rssi_mat.mat' and 'edges.csv':
exp_ble_rssi_mat = exp_ble_rssi_mat(:,2:end);
full_measurement_indices = find(sum(~isnan(exp_ble_rssi_mat),1) == length(edgenode_ids));

ble_rssi_mat = exp_ble_rssi_mat(:, full_measurement_indices);
room_index_vec = exp_room_index_vec(full_measurement_indices);
distance_mat = exp_distance_mat(:, full_measurement_indices);
user_loc_mat = exp_user_loc_mat(:, full_measurement_indices);
user_beacon_id_vec = exp_user_beacon_id_vec(:, full_measurement_indices);

edges_details_path = 'Parsed_Data\experiment2\edges.csv';
edges_details = readtable(edges_details_path,'Delimiter',',');
%% Choose Data Randomly - to work on data from all three BLE beacon devices
indices = randperm(size(ble_rssi_mat,2));
indices = indices(1:2e3);

chosen_ble_rssi_mat = ble_rssi_mat(:, indices);
chosen_room_index_vec = room_index_vec(indices);
chosen_distance_mat = distance_mat(:, indices);
chosen_user_loc_mat = user_loc_mat(:, indices);
chosen_user_beacon_id_vec = user_beacon_id_vec(indices);

% Plot user's Beacon-id Histogram:
figure(1); set(gcf,'Position', get(0, 'Screensize'));
subplot(1,2,1); hist(chosen_user_beacon_id_vec, beacon_ids);
title('Chosen Data Beacon-Id Histogram')
subplot(1,2,2); hist(user_beacon_id_vec, beacon_ids);
title('All Data Beacon-Id Histogram')

% Plot User-Locations:
user_loc_mat_1 = chosen_user_loc_mat(:,chosen_user_beacon_id_vec == 1);
user_loc_mat_3 = chosen_user_loc_mat(:,chosen_user_beacon_id_vec == 3);
user_loc_mat_6 = chosen_user_loc_mat(:,chosen_user_beacon_id_vec == 6);
user_loc_mat_8 = chosen_user_loc_mat(:,chosen_user_beacon_id_vec == 8);
user_loc_mat_9 = chosen_user_loc_mat(:,chosen_user_beacon_id_vec == 9);

figure(2); set(gcf,'Position', get(0, 'Screensize'));
hold on;
plot(user_loc_mat_1(1,:), user_loc_mat_1(2,:),'*','Color',beacon_id_color_map(1,:))
plot(user_loc_mat_3(1,:), user_loc_mat_3(2,:),'o','Color',beacon_id_color_map(3,:))
plot(user_loc_mat_6(1,:), user_loc_mat_6(2,:),'x','Color',beacon_id_color_map(6,:))
plot(user_loc_mat_8(1,:), user_loc_mat_8(2,:),'>','Color',beacon_id_color_map(8,:))
plot(user_loc_mat_9(1,:), user_loc_mat_9(2,:),'^','Color',beacon_id_color_map(9,:))
plot(edges_details.edge_x, edges_details.edge_y, 'sk','MarkerFaceColor','m','MarkerSize',10,'LineWidth',2);
hold off;
xlabel('x [m]'); ylabel('y [m]');
title('Randomly Chosen User-Locations for Exp. 2')
%% Correlation between RSSI measurements and location measurements:
S_Euc_rssi = DiffMatrixExtraction(chosen_ble_rssi_mat.');
S_Euc_loc = DiffMatrixExtraction(chosen_user_loc_mat.');

figure(3); set(gcf,'Position', get(0, 'Screensize'));
suptitle('Comparison between RSSI and Location Difference-Matrices of Chosen Measurements:')
subplot(1,2,1); imagesc(S_Euc_rssi); title('RSSI Measurements'' Difference-Matrix')
subplot(1,2,2); imagesc(S_Euc_loc); title('Location Measurements'' Difference-Matrix')
% figure; imagesc(sqrt(S_Euc)); colorbar

figure(4); set(gcf,'Position', get(0, 'Screensize'));
semilogy(sqrt(S_Euc_loc(:)), S_Euc_rssi(:),'*');
title('Correlation Between "Location distance" and "RSSI distance"')
xlabel('Location distance [m]')
ylabel('RSSI distance [dB]')
%% Laplacian-Eigenmaps Extraction:
alpha_scaling = 1e-3;
S = exp(-alpha_scaling*S_Euc_rssi);

figure(5); set(gcf,'Position', get(0, 'Screensize'));
imagesc(S);
title(['RSSI Measurements'' Similarity-Matrix using a Gaussian Kernel with a scaling-factor ' num2str(alpha_scaling)])

d_i = sum(S,2);
D = diag(d_i);
A = D\S;%inv(D) * S;

[V,Lambda] = eig(A);
eigenValues = sum(Lambda,2);
% eigenValues = abs(sum(Lambda,2));
[eigenValues ,eigenValues_idx]= sort(eigenValues,'desc');
V = V(:,eigenValues_idx);
zeta_k = eigenValues(1:end-1)-eigenValues(2:end);
if (sum(zeta_k < 0) > 0)
    disp('Error - (zeta_k < 0)')
end

DataMatrix_new = V(:,2:5);

%% Laplacian-Eigenmaps new representation colored by User Beacon-Id
figure(6); set(gcf,'Position', get(0, 'Screensize'));
scatter3(DataMatrix_new(:,1),DataMatrix_new(:,2),DataMatrix_new(:,3),[],chosen_user_beacon_id_vec);
colormap(beacon_id_color_map); colorbar('Ticks',beacon_ids)
title('Laplacian-Eigenmaps new representation colored by User Beacon-Id')

% figure;
% scatter(DataMatrix_new(:,1),DataMatrix_new(:,2),[],chosen_user_beacon_id_vec);
% scatter(DataMatrix_new(:,2),DataMatrix_new(:,3),[],chosen_user_beacon_id_vec);
% colormap(beacon_id_color_map); colorbar
% title('Laplacian-Eigenmaps new representation colored by User Beacon-Id')

% figure; scatter(DataMatrix_new(:,1),DataMatrix_new(:,2),[],chosen_user_beacon_id_vec); colormap jet; colorbar
% figure; scatter3(DataMatrix_new(:,2),DataMatrix_new(:,3),DataMatrix_new(:,4),[],chosen_user_beacon_id_vec); colormap jet; colorbar
% figure; scatter(DataMatrix_new(:,1),DataMatrix_new(:,2),[],exp_room_index_vec(indices)); colormap winter
%% Laplacian-Eigenmaps new representation colored by Distance from 2nd Edgenode:
figure(7); set(gcf,'Position', get(0, 'Screensize'));
scatter3(DataMatrix_new(:,1),DataMatrix_new(:,2),DataMatrix_new(:,3),[],chosen_distance_mat(2,:));
colormap jet; colorbar
title('Laplacian-Eigenmaps new representation colored by Distance from 2nd Edgenode')

%% Laplacian-Eigenmaps new representation with correspondance to the distance from each edgenode (Rasppberry Pi):
figure(8); set(gcf,'Position', get(0, 'Screensize'));
suptitle('1st Vector of New-Representation with Correspondance to Distance from each Edgenode (Rasppberry Pi)')
for k = 1:9
    subplot(3,3,k);
    plot(chosen_distance_mat(k,:), DataMatrix_new(:,1),'*');
    xlabel('Distance from each Edgenode [m]')
    ylabel('Laplacian-Eigenmaps')
    title([num2str(edgenode_ids(k)) ' :'])
end

%% User-Locations colored by values of the 1st Vector of the New-Representation:
figure(9); set(gcf,'Position', get(0, 'Screensize'));
scatter(chosen_user_loc_mat(1,:), chosen_user_loc_mat(2,:),[],DataMatrix_new(:,1)); colorbar
hold on; plot(edges_details.edge_x, edges_details.edge_y, 'sk','MarkerFaceColor','m','MarkerSize',10,'LineWidth',2); hold off;
xlabel('x [m]'); ylabel('y [m]');
title('User-Locations colored by values of the 1st Vector of the New-Representation')

%% User-Locations colored by values of the 1st Vector of the New-Representation and marked by beacon_id:
figure(10); set(gcf,'Position', get(0, 'Screensize'));
hold on;
for k = 1:length(beacon_ids)
    subplot(3,2,k);
    scatter(chosen_user_loc_mat(1,chosen_user_beacon_id_vec == beacon_ids(k)), chosen_user_loc_mat(2,chosen_user_beacon_id_vec == beacon_ids(k)),[],DataMatrix_new(chosen_user_beacon_id_vec == beacon_ids(k),1),'Marker',beacon_id_markers(k));
    colormap jet; caxis([min(DataMatrix_new(:,1)), max(DataMatrix_new(:,1))]); colorbar;
    hold on; plot(edges_details.edge_x, edges_details.edge_y, 'sk','MarkerFaceColor','m','MarkerSize',10,'LineWidth',2); hold off;
    xlabel('x [m]'); ylabel('y [m]'); title([num2str(beacon_ids(k)) ' :'])
end
hold off;
hold on; plot(edges_details.edge_x, edges_details.edge_y, 'sk','MarkerFaceColor','m','MarkerSize',10,'LineWidth',2); hold off;
% colormap jet; colorbar('Ticks',linspace(min(DataMatrix_new(:,1)),max(DataMatrix_new(:,1)),5),'TickLabels', beacon_ids);
suptitle('User-Locations colored by values of the 1st Vector of the New-Representation')

%% Laplacian-Eigenmaps new representation colored by User Beacon-Ids 1 & 3 :
figure(11); set(gcf,'Position', get(0, 'Screensize'));
k = 1; l = 3;
hold on;
scatter(DataMatrix_new(chosen_user_beacon_id_vec == k,1),...
    DataMatrix_new(chosen_user_beacon_id_vec == k,2),...
    [],chosen_user_beacon_id_vec(chosen_user_beacon_id_vec == k));

scatter(DataMatrix_new(chosen_user_beacon_id_vec == l,1),...
    DataMatrix_new(chosen_user_beacon_id_vec == l,2),...
    [],chosen_user_beacon_id_vec(chosen_user_beacon_id_vec == l));
hold off
colormap jet
colorbar
title('Laplacian-Eigenmaps new representation colored by User Beacon-Ids 1 & 3')

%% User-Locations colored by values of the 2nd Vector of the New-Representation:
figure(12); set(gcf,'Position', get(0, 'Screensize'));
scatter(chosen_user_loc_mat(1,:), chosen_user_loc_mat(2,:),[],DataMatrix_new(:,2)); colorbar
hold on; plot(edges_details.edge_x, edges_details.edge_y, 'sk','MarkerFaceColor','m','MarkerSize',10,'LineWidth',2); hold off;
xlabel('x [m]'); ylabel('y [m]');
title('User-Locations colored by values of the 2nd Vector of the New-Representation')

%% Correlation between RSSI measurements and location measurements via box plots:
% distance_root_factor = [1, 2, 3];
% step_size = [0.2, 0.5, 1, 2, 3, 5];

distance_root_factor = 2; step_size = 1;
distance_step = step_size*4^(1/distance_root_factor);
figure(13); set(gcf,'Position', get(0, 'Screensize'));
suptitle({['Correlation Between "Location distance" and "RSSI distance"']; ['distance root factor = ' num2str(distance_root_factor/2) ', distance step size = ' num2str(distance_step)]});

boxplot(S_Euc_rssi(:),floor((S_Euc_loc(:).^(1/distance_root_factor))/distance_step)*distance_step);
title('"RSSI distance"'); xlabel(['Location distance [m]']); ylabel('RSSI distance')

distance_root_factor = 2; step_size = 2;
distance_step = step_size*4^(1/distance_root_factor);
figure(14); set(gcf,'Position', get(0, 'Screensize'));
suptitle({['Correlation Between "Location distance" and "RSSI distance"']; ['distance root factor = ' num2str(distance_root_factor/2) ', distance step size = ' num2str(distance_step)]});

boxplot(S_Euc_rssi(:),floor((S_Euc_loc(:).^(1/distance_root_factor))/distance_step)*distance_step);
title('"RSSI distance"'); xlabel(['Location distance [m]]']); ylabel('RSSI distance')

distance_root_factor = 4; step_size = 1;
distance_step = step_size*4^(1/distance_root_factor);
figure(15); set(gcf,'Position', get(0, 'Screensize'));
suptitle({['Correlation Between "Location distance" and "RSSI distance"']; ['distance root factor = ' num2str(distance_root_factor/2) ', distance step size = ' num2str(distance_step)]});

boxplot(S_Euc_rssi(:),floor((S_Euc_loc(:).^(1/distance_root_factor))/distance_step)*distance_step);
title('"RSSI distance"'); xlabel(['Location distance [m^{1/2}]']); ylabel('RSSI distance')

% subplot(1,2,1);
% boxplot(S_Euc_rssi(:),floor((S_Euc_loc(:).^(1/distance_root_factor))/distance_steps)*distance_steps);
% title('linear "RSSI distance"'); xlabel('Location distance [m]'); ylabel('RSSI distance')

% subplot(1,2,2); boxplot(exp(-1e-6*S_Euc_rssi(:)),floor((S_Euc_loc(:).^(1/distance_root_factor))/distance_steps)*distance_steps);
% title('exponential "RSSI distance"'); xlabel('Location distance [m]'); ylabel('RSSI distance')