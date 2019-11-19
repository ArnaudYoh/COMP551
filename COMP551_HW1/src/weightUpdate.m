function [neww,newv] = weightUpdate(dx,w,learningRate,v,momentum)

newv = momentum * v - learningRate * dx;
neww  = w + newv;

end


