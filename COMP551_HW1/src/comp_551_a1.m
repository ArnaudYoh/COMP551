fileID = fopen('Project1_data.csv', 'r');
first_level_matrix = {};
i = 1;
while true
    disp(i);
    file_line = fgetl(fileID);
    if file_line == -1
        break;
    else
       first_level_matrix =  process_line(file_line, first_level_matrix);
        i = i + 1;
    end
end

fclose(fileID);

for i=1:26961
   remove_value(first_level_matrix(i, 3), '-');
   remove_value(first_level_matrix(i, 4), '-');
   first_level_matrix{i, 3} = lower(first_level_matrix{i, 3});
   first_level_matrix{i, 4} = lower(first_level_matrix{i, 4});
end


[x, y] = size(first_level_matrix);

for i=1:x
    first_level_matrix{i, 1} = str2double(first_level_matrix{i, 1});
end

for w=1:x
    disp(w);
    first_level_matrix{w, 8} = find_distance_type(first_level_matrix{w, 4});
end

years = [[2012,09,23];[2013,09,22]; [2014,09,28]; [2015,09,20]; [2016,09,25]];

 for w=1:26961
     disp(w);
        tokens = str2double(strsplit(first_level_matrix{w, 2}, '-'));
        for i=1:5
            if tokens(1) <= years(i, 1) 
                if tokens(2) <= years(i, 2) || tokens(1) < years(i, 1) 
                    if tokens(3) < years(i, 3) || tokens(2) < years(i, 2) || tokens(1) < years(i, 1) 
                        switch i
                            case 1 
                                   first_level_matrix{w, 7} = 2012;
                            case 2 
                                   first_level_matrix{w, 7} = 2013;
                            case 3 
                                   first_level_matrix{w, 7} = 2014;
                            case 4 
                                   first_level_matrix{w, 7} = 2015;
                            case 5 
                                   first_level_matrix{w, 7} = 2016;
                        end
                        break;
                    end
                end
            end
        end
 end
first_level_matrix(1, 1) = 0;
[x, y] = size(first_level_matrix);
years = ['2012', '2013', '2014', '2015', '2016'];
x_matrix = NaN(5, 8711, 6);
x_matrix(1:5, 1:8711, 1:2) = 0;

