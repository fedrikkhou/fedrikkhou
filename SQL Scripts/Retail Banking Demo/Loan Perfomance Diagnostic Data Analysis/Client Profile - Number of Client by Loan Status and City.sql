SELECT l.status,  c.city, count(DISTINCT l.loan_id) 
FROM loan l 
	JOIN account a ON a.account_id  = l.account_id 
	JOIN disposition d ON d.account_id = a.account_id  AND d."type" = 'Owner'
	JOIN client c ON c.client_id = d.client_id
WHERE status IN ('B', 'D', 'A')
GROUP BY 1, 2
ORDER BY 1, 3 DESC, 2;
