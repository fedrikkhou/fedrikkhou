WITH user_group AS (
    SELECT DISTINCT user.id AS user_id, 
    CASE
        WHEN user.age >= 55 THEN '55 and above'
        WHEN user.age >= 35 THEN '35 to 54'
        WHEN user.age >= 25 THEN '25 to 34'
        WHEN user.age >= 18 THEN '18 to 24'
        ELSE 'below 18'
        END AS age_group,
    user.gender, user.country
    FROM `sql-project-376612.thelook_ecommerce.users` AS user 
        JOIN `sql-project-376612.thelook_ecommerce.orders` AS ord ON ord.user_id = user.id
    WHERE ord.status = 'Complete' 
        AND DATE(ord.shipped_at) BETWEEN '2021-01-01' AND '2021-12-31'
)

SELECT age_group, gender, country
    , COUNT(user_id) AS num_users
    , SUM(count(*)) OVER() AS total_users
    , COUNT(user_id) /  SUM(count(*)) OVER() as ratio
    , (COUNT(user_id) /  SUM(count(*)) OVER()) * 100 as percentage
FROM user_group
GROUP BY 1, 2, 3
ORDER BY 4 DESC