x_mat = augmented_jeremy_matrix;
y_mat = augmented_y_matrix;

j = 1;
w = 1;
test_set_size = 0;
test_set = zeros(0, 7);
[x,y] = size(x_mat);

male = sum(x_mat(1:end, 3));
female = x - male;
male_p = 0;
female_p = 0;
for i=1:x
    if y_mat(i) && x_mat(i, 3)
        male_p = male_p + 1;
    elseif y_mat(i) && x_mat(i, 3) == 0
        female_p = female_p + 1;
    end 
end

male_p = male_p / male;
female_p = female_p / female;
training_set = zeros(0, 7);
for i=1:x
       if x_mat(i, 5) == 2016
           break;
       end
       if rand(1) > .95
          test_set(end+1, 1:6) = x_mat(i, 1:6); 
          test_set(end, 7) = y_mat(i, 1);  
          test_set_size = test_set_size + 1;
       else
          if y_mat(i)
            part(j, 1:6) = x_mat(i, 1:6);
            j = j+1;
          else
            non_part(w, 1:6) = x_mat(i, 1:6);
            w = w+1;
          end
          training_set(end+1, 1:6) = x_mat(i, 1:6);
          training_set(end, 7) = y_mat(i, 1);  
       end
end
total = j + w - 2;
fprintf('%d %d %d %d\n', total + test_set_size, i, total, test_set_size);
for i=1:4
    part_table(i, 1) = mean(part(1:end, i));
    part_table(i, 2) = var(part(1:end, i));
    non_part_table(i, 1) = mean(non_part(1:end, i));
    non_part_table(i, 2) = var(non_part(1:end, i));
end

prob_p = j/(j+w);
prob_np = 1 - prob_p;
count_right = 0;
prob = zeros(4, 1);
[x, y] = size(training_set);

test_count1 = 0;
test_count2 = 0;
type_1 = 0;
type_2 = 0;
true_participants = 0;
for i=1:x
    if training_set(i, 5) == 2016
       break;
    end
    for j=1:4
        prob(j) = normal_dist(training_set(i, j), part_table(j, 1), part_table(j, 2));
    end
    if training_set(i, 3)
        prob(3) = male_p;
    else
        prob(3) = female_p;
    end
    prob_true = prob(1) * prob(2) * prob(3) * prob(4) * prob_p;
    for j=1:4
        prob(j) = normal_dist(training_set(i, j), non_part_table(j, 1), non_part_table(j, 2));
    end
    prob_false = prob(1) * prob(2) * prob(3) * prob(4) * prob_np;
    if training_set(i, 3)
        prob(3) = 1 - male_p;
    else
        prob(3) = 1 - female_p;
    end
    if prob_true > prob_false
        prediction = 1;
        test_count1 = test_count1 + 1;
    else
        prediction = 0;
        test_count2 = test_count2 + 1;
    end 
    if prediction == training_set(i, 7)
        count_right = count_right + 1;
    elseif prediction
        type_1 = type_1 + 1;
    else
        type_2 = type_2 + 1;
    end
    
    if training_set(i, 7)
        true_participants = true_participants + 1;
    end
end
disp('Training Set');
disp(i);
disp(test_count1);
disp(test_count2);
disp(count_right/i);
disp(sum(training_set(1:end, 7)));
disp(x - sum(training_set(1:end, 7)));
fprintf('Error: %d %d\n', type_1, type_2);

type_1 = 0;
type_2 = 0;
[x, y] = size(test_set);
predicted_true = 0;
predicted_false = 0;
count = 0;
for i=1:x
    for j=1:4
        prob(j) = normal_dist(test_set(i, j), part_table(j, 1), part_table(j, 2));
    end
    if test_set(i, 3)
        prob(3) = male_p;
    else
        prob(3) = female_p;
    end
    prob_true = prob(1) * prob(2) * prob(3) * prob(4) * prob_p;
    for j=1:4
        prob(j) = normal_dist(test_set(i, j), non_part_table(j, 1), non_part_table(j, 2));
    end
    if test_set(i, 3)
        prob(3) = 1 - male_p;
    else
        prob(3) = 1 - female_p;
    end
    prob_false = prob(1) * prob(2) * prob(3) * prob(4) * prob_np;
    if prob_true > prob_false
        predicted_true = predicted_true + 1;
        prediction = 1;
    else
        predicted_false = predicted_false + 1;
        prediction = 0;
    end
    if prediction == test_set(i, 7)
        count = count + 1;        
    elseif prediction
        type_1 = type_1 + 1;
    else
        type_2 = type_2 + 1;
    end
end
disp('Test Set');
disp(x);
disp(predicted_true);
disp(predicted_false);
disp(sum(test_set(i:end, 7)));
disp(x - sum(test_set(i:end, 7)));
disp(count/x);
disp(sum(test_set(1:end, 7)));
fprintf('Error: %d %d\n', type_1, type_2);
predicted_true = 0;
predicted_false = 0;
prediction_matrix = zeros(0, 7);
type_1 = 0;
type_2 = 0;
pred = 0;
[x, y] = size(x_mat);
for i=1:x
    if x_mat(i, 5) ~= 2016
       continue;
    end
    for j=1:4
        prob(j) = normal_dist(x_mat(i, j), part_table(j, 1), part_table(j, 2));
    end
    if x_mat(i, 3)
        prob(3) = male_p;
    else
        prob(3) = female_p;
    end
    prob_true = prob(1) * prob(2) * prob(3) * prob(4) * prob_p;
    for j=1:4
        prob(j) = normal_dist(x_mat(i, j), non_part_table(j, 1), non_part_table(j, 2));
    end
    if x_mat(i, 3)
        prob(3) = 1 - male_p;
    else
        prob(3) = 1 - female_p;
    end
    prob_false = prob(1) * prob(2) * prob(3) * prob(4) * prob_np;
    
    if prob_true > prob_false
        predicted_true = predicted_true + 1;
        prediction = 1;
    else
        predicted_false = predicted_false + 1;
        prediction = 0;
    end
    prediction_matrix(pred+1, 1:6) = x_mat(i, 1:6);
    prediction_matrix(pred+1, 7) = prediction;
    pred = pred + 1;
end

disp('2016 Predictions');
disp(predicted_true);
disp(predicted_false);
