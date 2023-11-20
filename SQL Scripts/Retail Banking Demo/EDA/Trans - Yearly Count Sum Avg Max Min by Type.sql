SELECT date_part('year', trans_date) , t.type, 
		count(DISTINCT trans_id), 
		sum(t.amount), 
		avg(t.amount), 
		max(t.amount), 
		min(t.amount) 
FROM trans t 
GROUP BY 1,2  
ORDER BY 1,2;
