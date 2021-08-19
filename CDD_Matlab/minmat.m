function [ minimum,index ] = minmat( array )
% Function: Calculate the minimum value and its indices in a multidimensional array
% -------- Logic description --------
% First of all, identify the Matlab convention for numbering the elements of a multi-dimensional array.
%   First are all the elements for the first dimension
%   Then the ones for the second and so on
% In each iteration, divide the number that identifies the minimum with the dimension under investigation
%   The remainder is the Index for this dimension (check for special cases below)
%   The integer is the "New number" that identifies the minimum, to be used for the next loop
% Repeat the steps as many times as the number of dimensions (e.g for a 2-by-3-by-4-by-5 table, repeat 4 times)
neldim      = size(array);              % Length of each dimension
ndim        = length(neldim);           % Number of dimensions
[minimum,I] = min(array(:));
remaining = 1;                          % Counter to evaluate the end of dimensions
index = [];                             % Initialize index
while remaining~=ndim+1                 % Break after the loop for the last dimension has been evaluated
    % Divide the integer with the the value of each dimension --> Identify at which group the integer belongs
    r       = rem(I,neldim(remaining)); % The remainder identifies the index for the dimension under evaluation
    int     = fix(I/neldim(remaining)); % The integer is the number that has to be used for the next iteration
    if r == 0                           % Compensate for being the last element of a "group" --> It index is equal to the dimension under evaluation
        new_index   = neldim(remaining);
    else                                % Compensate for the number of group --> Increase by 1 (e.g if remainder 8/3 = 2 and integer = 2, it means that you are at the 2+1 group in the 2nd position)
        int         = int+1;
        new_index   = r;
    end
    I     = int;                        % Adjust the new number for the division. This is the group th
    index = [index new_index];          % Append the current index at the end
    remaining = remaining + 1;
end
end