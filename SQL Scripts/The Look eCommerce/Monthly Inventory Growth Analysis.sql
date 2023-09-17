WITH added_inventory_over_month AS (
    SELECT DATE(DATE_TRUNC(created_at, MONTH)) AS created_month
        , product_category
        , COUNT(id) AS added_inventory 
    FROM `sql-project-376612.thelook_ecommerce.inventory_items`
    GROUP BY 1, 2
    ),
sold_inventory_over_month AS (
    SELECT DATE(DATE_TRUNC(sold_at, MONTH)) AS sold_month
    , product_category
    , COUNT(id) AS sold_inventory 
    FROM `sql-project-376612.thelook_ecommerce.inventory_items`
    WHERE sold_at IS NOT NULL
    GROUP BY 1, 2
    ),
combine_inventory_data AS (
SELECT created_month AS inventory_month,
         added.product_category, added_inventory
    , COALESCE(sold_inventory, 0) AS sold_inventory
    
FROM added_inventory_over_month AS added
LEFT JOIN sold_inventory_over_month AS sold ON added.created_month = sold.sold_month
    AND added.product_category = sold.product_category
),
calculate_monthly_growth AS (
SELECT *
    , SUM(added_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month) AS total_added_inventory
    , SUM(sold_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month) AS total_sold_inventory
    , SUM(added_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month) - 
        SUM(sold_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month) AS total_inventory
FROM combine_inventory_data
)
SELECT *
    , (total_inventory - LAG(total_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month)) AS total_inventory_growth
    , ((total_inventory - LAG(total_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month)) /
        NULLIF(LAG(total_inventory) OVER (PARTITION BY product_category ORDER BY inventory_month),0)) AS total_inventory_growth_rate
FROM calculate_monthly_growth
ORDER BY 2, 1