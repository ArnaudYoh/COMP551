function [neww,Loss] = training(X,w,y,lambda,Iteration,learningRate,mode)
traingDecay = 0.5;
v = zeros(size(w));
momentum = 0.;
for i = 1 : Iteration
    [Loss,grad] = logisiticRegression(X,y,w,lambda);
    [neww,v] = weightUpdate(grad,w,learningRate,v,momentum);
    w = neww;
    if mode ~= 1
        fprintf('\nAt iteration: %d, the Loss is: %f, learningRate is: %f, traing accuracy is : %f\n',...
                i,Loss,learningRate,mean(double(y == predict(X,neww)))*100);
    end
    if mod(i,20000) == 0
        learningRate = learningRate * traingDecay;
    end
end