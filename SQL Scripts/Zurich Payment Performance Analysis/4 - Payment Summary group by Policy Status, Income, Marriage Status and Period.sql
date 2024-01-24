SELECT ip.policystatus,
		ip.income, marriage_status, ip.periode_id,
		count(DISTINCT ip.referal_code) AS num_customer,
		count(p.payment_date) AS num_payment,
		sum(p.amount) AS total_payment, 
		max(p.amount) AS max_payment,
		min(p.amount) AS min_payment,
		avg(p.amount) AS average_payment
FROM insurance_policy ip 
	JOIN payment p ON ip.referal_code = p.referal_code 
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3, 4