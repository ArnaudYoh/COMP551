function [neww,Loss] = training1(X,w,y,lambda,Iteration,learningRate,mode,X2)
%traingDecay = 0.5;
v = zeros(size(w));
momentum = 0.;
for i = 1 : Iteration
    [Loss,grad] = logisiticRegression(X,y,w,lambda); 
    [neww,v] = weightUpdate(grad,w,learningRate,v,momentum);
    pre_P = size(find(predict(X,neww) == 1),1);
    act_P = size(find(y == 1),1);
    trueP = size(intersect(find(y == 1),find(predict(X,neww) == 1)),1);
    P = trueP / pre_P;
    R = trueP / act_P;
    F_score = 2*(P*R)/(P + R);
    p = predict(X2,neww);
    p = p(34613:end,:);
    if size(find(p == 1),1) <= 650
        break 
    end
    w = neww;
    if mode ~= 1
        fprintf('\nAt iteration: %d, the Loss is: %f, learningRate is: %f, traing accuracy is : %f\n',...
                i,Loss,learningRate,mean(double(y == predict(X,neww)))*100);
    end
end