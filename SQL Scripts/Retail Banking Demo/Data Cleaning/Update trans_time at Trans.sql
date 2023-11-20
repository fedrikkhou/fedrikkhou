UPDATE trans 
	SET trans_time = CONCAT(CAST (LEFT(trans_time, 2) AS INTEGER) + 1, ':00:', RIGHT(trans_time, 2)) 
WHERE trans_time like '%:60:%