function [S_Euc] = DiffMatrixExtraction(DataMatrix)
% This Function Extracts the Difference-Matrix
% (aka Euclidean-Affinity-Matrix, aka Similarity-Matrix)
% of the input data.
% 
% Input:
% * DataMatrix - #Samples x #Features .
% Output:
% * S_Euc - Euclidean Difference Matix - #Samples x #Samples .

num_of_samples = size(DataMatrix,1);
S_Euc = zeros(num_of_samples,num_of_samples);
for n = 1:size(S_Euc,1)
    DataMatrix_n = DataMatrix(n,:);
    % Euclidean Kernel:
    S_Euc(n,:) = sum( (repmat(DataMatrix_n,num_of_samples,1) - DataMatrix).^2 ,2);
end
end

