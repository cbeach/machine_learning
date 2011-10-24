function [theta, J_history, theta_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);



theta_history = theta;

for iter = 1:num_iters
	
    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCost) and gradient here.
    %
	%can't be sure you don't have a script to enforce where our code goes

	h = X * theta; 
	tempTheta = theta;
	tempTheta(1) = theta(1) .- (alpha * (1/m) * sum((h .- y) .* X(:,1)));
	tempTheta(2) = theta(2) .- (alpha * (1/m) * sum((h .- y) .* X(:,2)));
	theta = tempTheta;
%	theta_history = [theta_history, theta];
    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCost(X, y, theta);

end

end
