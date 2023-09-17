SELECT DATE_TRUNC(ord.shipped_at, MONTH) AS shipped_month, 
        COUNT(DISTINCT ord.order_id) as num_order
FROM `sql-project-376612.thelook_ecommerce.orders` AS ord
  JOIN `sql-project-376612.thelook_ecommerce.order_items` AS ord_item ON ord.order_id = ord_item.order_id
  JOIN `sql-project-376612.thelook_ecommerce.products` AS product ON ord_item.product_id = product.id
WHERE DATE(ord.shipped_at) BETWEEN '2021-01-01' AND '2021-12-31'
        AND product.category = 'Jeans'
        AND ord.status = 'Complete'
GROUP BY 1
ORDER BY 2