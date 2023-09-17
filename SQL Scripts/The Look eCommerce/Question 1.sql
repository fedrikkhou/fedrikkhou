SELECT product_category, 
    COUNT(DISTINCT product_sku) AS sku_num
FROM `sql-project-376612.thelook_ecommerce.inventory_items`
WHERE DATE(created_at) BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY product_category
ORDER BY 2 DESC