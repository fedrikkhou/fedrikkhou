SELECT status, purpose, 
	count(DISTINCT loan_id) 
FROM loan l 
GROUP BY 1, 2
ORDER BY 1, 3 DESC ,  2;