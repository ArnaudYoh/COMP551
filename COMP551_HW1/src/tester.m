% TESTER

function cellarr = tester(x,y,input) 
    cellarr = {};
    for i=3:2:5
        order = higher_order(x,i); 
        w = closed_form(order,y); 
        order2 = higher_order(input,i); 
        order2 = [ones(size(order2(:,1))) order2]; 
        cellarr{i} = order2*w;
        square = 0; 
        for j=1:size(cellarr{i}(:,1))
            square = square + (input(j,6)-cellarr{i}(j,1))^2;
        end 
        disp(i);
        disp(square); 
    end 
end 