for i=1:x
   disp(i);
   switch first_level_matrix{i, 7}
       case 2012
            if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal')) == 1 && (first_level_matrix{i, 8} >=  42)
                x_matrix(1, (first_level_matrix{i, 1})+1, 1) = x_matrix(1, (first_level_matrix{i, 1})+1, 1) + 1;
            else
                x_matrix(1, (first_level_matrix{i, 1})+1, 2) = x_matrix(1, (first_level_matrix{i, 1})+1, 2) + 1;
            end
            gender_age = first_level_matrix{i, 6};
            if ~isempty(gender_age) && isnan(x_matrix(1, (first_level_matrix{i, 1})+1, 3))
                if gender_age(1) == 'M'
                    x_matrix(1, (first_level_matrix{i, 1})+1, 3) = 0;
                else
                    x_matrix(1, (first_level_matrix{i, 1})+1, 3) = 1;
                end
                tokens = strsplit(gender_age(2:end), '-');
                if length(tokens) == 1
                    x_matrix(1, (first_level_matrix{i, 1})+1, 4) = str2double(tokens(1));
                elseif length(tokens) == 2
                    x_matrix(1, (first_level_matrix{i, 1})+1, 4) = (str2double(tokens(1)) + str2double(tokens(2)))/2;
                end
            end
       case 2013
            if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal')) == 1 && (first_level_matrix{i, 8} >=  42)
                x_matrix(2, (first_level_matrix{i, 1})+1, 1) = x_matrix(2, (first_level_matrix{i, 1})+1, 1) + 1;
            else
                x_matrix(2, (first_level_matrix{i, 1})+1, 2) = x_matrix(2, (first_level_matrix{i, 1})+1, 2) + 1;
            end
            gender_age = first_level_matrix{i, 6};
            if ~isempty(gender_age) && isnan(x_matrix(2, (first_level_matrix{i, 1})+1, 3))
                if gender_age(1) == 'M'
                    x_matrix(2, (first_level_matrix{i, 1})+1, 3) = 0;
                else
                    x_matrix(2, (first_level_matrix{i, 1})+1, 3) = 1;
                end
                tokens = strsplit(gender_age(2:end), '-');
                if length(tokens) == 1
                    x_matrix(2, (first_level_matrix{i, 1})+1, 4) = str2double(tokens(1));
                elseif length(tokens) == 2
                    x_matrix(2, (first_level_matrix{i, 1})+1, 4) = (str2double(tokens(1)) + str2double(tokens(2)))/2;
                end
            end
       case 2014
            if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal')) == 1 && (first_level_matrix{i, 8} >=  42)
                x_matrix(3, (first_level_matrix{i, 1})+1, 1) = x_matrix(3, (first_level_matrix{i, 1})+1, 1) + 1;
            else
                x_matrix(3, (first_level_matrix{i, 1})+1, 2) = x_matrix(3, (first_level_matrix{i, 1})+1, 2) + 1;
            end
            gender_age = first_level_matrix{i, 6};
            if ~isempty(gender_age) && isnan(x_matrix(3, (first_level_matrix{i, 1})+1, 3))
                if gender_age(1) == 'M'
                    x_matrix(3, (first_level_matrix{i, 1})+1, 3) = 0;
                else
                    x_matrix(3, (first_level_matrix{i, 1})+1, 3) = 1;
                end
                tokens = strsplit(gender_age(2:end), '-');
                if length(tokens) == 1
                    x_matrix(3, (first_level_matrix{i, 1})+1, 4) = str2double(tokens(1));
                elseif length(tokens) == 2
                    x_matrix(3, (first_level_matrix{i, 1})+1, 4) = (str2double(tokens(1)) + str2double(tokens(2)))/2;
                end
            end
       case 2015
            if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal')) == 1 && (first_level_matrix{i, 8} >=  42)
                x_matrix(4, (first_level_matrix{i, 1} + 1), 1) = x_matrix(4, (first_level_matrix{i, 1})+1, 1) + 1;
            else
                x_matrix(4, (first_level_matrix{i, 1} + 1), 2) = x_matrix(4, (first_level_matrix{i, 1})+1, 2) + 1;
            end
            gender_age = first_level_matrix{i, 6};
            if ~isempty(gender_age) && isnan(x_matrix(4, (first_level_matrix{i, 1})+1, 3))
                if gender_age(1) == 'M'
                    x_matrix(4, (first_level_matrix{i, 1})+1, 3) = 0;
                else
                    x_matrix(4, (first_level_matrix{i, 1})+1, 3) = 1;
                end
                tokens = strsplit(gender_age(2:end), '-');
                if length(tokens) == 1
                    x_matrix(4, (first_level_matrix{i, 1})+1, 4) = str2double(tokens(1));
                elseif length(tokens) == 2
                    x_matrix(4, (first_level_matrix{i, 1})+1, 4) = (str2double(tokens(1)) + str2double(tokens(2)))/2;
                end
            end
       case 2016
            if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal')) == 1 && (first_level_matrix{i, 8} >=  42)
                x_matrix(5, (first_level_matrix{i, 1})+1, 1) = x_matrix(5, (first_level_matrix{i, 1})+1, 1) + 1;
            else
                x_matrix(5, (first_level_matrix{i, 1})+1, 2) = x_matrix(5, (first_level_matrix{i, 1})+1, 2) + 1;
            end
            gender_age = first_level_matrix{i, 6};
            if ~isempty(gender_age) && isnan(x_matrix(5, (first_level_matrix{i, 1})+1, 3))
                if gender_age(1) == 'M'
                    x_matrix(5, (first_level_matrix{i, 1})+1, 3) = 0;
                else
                    x_matrix(5, (first_level_matrix{i, 1})+1, 3) = 1;
                end
                tokens = strsplit(gender_age(2:end), '-');
                if length(tokens) == 1
                    x_matrix(5, (first_level_matrix{i, 1})+1, 4) = str2double(tokens(1));
                elseif length(tokens) == 2
                    x_matrix(5, (first_level_matrix{i, 1})+1, 4) = (str2double(tokens(1)) + str2double(tokens(2)))/2;
                end
            end
       otherwise
           error('life sucks');
   end
end
% normalizing the ages

for i=1:5
    x_matrix(i, 1:end, 5) = i + 2011;
    x_matrix(i, 1:end, 6) = 0:8710;
end

for i=1:8711
    for w=1:5
           if ~isnan(x_matrix(w, i, 4))
                x_matrix(1, i, 4) = x_matrix(w, i, 4) + 1 - w;
                x_matrix(2, i, 4) = x_matrix(w, i, 4) + 2 - w;
                x_matrix(3, i, 4) = x_matrix(w, i, 4) + 3 - w;
                x_matrix(4, i, 4) = x_matrix(w, i, 4) + 4 - w;
                x_matrix(5, i, 4) = x_matrix(w, i, 4) + 5 - w;
                %fprintf('%d %d %d %d %d\n', x_matrix(1, i, 4), x_matrix(2, i, 4), x_matrix(3, i, 4), x_matrix(4, i, 4), x_matrix(5, i, 4));
                break;
           end
    end
