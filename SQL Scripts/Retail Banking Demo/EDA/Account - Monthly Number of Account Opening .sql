SELECT date_trunc('month', a.creation_date), 
	count(DISTINCT account_id) 
FROM account a 
GROUP BY 1 
ORDER BY 1