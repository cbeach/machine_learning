function [all_theta] = test_rig1()

	num_labels = 2;
	s = 5;
	X = magic(s);
	y = mod(min(magic(s)), num_labels)' + 1;

	[J Grad] = lrCostFunction(zeros(s,1), X, y, 0.1)
	all_theta = oneVsAll(X, y, num_labels, 0.1);
	predictOneVsAll(all_theta, X)

end
