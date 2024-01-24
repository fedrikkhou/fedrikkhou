WITH payment_data AS (
	SELECT ip.referal_code,
			p.payment_date,
			number_of_recurring_payment,
			extract(day from payment_date - first_transaction_date) AS payment_days,
			CASE
			  	WHEN ip.periode_id = 'Monthly' THEN 30
			  	WHEN ip.periode_id = 'Quarterly' THEN 30 * 3
			  	WHEN ip.periode_id = 'Half yearly' THEN 30 * 6
			  	WHEN ip.periode_id = 'Yearly' THEN 30 * 12
			ELSE
			 	0
			END AS "period_days"
	FROM insurance_policy ip 
		JOIN payment p ON ip.referal_code = p.referal_code 
	ORDER BY 1, 2, 3, 4, 5
),
payment_late_days AS (		
	SELECT *,
		payment_days - ((number_of_recurring_payment - 1) * period_days) AS late_days
	FROM payment_data
)
UPDATE payment
SET late_days = payment_late_days.late_days
FROM payment_late_days
WHERE payment.referal_code = payment_late_days.referal_code
		AND payment.payment_date = payment_late_days.payment_date
		AND payment.number_of_recurring_payment = payment_late_days.number_of_recurring_payment