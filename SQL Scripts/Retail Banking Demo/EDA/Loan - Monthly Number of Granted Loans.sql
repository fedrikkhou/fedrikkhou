SELECT date_trunc('month', granted_date),
	count(DISTINCT loan_id) 
FROM loan l 
GROUP BY 1 
ORDER BY 1;