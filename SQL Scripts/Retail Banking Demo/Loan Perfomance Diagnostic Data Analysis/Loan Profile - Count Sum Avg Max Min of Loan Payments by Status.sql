SELECT status, 
	count(DISTINCT loan_id), sum(payments), avg(payments), max(payments), min(payments) 
FROM loan l
GROUP BY 1
ORDER BY 1;