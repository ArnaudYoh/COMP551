function [Loss, grad] = logisiticRegression(X,y,w,lambda)

% 

% Our X will include the bias b
% size of X is (# of Id * 3) * 4
% size of Theta is 4 * 1
% the output size will be (# of Id * 3) * 1
% all those code has been vectorized

[m,~] = size(X);
h = sigmoid(X * w);
reg = (lambda/(2*m)).*sum(w(2:end,1).^2);
Loss = (1/m).*sum((-y)'*log(h)-(1-y)'*log(1-h))+reg;

tmp = w;
% bias doesnt need to be calculated
tmp(1) = 0;
grad = (1/m).*(X'*(h-y) + lambda.*tmp);

end