SELECT date_trunc('month', t.trans_date), 
count(DISTINCT trans_id) 
FROM trans t 
GROUP BY 1 
ORDER BY 1;