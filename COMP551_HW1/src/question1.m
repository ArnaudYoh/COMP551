% Question 1 
clc 
clear all
%% ------------------- part0: main control --------------------
% mode 1 : cross_val 
% mode 2 : real training
% mode 3 : prediction
% mode 4 : cross_val 2
mode =1;
order = 4;
weight_bal = 1;
%% ------------------- part1: data init and pre prcessing--------------------

pre_x = load('x_matrix.mat');
pre_y = load('y_matrix.mat');
pre_x = pre_x.augmented_jeremy_matrix();
pre_y = pre_y.augmented_y_matrix;
fprintf('Loading complete');
% get prediction part
pre_X_pred = pre_x;
pre_x = pre_x(pre_x(:,5) ~= 2016,:);
pre_y = pre_y(1:size(pre_x,1),:);

% order 
tmp_x = higher_order( pre_x, order );
tmp_X_pred = higher_order( pre_X_pred, order );

% mean normalization

[numberOfTest,numberOfFeatures] = size(tmp_x);
numberOfC = size(pre_y);

if numberOfC ~= numberOfTest
    fprintf('matrix error');
    pause;
else
    X =  meanNormalization(tmp_x);
    X_pred = meanNormalization(tmp_X_pred);
    y =  pre_y;
end

%% ------------------- part2: weight init --------------------
% Here, we use rand() function from matlab to init weight, 
% the reason is rand() returns uniformly distributed random number 
% which will help gradient decent convergent.

[a,b] = size(X);
[c,~] = size(y);
w = rand(b,1) * weight_bal;
%% ------------------- part3: cross val --------------------
if mode == 1
    lambda = 3;
    valN = round(a / 5);

    for i = 1 : 5
        ra = randperm(a,a);
        X_val = X(ra(1:valN),:);
        X_train = X(ra(valN : end),:);
        y_val = y(ra(1:valN),:);
        y_train = y(ra(valN:end),:);    
        fprintf('\n Test: %d',i);
        [lambda,learningRate] = cross_val(X_train,X_val,w,y_train,y_val,mode);
        fprintf('\nTest; %d, best lambda is : %f, best learningRate is %f',i,lambda,learningRate);
    end
    fprintf('cross_val end');
end


%% ------------------- part3.5:cross val 2 --------------------

if mode == 4
    yC = load('prediction.mat');
    yC = yC.prediction_matrix;
    yC = yC(:,7);
    limit = 0.05;
    lambda = 3;
    learningRate = 1e-3;
    valN = round(a / 5);
    maxOrder = 6;
    for i = 1 : 5
        for j = 1: maxOrder
            ra = randperm(a,a);
            X_val = meanNormalization(higher_order(pre_x(ra(1:valN),:),j));
            X_train = meanNormalization(higher_order(pre_x(ra(valN : end),:),j));
            y_val = pre_y(ra(1:valN),:);
            y_train = pre_y(ra(valN:end),:);
            X_pred = meanNormalization(higher_order(pre_X_pred,j));
            w = rand(size(X_val,2),1);
            iter  = cross_val2(X_pred,X_train,X_val,w,y_train,y_val,mode,lambda,learningRate,limit,yC);
            fprintf('\nTest; %d, Order: %d, Iteration is: %d,limit is %f',i,j,iter,limit);
        end
    end
    fprintf('cross_val end');
end

%% ------------------- part4:training--------------------
if mode == 2    
    lambda = 5;
    Iteration = 3000;
    learningRate = 1e-2;
    [neww, Loss]= training1(X,w,y,lambda,Iteration,learningRate,mode,X_pred);
    %neww = closedForm(X,y);
    p  = predict(X,neww);
    size(find(p == 1))
    size(find(y ==1))
    fprintf('\nTraining accuracy is: %f now',mean(double(y == p))*100);
    fprintf('real training end');
end

%% ------------------- part5: predict --------------------
if mode == 3 || mode == 2
   % plotDecisionBoundary(neww, X, y);
    p = predict(X_pred,neww);
    pure = purepredict(X_pred,neww);
    p = p(34613:end,:);
    save 'Question1.mat' p;
    fprintf('prediction end');
    size(find(p == 1))
end




