SELECT EXTRACT(MONTH FROM payment_date) AS payment_month, 
		count(DISTINCT referal_code) AS number_of_customer, 
		count(*) AS number_of_payment, 
		sum(amount) AS total_payment, 
		max(amount) AS max_payment, 
		min(amount) AS min_payment, 
		avg(amount) AS avg_payment
FROM payment p
GROUP BY 1
ORDER BY 1 DESC
