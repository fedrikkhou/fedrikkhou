SELECT CASE
			WHEN p.late_days > 45 THEN '> 45 Days'
			WHEN p.late_days > 30 THEN '31 - 45 Days'
			WHEN p.late_days > 15 THEN '16 - 30 Days'
			WHEN p.late_days > 5  THEN '6 - 15 Days'
			WHEN p.late_days > 0 THEN '1 - 5 Days'
		ELSE
			 'Not Late'
		END AS "late_group",
		periode_id,
		income, marriage_status,
		COUNT(*) AS num_payment,
		COUNT(DISTINCT p.referal_code) AS num_customer,
		sum(p.amount)
FROM payment p
	JOIN insurance_policy ip ON p.referal_code = ip.referal_code
GROUP BY 1, 2, 3, 4
