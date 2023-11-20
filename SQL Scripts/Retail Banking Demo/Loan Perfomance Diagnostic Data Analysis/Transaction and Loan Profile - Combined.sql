-- Total Transaction Amount per Month
WITH monthly_total_transaction AS (
	SELECT c.client_id, l.status, l.amount AS loan_amount, l.payments,
		date_trunc('month', t.trans_date) AS trans_month, t."type" AS trans_type, sum(t.amount) AS total_amount
	FROM loan l
		JOIN account a ON a.account_id  = l.account_id 
		JOIN disposition d ON d.account_id = a.account_id AND d."type" = 'Owner' 
		JOIN client c ON c.client_id = d.client_id
		JOIN trans t ON t.account_id = a.account_id 
	WHERE l.status IN ('B', 'D', 'A')
	GROUP BY 1, 2, 3, 4, 5, 6
	ORDER BY 2, 1, 4 ),
-- Average of Total Transaction Amount per Month
monthly_average_transaction AS (
	SELECT client_id, status, loan_amount, payments, trans_type, avg(total_amount) AS monthly_average_amount
	FROM monthly_total_transaction
	GROUP BY 1, 2, 3, 4, 5
	ORDER BY 2, 1, 4),
-- Summarize the Average of Total Transaction Amount per Month of each client / create the data into 1 row per client
monthly_average_transaction_summary AS (
	SELECT credit.client_id, credit.status, credit.loan_amount, credit.payments, 
		credit.trans_type, credit.monthly_average_amount AS monthly_average_credit_amount, 
		debit.trans_type, debit.monthly_average_amount AS monthly_average_debit_amount, 
		credit.monthly_average_amount - debit.monthly_average_amount AS diff,
		CASE
			WHEN credit.monthly_average_amount - debit.monthly_average_amount > 0 THEN 1
			ELSE 0
		END AS is_surplus,
		credit.payments / credit.monthly_average_amount AS pct_of_payments
	FROM (SELECT * FROM monthly_average_transaction WHERE trans_type = 'Credit') credit
		JOIN (SELECT * FROM monthly_average_transaction WHERE trans_type = 'Debit') debit ON credit.client_id = debit.client_id)
SELECT status,
		CASE 
			WHEN loan_amount > 100000 THEN 'Above 100k'
			ELSE 'Under 100k'
		END AS loan_amount_range,
		count(DISTINCT client_id) AS number_of_client,
		sum(is_surplus) AS number_of_client_positive_balance,
		cast(sum(is_surplus) as decimal(7,2)) / cast(count(DISTINCT client_id) as decimal(7,2)) 
					AS number_of_client_positive_balance_pct,
		avg(pct_of_payments) AS average_of_pct_of_payments
FROM monthly_average_transaction_summary
GROUP BY 1, 2
ORDER BY 1, 2;
