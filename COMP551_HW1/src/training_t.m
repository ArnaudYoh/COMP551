function [neww,Loss,i,Ti,Vi,bestFscoreT,bestFscoreV] = training_t(X,w,y,lambda,~,learningRate,mode,limit,X1,y1,X2,yC)
%traingDecay = 0.5;
pLimit = 76;
v = zeros(size(w));
momentum = 0.;
bottomlimit = size(find(y ==1),1) * limit;
i = 1;
bestFscoreT = 0;
Ti = 0;
bestFscoreV = 0;
Vi = 0;
while true
    [Loss,grad] = logisiticRegression(X,y,w,lambda);
    [neww,m1,v1] = Adam(w,grad,learningRate,m1,v1,i); 
    [F_scoreT, F_scoreV,p_train, p_val] = FscoreCollection(X,y,X1,y1,neww);    
    p = predict(X2,neww);
    p = p(34613:end,:);
    simi = size(intersect(find(yC == 1),find(p == 1)),1);
    sp = size(find(p == 1),1);
    
    if p_train  >= pLimit ||  p_val >= pLimit
        fprintf('\n At itertion: %d, F1 score for train is %f, F1 score for val is %f, training accuracy is: %f, val accuracy is: %f, number of Sp is: %d, simi is %f',i,F_scoreT,F_scoreV,p_train, p_val,sp,simi);
        fprintf('\n Div: %f',simi / sp *100);
    end
    if F_scoreT > bestFscoreT
        bestFscoreT = F_scoreT;
        Ti = i;
    end
    if F_scoreV > bestFscoreV
        bestFscoreT = F_scoreT;
        Vi = i;
    end
    p  = predict(X,neww);
    if bottomlimit > size(find(p == 1),1)
        break;
    end
    w = neww;
    i  = i + 1;
end
pause;
end