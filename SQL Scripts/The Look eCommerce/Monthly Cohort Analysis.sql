WITH cohort_items AS (
    SELECT user_id, MIN(DATE(DATE_TRUNC(created_at, MONTH))) AS cohort_month
    FROM `sql-project-376612.thelook_ecommerce.orders`
    WHERE status = 'Complete'
    GROUP BY 1
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) num_users
    FROM cohort_items
    GROUP BY 1
),
user_orders AS (
    SELECT cohort_items.user_id, 
            cohort_month,
            created_at,
          DATE_DIFF(DATE(DATE_TRUNC(created_at, MONTH)), cohort_month, MONTH) AS month_number
    FROM cohort_items
    LEFT JOIN `sql-project-376612.thelook_ecommerce.orders` ord    
        ON ord.user_id = cohort_items.user_id
     WHERE ord.status = 'Complete' 
    ORDER BY 1
),
retention_table AS (
    SELECT cohort_items.cohort_month,
            ord.month_number,
            COUNT(DISTINCT ord.user_id) AS num_users
    FROM cohort_items    
    LEFT JOIN user_orders ord ON ord.user_id = cohort_items.user_id
    GROUP BY 1, 2
)
SELECT retention.cohort_month,
    size.num_users,
    retention.month_number,
    retention.num_users AS total_users,
    CAST(retention.num_users AS decimal) / size.num_users AS percentage
FROM retention_table retention
LEFT JOIN cohort_size size ON retention.cohort_month = size.cohort_month
WHERE retention.cohort_month IS NOT NULL
        AND retention.cohort_month >= '2021-12-01'
ORDER BY 1,3