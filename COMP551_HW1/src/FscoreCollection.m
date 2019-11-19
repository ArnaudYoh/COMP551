function [F_scoreT, F_scoreV, p_train, p_val] = FscoreCollection(X_train,y_train,X_val,y_val,neww)
    pT = predict(X_train,neww);
    pV = predict(X_val,neww);
    p_train = mean(double(y_train == pT))*100;  
    pre_P = size(find(pT == 1),1);
    act_P = size(find(y_train == 1),1);
    trueP = size(intersect(find(y_train == 1),find(pT == 1)),1);
    P = trueP / pre_P;
    R = trueP / act_P;
    F_scoreT = 2*(P*R)/(P + R);
    p_val = mean(double(y_val == pV))*100;    
    pre_P = size(find(pV == 1),1);
    act_P = size(find(y_val == 1),1);
    trueP = size(intersect(find(y_val == 1),find(pV == 1)),1);
    P = trueP / pre_P;
    R = trueP / act_P;
    F_scoreV = 2*(P*R)/(P + R);    
end