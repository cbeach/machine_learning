function [J, grad] = costFunctionReg(theta, X, y, lambda)
	%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
	%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
	%   theta as the parameter for regularized logistic regression and the
	%   gradient of the cost w.r.t. to the parameters. 

	% Initialize some useful values
	m = length(y); % number of training examples
	lsum = 0;
	% You need to return the following variables correctly 
	J = 0;
	grad = zeros(size(theta));

	% ====================== YOUR CODE HERE ======================
	% Instructions: Compute the cost of a particular choice of theta.
	%               You should set J to the cost.
	%               Compute the partial derivatives and set grad to the partial
	%               derivatives of the cost w.r.t. each parameter in theta
		
	format long;	
	h = sigmoid(X * theta);

	'lambda'
	lambda

	J = J + 1/m * sum( -y' * log(h(:,1)) .- (1.-y)' * log(1.-h(:,1)))  
	for i = 2:size(h,2)
		J = J + 1/m * sum( -y' * log(h(:,i)) .- (1.-y)' * log(1.-h(:,i)))  
	end
%(lambda / (2*m)) * theta(i,:) * theta(i,:i)
	for i = 2:size(theta)
		lsum = lsum + theta(i,1) * theta(i,1);
	end

	J = J + (lambda / (2 * m)) * lsum;

	grad(1,1) = 1 / m * sum( (h .- y).*X(:,1));

	for j = 2:size(X,2)
		grad(j,1) = 1 / m * sum( (h .- y).*X(:,j) - lambda * theta(j,1));
	end





	% =============================================================

end
