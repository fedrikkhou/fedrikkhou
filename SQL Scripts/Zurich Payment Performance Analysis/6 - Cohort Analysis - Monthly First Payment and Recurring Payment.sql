WITH cohort_items AS (
    SELECT ip.referal_code, 
    		date_trunc('MONTH', ip.first_transaction_date) AS cohort_month
    FROM insurance_policy ip
    WHERE ip.periode_id = 'Monthly'
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT referal_code) num_users
    FROM cohort_items
    GROUP BY 1
),
policy_payment AS (
    SELECT cohort_items.referal_code, 
            cohort_month,
            p.payment_date,
            DATE_PART('month', AGE(date_trunc('MONTH', p.payment_date), cohort_month)) AS month_number,
            p.number_of_recurring_payment
    FROM cohort_items
    LEFT JOIN payment p   
        ON p.referal_code = cohort_items.referal_code
   	ORDER BY 1, 3
),
retention_table AS (
    SELECT ci.cohort_month,
            --pp.month_number,
            number_of_recurring_payment,
            COUNT(DISTINCT pp.referal_code) AS num_users
    FROM cohort_items ci  
    LEFT JOIN policy_payment pp ON pp.referal_code = ci.referal_code
    GROUP BY 1, 2
)
SELECT retention.cohort_month,
    cs.num_users,
    --retention.month_number,
    retention.number_of_recurring_payment,
    retention.num_users AS total_users,
    CAST(retention.num_users AS decimal) / cs.num_users AS percentage
FROM retention_table retention
LEFT JOIN cohort_size cs ON retention.cohort_month = cs.cohort_month
ORDER BY 1,3

--SELECT referal_code, periode_id  register_time, first_transaction_date  FROM insurance_policy ip 
--SELECT * FROM payment p 