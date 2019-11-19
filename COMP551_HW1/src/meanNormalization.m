function [normalize, me, STD] = meanNormalization(X)

me = mean(X);
STD = std(X);
a = bsxfun(@minus,X,me);
normalize = bsxfun(@rdivide,a,STD);
normalize = [ones(size(normalize(:,1))), normalize];
end