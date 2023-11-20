SELECT status, 
	date_part('year', granted_date),
	count(DISTINCT loan_id) 
FROM loan l 
GROUP BY 1, 2
ORDER BY 1, 2;