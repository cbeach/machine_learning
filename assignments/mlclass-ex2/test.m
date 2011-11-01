function Reg n = size(theta); 
	sum = 0; 
	for i = 1:m, 
		hyp = 0;
		for j= 1:n, 
			hyp = hyp + theta(j)X(i,j); 
		end 
		xx(i) = sigmoid(hyp); 
		yl = y(i)log(xx(i)); 
		J = J + -y(i)log(xx(i)) - (1-y(i))log(1-xx(i)); 
	end 

	for j= 2:n, 
		lsum = lsum + theta(j)theta(j); 
	end 
	J = J/m + lsum/2/m;
end
