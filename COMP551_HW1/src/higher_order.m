% this code is from https://gist.github.com/almathie/53f955bfeb14c45e2638#file-higher_order-m-L1
function newX = higher_order( X, max_order )
    [~, n_vars] = size(X);
    stacked = zeros(0, n_vars);                     % this will collect all the coefficients...    
    for o = 1:max_order                             % for degree 1 polynomial to degree 'order'
      stacked = [stacked; mg_sums(n_vars, o)];
    end
    newX =[];
    size(find(stacked ~= 0));
    [a,b] = size(stacked);
    for i = 1:a
        for j = 1:b
            if stacked(i,j) ~= 0
                newX = [newX, X(:,j) .^ stacked(i,j)];
            end
        end
    end

    %log_newX = log(X) * stacked';                   % this is the sexy step!
                                                    % multiplying log of data matrix by the    
                                                    % matrix of all possible exponent combinations
                                                    % effectively raises terms to powers and multiplies them!

    %newX = exp(log_newX);                           % back to normal
end