function dF = different(F,x,dim)
%DIFFERENT Approximate derivative.
%   DF = DIFFERENT(F,X,DIM) approximates the derivative of the ND array F
%   with respect to the coordinate vector X along the dimension DIM.
%   Default for DIM is the first non-singleton dimension.
%
%   DIFFERENT is an alternative to GRADIENT for non-uniform grids.
%   GRADIENT uses centered difference quotients and is suitable for
%   uniform grids only.
%
%   Example 1:
%       % For a parabola DIFFERENT is "exact"
%       x = cumsum(rand(7,1));
%       err1 = gradient(x.^2,x) - 2*x
%       err2 = different(x.^2,x) - 2*x
%   
%   Example 2:
%       % Gradient approximation
%       x = linspace(0,4*pi,25);
%       y = cumsum(rand(1,15));
%       [X,Y] = ndgrid(x,y);
%       F = sin(X/2).*cos(Y);
%       Fx = different(F,x);
%       Fy = different(F,y,2);
%
%   See also GRADIENT

%   Author: jonas.lundgren@saabgroup.com, 2009.

%   2011-07-01  Major speed up

if nargin < 1, help different, return, end

% Treat dimensions
sizeF = size(F);
maxdim = length(sizeF);
if nargin < 3
    % Find first non-singleton dimension
    dim = find(sizeF > 1,1);
    if isempty(dim)
        dim = maxdim;
    end
else
    % Check dimension
    if ~isscalar(dim) || dim < 1 || dim > maxdim || fix(dim) < dim
        error('different:baddim','Bad dimension!')
    end
end

% Treat coordinate vector
if nargin < 2 || isempty(x)
    % Create vector
    n = sizeF(dim);
    x = 1:n;
else
    % Check size along dimension
    n = numel(x);
    if sizeF(dim) ~= n
        error('different:badsize', ...
              'Length of X must equal size of F along dimension %d.',dim)
    end
end

% Trivial cases
if isempty(F) || n == 1
    % Empty or constant case
    dF = zeros(size(F),class(F));
    return
elseif n == 2
    % Linear case
    mnp = ones(1,maxdim);
    mnp(dim) = 2;
    dF = repmat(diff(F,1,dim)/diff(x),mnp);
    return
end

% Permute dimensions
if dim > 1 && dim < maxdim
	perm = [dim 1:dim-1 dim+1:maxdim];
	F = permute(F,perm);
	sizeF = size(F);
end

% Differentiate
if dim < maxdim
    % along first dimension
    F = reshape(F,n,[]);
    x = reshape(x,n,1);
    dF = diff1(F,x,n);
else
    % along last dimension
    F = reshape(F,[],n);
    x = reshape(x,1,n);
    dF = diff2(F,x,n);
end

% Reshape to ND
dF = reshape(dF,sizeF);

% Inverse permute dimensions
if dim > 1 && dim < maxdim
    dF = ipermute(dF,perm);
end


%--------------------------------------------------------------------------
function dF = diff1(F,x,n)
%DIFF1 Differentiate 2D array along dimension 1

ii = [1 1:n-1 2:n n];
jj = [2 1:n-1 1:n-1 n-2];
A = sparse(ii,jj,1);
B = sparse(ii,jj,[-1 -1 ones(1,2*n-4) -1 -1]);
C = sparse(ii,jj,[-1 ones(1,2*n-2) -1]);

% Differences
dx1 = diff(x,1,1);
dF1 = diff(F,1,1);
% Centered differences
dx2 = A*dx1;
dF2 = B*dF1;
% Quotients
dF1 = bsxfun(@rdivide,dF1,dx1);
dF2 = bsxfun(@rdivide,dF2,dx2);

% Approximate derivative
dF = C*dF1 - dF2;


%--------------------------------------------------------------------------
function dF = diff2(F,x,n)
%DIFF2 Differentiate 2D array along dimension 2

ii = [1 1:n-1 2:n n];
jj = [2 1:n-1 1:n-1 n-2];
A = sparse(jj,ii,1);
B = sparse(jj,ii,[-1 -1 ones(1,2*n-4) -1 -1]);
C = sparse(jj,ii,[-1 ones(1,2*n-2) -1]);

% Differences
dx1 = diff(x,1,2);
dF1 = diff(F,1,2);
% Centered differences
dx2 = dx1*A;
dF2 = dF1*B;
% Quotients
dF1 = bsxfun(@rdivide,dF1,dx1);
dF2 = bsxfun(@rdivide,dF2,dx2);

% Approximate derivative
dF = dF1*C - dF2;

