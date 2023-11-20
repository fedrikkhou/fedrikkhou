SELECT t.type, t.operation, t.k_symbol, 
	count(DISTINCT trans_id), 
	sum(t.amount), 
	avg(t.amount), 
	max(t.amount), 
	min(t.amount) 
FROM trans t 
GROUP BY 1, 2, 3 
ORDER BY 1, 4 DESC, 2, 3;