end

for i=1:8711
    for w=1:5
           if ~isnan(x_matrix(w, i, 3))
                x_matrix(1:5, i, 3) = x_matrix(w, i, 3);
                %fprintf('%d %d %d %d %d\n', x_matrix(1, i, 4), x_matrix(2, i, 4), x_matrix(3, i, 4), x_matrix(4, i, 4), x_matrix(5, i, 4));
                break;
           end
    end
end
%for the y_matrix
for i=1:5
    jeremy_matrix(((i-1) * 8711 + 1):(i *8711), 1:5) = x_matrix(i, 1:8711, 1:5);
end

y_matrix = zeros(43555, 1);
y_matrix(1:(8711*4 + 1)) = jeremy_matrix(8711:end, 1);


%{
for j=1:8711
    for i=2:5
        if ~isnan(x_matrix(i-1, j, 1))
            x_matrix(i, j, 1) = x_matrix(i, j, 1) + x_matrix(i-1, j, 1);
        end
        if ~isnan(x_matrix(i-1, j, 2))
            x_matrix(i, j, 2) = x_matrix(i, j, 2) + x_matrix(i-1, j, 2);
        end
    end
end
%}

%New Weighted Distribution System
for k=1:1
for j=1:8711
    for i=2:5
        if ~isnan(x_matrix(i-1, j, 1))
            x_matrix(i, j, 1) = x_matrix(i, j, 1) + x_matrix(i-1, j, 1) * 1.5;
        end
        if ~isnan(x_matrix(i-1, j, 2))
            x_matrix(i, j, 2) = x_matrix(i, j, 2) + x_matrix(i-1, j, 2) * .67;
        end
    end
end
end


for i=1:5
    jeremy_matrix(((i-1) * 8711 + 1):(i *8711), 1:6) = x_matrix(i, 1:8711, 1:6);
end

j = 1;
augmented_jeremy_matrix = [];
augmented_y_matrix = [];
for i=1:43555
    if ~isnan(jeremy_matrix(i, 3)) && ~isnan(jeremy_matrix(i, 4))
        augmented_jeremy_matrix(j, 1:6) = jeremy_matrix(i, 1:end);
        augmented_y_matrix(j, 1) = y_matrix(i);
        j = j+1;
    end
end

for i=1:6791
   if isnan(final_t2_matrix(i, 8))
      disp(final_t2_matrix(i, 1:8)); 
   end
end

%The beginning of T2 Data Scrapping

[x, y] = size(first_level_matrix);

for i=1:x
    found1 = strfind(first_level_matrix{i, 4}, 'demi-marathon');
    found2 = strfind(first_level_matrix{i, 4}, 'demi marathon');   
    found3 = strfind(first_level_matrix{i, 4}, 'half-marathon');    
    found4 = strfind(first_level_matrix{i, 4}, 'half marathon');
    if (length(found1) || length(found2) || length(found3) || length(found4)) && first_level_matrix{i, 8} >= 20
        first_level_matrix{i, 4} = 'half-marathon';
    end
end


for i=1:x
   if length(strfind(first_level_matrix{i, 4}, 'marathon')) && first_level_matrix{i, 8} >= 40
       first_level_matrix{i, 4} = 'marathon';
   end
end

for i=1:x
   if ~strcmp(first_level_matrix{i, 5}, '-1')
       tokens = strsplit(first_level_matrix{i, 5}, ':');
       if length(tokens) ~= 3
           disp(i)
           break;
       end
       list = str2double(tokens(1:3));
       first_level_matrix{i, 9} = list(1) + list(2)/60 + list(3)/(3600);
   else
       first_level_matrix{i, 9} = -1;
   end
end

t2_x_matrix = NaN(5, 8711, 9);
t2_x_matrix(1:5, 1:8711, 3:7) = 0;


