SELECT usr.country
      ,COUNT(DISTINCT ord.user_id) total_user
FROM `sql-project-376612.thelook_ecommerce.orders` AS ord
LEFT JOIN `sql-project-376612.thelook_ecommerce.users` AS usr on usr.id = ord.user_id
WHERE ord.status = 'Complete'
AND DATE(ord.shipped_at) BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY 1
ORDER BY 2 DESC
 