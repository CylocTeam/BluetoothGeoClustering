function [DataMatrix_new] = LaplacianEigenmapsExtraction(DataMatrix,alpha_scaling)
% This Function Extracts the 3 eigenvectors given by the
% Laplacian-Eigenmaps algorithm, using a Gaussian kernel (RBF).
% 
% Inputs:
% * DataMatrix - #Samples x #Features .
% * alpha_scaling - scaling factor for the Gaussian kernel.
% Output:
% * DataMatrix_new - new representation for the input data.

S_Euc = DiffMatrixExtraction(DataMatrix);

S = exp(-alpha_scaling*S_Euc);
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

DataMatrix_new = V(:,2:4);
end

