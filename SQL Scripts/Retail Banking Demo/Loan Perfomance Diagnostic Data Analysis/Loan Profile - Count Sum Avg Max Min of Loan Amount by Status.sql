SELECT status, 
	count(DISTINCT loan_id), sum(amount), avg(amount), max(amount), min(amount) 
FROM loan l
GROUP BY 1
ORDER BY 1;