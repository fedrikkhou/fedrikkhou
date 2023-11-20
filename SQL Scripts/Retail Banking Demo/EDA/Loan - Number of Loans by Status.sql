SELECT status, 
	count(DISTINCT loan_id) 
FROM loan l 
GROUP BY 1;