for i=1:x
   disp(i);
   switch first_level_matrix{i, 7}
       case 2012
           if (strcmp(first_level_matrix{i,4}, 'half-marathon') == 1)
                t2_x_matrix(1, first_level_matrix{i, 1} + 1, 3) =  t2_x_matrix(1, first_level_matrix{i, 1} + 1, 3) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 4.5;
                end
                t2_x_matrix(1, first_level_matrix{i, 1} + 1, 4) =  t2_x_matrix(1, first_level_matrix{i, 1} + 1, 4) + first_level_matrix{i, 9};
           elseif (strcmp(first_level_matrix{i,4}, 'marathon') == 1 || (isempty(strfind(first_level_matrix{i, 3}, 'marathon')) && first_level_matrix{i, 8} >= 40))
                t2_x_matrix(1, first_level_matrix{i, 1} + 1, 5) =  t2_x_matrix(1, first_level_matrix{i, 1} + 1, 5) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 7;
                end
                t2_x_matrix(1, first_level_matrix{i, 1} + 1, 6) =  t2_x_matrix(1, first_level_matrix{i, 1} + 1, 6) + first_level_matrix{i, 9};           
           end
       case 2013
           if (strcmp(first_level_matrix{i,4}, 'half-marathon') == 1)
                t2_x_matrix(2, first_level_matrix{i, 1} + 1, 3) =  t2_x_matrix(2, first_level_matrix{i, 1} + 1, 3) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 4.5;
                end
                t2_x_matrix(2, first_level_matrix{i, 1} + 1, 4) =  t2_x_matrix(2, first_level_matrix{i, 1} + 1, 4) + first_level_matrix{i, 9};
           elseif (strcmp(first_level_matrix{i,4}, 'marathon') == 1 || (isempty(strfind(first_level_matrix{i, 3}, 'marathon')) && first_level_matrix{i, 8} >= 40))
                t2_x_matrix(2, first_level_matrix{i, 1} + 1, 5) =  t2_x_matrix(2, first_level_matrix{i, 1} + 1, 5) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 7;
                end
                t2_x_matrix(2, first_level_matrix{i, 1} + 1, 6) =  t2_x_matrix(2, first_level_matrix{i, 1} + 1, 6) + first_level_matrix{i, 9};           
                if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal'))
                    t2_x_matrix(1, first_level_matrix{i, 1} + 1, 8) = first_level_matrix{i, 9};
                end
           end
       case 2014
           if (strcmp(first_level_matrix{i,4}, 'half-marathon') == 1)
                t2_x_matrix(3, first_level_matrix{i, 1} + 1, 3) =  t2_x_matrix(3, first_level_matrix{i, 1} + 1, 3) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 4.5;
                end
                t2_x_matrix(3, first_level_matrix{i, 1} + 1, 4) =  t2_x_matrix(3, first_level_matrix{i, 1} + 1, 4) + first_level_matrix{i, 9};
           elseif (strcmp(first_level_matrix{i,4}, 'marathon') == 1 || (isempty(strfind(first_level_matrix{i, 3}, 'marathon')) && first_level_matrix{i, 8} >= 40))
                t2_x_matrix(3, first_level_matrix{i, 1} + 1, 5) =  t2_x_matrix(3, first_level_matrix{i, 1} + 1, 5) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 7;
                end
                t2_x_matrix(3, first_level_matrix{i, 1} + 1, 6) =  t2_x_matrix(3, first_level_matrix{i, 1} + 1, 6) + first_level_matrix{i, 9};           
                if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal'))
                    t2_x_matrix(2, first_level_matrix{i, 1} + 1, 8) = first_level_matrix{i, 9};
                end
           end
       case 2015
           if (strcmp(first_level_matrix{i,4}, 'half-marathon') == 1)
                t2_x_matrix(4, first_level_matrix{i, 1} + 1, 3) =  t2_x_matrix(4, first_level_matrix{i, 1} + 1, 3) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 4.5;
                end
                t2_x_matrix(4, first_level_matrix{i, 1} + 1, 4) =  t2_x_matrix(4, first_level_matrix{i, 1} + 1, 4) + first_level_matrix{i, 9};
           elseif (strcmp(first_level_matrix{i,4}, 'marathon') == 1 || (isempty(strfind(first_level_matrix{i, 3}, 'marathon')) && first_level_matrix{i, 8} >= 40))
                t2_x_matrix(4, first_level_matrix{i, 1} + 1, 5) =  t2_x_matrix(4, first_level_matrix{i, 1} + 1, 5) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 7;
                end
                t2_x_matrix(4, first_level_matrix{i, 1} + 1, 6) =  t2_x_matrix(4, first_level_matrix{i, 1} + 1, 6) + first_level_matrix{i, 9};           
                if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal'))
                    t2_x_matrix(3, first_level_matrix{i, 1} + 1, 8) = first_level_matrix{i, 9};
                end
           end
       case 2016
           if (strcmp(first_level_matrix{i,4}, 'half-marathon') == 1)
                t2_x_matrix(5, first_level_matrix{i, 1} + 1, 3) =  t2_x_matrix(5, first_level_matrix{i, 1} + 1, 3) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 4.5;
                end
                t2_x_matrix(5, first_level_matrix{i, 1} + 1, 4) =  t2_x_matrix(5, first_level_matrix{i, 1} + 1, 4) + first_level_matrix{i, 9};
           elseif (strcmp(first_level_matrix{i,4}, 'marathon') == 1 || (isempty(strfind(first_level_matrix{i, 3}, 'marathon')) && first_level_matrix{i, 8} >= 40))
                t2_x_matrix(5, first_level_matrix{i, 1} + 1, 5) =  t2_x_matrix(5, first_level_matrix{i, 1} + 1, 5) + 1;
                if first_level_matrix{i, 9} == -1;
                    first_level_matrix{i, 9} = 7;
                end
                t2_x_matrix(5, first_level_matrix{i, 1} + 1, 6) =  t2_x_matrix(5, first_level_matrix{i, 1} + 1, 6) + first_level_matrix{i, 9};           
                if length(strfind(first_level_matrix{i, 3}, 'marathon oasis')) == 1 && length(strfind(first_level_matrix{i, 3}, 'montreal'))
                    t2_x_matrix(4, first_level_matrix{i, 1} + 1, 8) = first_level_matrix{i, 9};
                end
           end
       otherwise
   end
