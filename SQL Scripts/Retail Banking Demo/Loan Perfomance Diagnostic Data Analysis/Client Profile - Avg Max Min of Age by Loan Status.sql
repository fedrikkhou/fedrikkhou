SELECT l.status, avg(c.age), max(c.age), min(c.age)
FROM loan l 
	JOIN account a ON a.account_id  = l.account_id 
	JOIN disposition d ON d.account_id = a.account_id AND d."type" = 'Owner' 
	JOIN client c ON c.client_id = d.client_id
WHERE status IN ('B', 'D', 'A')
GROUP BY 1;