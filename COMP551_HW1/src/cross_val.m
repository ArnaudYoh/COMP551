function [lambda,learningRate] = cross_val(X_train,X_val,w,y_train,y_val,mode)
learningRateT = [1e-1,1e-2,1e-3,1e-4,1e-5];
lambdaT = [0.001,0.005,0.01,0.05,0.1,0.5,1,5];
bestP = 0;
highestOne_val = 0;
bestlearningRateI = 0;
bestlambdaI = 0;
for i = 1 : length(learningRateT)
    for j = 1 : length(lambdaT)
         [neww,Loss] = training(X_train,w,y_train,lambdaT(j),500,learningRateT(i),mode);
         p_train = mean(double(y_train == predict(X_train,neww)))*100;
         p_val = mean(double(y_val == predict(X_val,neww)))*100;
         one_val= size(find(predict(X_val,neww)));
         fprintf('\nWhen using lambda: %f, learningRate : %f, val accuracy is: %f, train accuracy is : %f, one is : %d',lambdaT(j),learningRateT(i),p_val,p_train,one_val);
         if bestP <= p_val
             if bestP == p_val
                 if one_val >  highestOne_val
                    highestOne_val = one_val;
                    bestP = p_val;
                    bestlearningRateI = i;
                    bestlambdaI = j;
                 end
             else
                bestP = p_val;
                bestlearningRateI = i;
                bestlambdaI = j;
             end
         end
    end
end
lambda = lambdaT(bestlambdaI);
learningRate = learningRateT(bestlearningRateI);
end