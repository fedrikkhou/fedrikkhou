WITH payment_data AS (
	SELECT ip.policystatus, 
		ip.periode_id, ip.referal_code,  
		ip.first_transaction_date, 
		count(p.payment_date) AS num_of_payment, 
		sum(p.amount) AS total_payment, 
		avg(p.amount) AS average_payment
	FROM insurance_policy ip 
	JOIN payment p ON ip.referal_code = p.referal_code 
	GROUP BY 1, 2, 3, 4
	ORDER BY 1, 2
)
SELECT policystatus, periode_id, 
	sum(num_of_payment) number_of_payment,
	avg(num_of_payment) avg_num_of_payment,
	sum(total_payment) grand_total_payment,
	max(total_payment) max_total_payment,
	min(total_payment) min_total_payment,
	avg(total_payment) avg_total_payment
FROM payment_data
GROUP BY 1, 2
ORDER BY 1, 2