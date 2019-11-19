function iter = cross_val2(X_pred,X_train,X_val,w,y_train,y_val,mode,lambda,learningRate,limit,yC)
    [neww,~,iter,Ti,Vi,F_scoreT,F_scoreV] = training_t(X_train,w,y_train,lambda,500,learningRate,mode,limit,X_val,y_val,X_pred,yC);
    % precision (true positive / no. of predicted positive) and recall
    % (true positive / no, of actual positive)
    fprintf('\n F1 Best score for train is %f,index is %d, F1 Best score for val is %f, index is %d',F_scoreT,Ti,F_scoreV,Vi);
    %one_val= size(find(predict(X_val,neww)),1);
    p = predict(X_pred,neww);
    p = p(34613:end,:);
    sp = size(find(p == 1),1);
    fprintf('\n pred has: %f one, one is: %f, i is: %f',size(find(p == 1),1),iter);
end