end

t2_x_matrix(1:5, 1:end, 1:2) = x_matrix(1:5, 1:end, 3:4);
t2_x_matrix(1:5, 1:end, 7) = x_matrix(1:5, 1:end, 5);

for j=1:8711
    for i=2:5
        if ~isnan(t2_x_matrix(i-1, j, 1))
            t2_x_matrix(i, j, 3) = t2_x_matrix(i, j, 3) + t2_x_matrix(i-1, j, 3);
        end
        if ~isnan(t2_x_matrix(i-1, j, 2))
            t2_x_matrix(i, j, 4) = t2_x_matrix(i, j, 4) + t2_x_matrix(i-1, j, 4);
        end
        if ~isnan(t2_x_matrix(i-1, j, 1))
            t2_x_matrix(i, j, 5) = t2_x_matrix(i, j, 5) + t2_x_matrix(i-1, j, 5);
        end
        if ~isnan(t2_x_matrix(i-1, j, 2))
            t2_x_matrix(i, j, 6) = t2_x_matrix(i, j, 6) + t2_x_matrix(i-1, j, 6);
        end
    end
    for i=1:5
        if t2_x_matrix(i, j, 3) ~= 0
            t2_x_matrix(i, j, 4) = t2_x_matrix(i, j, 4) / t2_x_matrix(i, j, 3);
        end
        if t2_x_matrix(i, j, 5) ~= 0
            t2_x_matrix(i, j, 6) = t2_x_matrix(i, j, 6) / t2_x_matrix(i, j, 5);
        end
        t2_x_matrix(i, j, 9) = j;
    end
    
end

for j=1:8711
    for i=1:5
        t2_x_matrix(i, j, 3) = t2_x_matrix(i, j, 3) / i;
        t2_x_matrix(i, j, 5) = t2_x_matrix(i, j, 5) / i;
    end
end

for i=1:8711
   if (t2_x_matrix(5, i, 6) ~= 0)
    for j=1:4
        if t2_x_matrix(j, i, 6) == 0
            t2_x_matrix(j, i, 6) = t2_x_matrix(5, i, 6);
        end
        if t2_x_matrix(j, i, 4) == 0
            t2_x_matrix(j, i, 4) = t2_x_matrix(5, i, 6)/2;
        end
    end
   end
end

for i=1:5
    t2_matrix(((i-1) * 8711 + 1):(i *8711), 1:9) = t2_x_matrix(i, 1:8711, 1:9);
end

for i=1:43555
    if isnan(t2_matrix(i, 4)) && ~isnan(t2_matrix(i, 6))
        t2_matrix(i,4) = t2_matrix(i, 6)/2;
    end
end

i = 1;
count = 0;


for j=1:43555
    if isnan(t2_matrix(j,1)) || isnan(t2_matrix(j,2)) || isnan(t2_matrix(j,6)) || isnan(t2_matrix(j,8))
        count = count + 1;
    else
        final_t2_matrix(i, 1:9) = t2_matrix(j, 1:9);
        i = i + 1;
    end
end

t2_2016 = zeros(0, 9);

for j=1:43555
    if t2_matrix(j, 7) == 2016 && isnan(t2_matrix(j,8)) && (~isnan(t2_matrix(j,2)) && t2_matrix(j,6) ~= 0 && ~isnan(t2_matrix(j,1)))
        t2_2016(end+1, 1:9) = t2_matrix(j, 1:9);
        i = i + 1;
    end
end

