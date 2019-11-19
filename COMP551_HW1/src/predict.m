function p = predict(X,w)

p = round(sigmoid(X * w));

end