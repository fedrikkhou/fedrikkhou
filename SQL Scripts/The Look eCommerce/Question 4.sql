SELECT distribution_center.name, user.country
    , COUNT(DISTINCT ord.order_id) num_orders
    , COUNT(DISTINCT order_item.id) num_item_orders
FROM `sql-project-376612.thelook_ecommerce.orders` AS ord
    JOIN `sql-project-376612.thelook_ecommerce.users` AS user ON ord.user_id = user.id
    JOIN `sql-project-376612.thelook_ecommerce.order_items` AS order_item ON order_item.order_id = ord.order_id
    JOIN `sql-project-376612.thelook_ecommerce.inventory_items` AS inventory_item ON inventory_item.id = order_item.inventory_item_id
    JOIN `sql-project-376612.thelook_ecommerce.distribution_centers` AS distribution_center ON distribution_center.id = inventory_item.product_distribution_center_id
WHERE ord.status = 'Complete' 
        AND DATE(ord.shipped_at) BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY 1, 2
ORDER BY 4 DESC