SELECT date_trunc('month', issued_date), 
	count(DISTINCT card_id) 
FROM card c 
GROUP BY 1 
ORDER BY 1;
