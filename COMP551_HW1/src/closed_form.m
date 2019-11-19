function w = closed_form(x,y)
    x = [ones(size(x(:,1))) x]; 
    w = pinv(x'*x)*x'*y; 
end 