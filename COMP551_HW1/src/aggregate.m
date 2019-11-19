t1_final_result_bayes = zeros(8711, 4);
j = 1;
for i=1:8653
   t1_final_result_bayes(prediction_matrix(i, 6)+1, 3) = prediction_matrix(i, 7);
   t1_final_result_bayes(prediction_matrix(i, 6)+1, 2) = p(i);
end

t1_final_result_bayes(1:end, 4) = NaN;
for i=1:7535
   t1_final_result_bayes(PRED(i, 2), 4) = PRED(i, 1);
end

for i=1:8711
   if isnan(t1_final_result_bayes(i, 4)) 
       t1_final_result_bayes(i, 4) = normrnd(mean(PRED(1:end, 1)), var(PRED(1:end, 1)));
   end
end
t1_final_result_bayes(1:end, 1) = 0:8710;
disp(sum(t1_final_result_bayes(1:end, 3)));

final = cell(8711,4);
for i=1:8711
    t(1) = floor(t1_final_result_bayes(i, 4));
    t(2) = floor((t1_final_result_bayes(i,4) - t(1)) * 60);
    t(3) = floor((t1_final_result_bayes(i,4) - t(1) - t(2)/60) * 3600);
    if t(1) < 10
        str{1} = sprintf('0%d:', t(1));
    else
        str{1} = sprintf('%d:', t(1));
    end
    if t(2) < 10
        str{2} = sprintf('0%d:', t(2));
    else
        str{2} = sprintf('%d:', t(2));
    end
    if t(3) < 10
        str{3} = sprintf('0%d', t(3));
    else
        str{3} = sprintf('%d', t(3));
    end
    final{i, 1} = t1_final_result_bayes(i, 1);
        final{i, 2} = t1_final_result_bayes(i, 2);
            final{i, 3} = t1_final_result_bayes(i, 3);
    final{i, 4} = strcat(str{1}, str{2}, str{3});
end

fid = fopen('prediction.csv', 'w');
for i=1:8711
   fprintf(fid, '%d,', final{i, 1});
   fprintf(fid, '%d,', final{i, 2}); 
   fprintf(fid, '%d,', final{i, 3}); 
   fprintf(fid, '%s\r\n', final{i, 4}); 
end