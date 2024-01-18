-------------------------FORMAT -----------------------------------------------------------------
SELECT UPPER(d."Format"),
		SUM(amount_spent) AS Spend,
		SUM(impressions) AS Impressions,
		SUM(amount_spent) / SUM(impressions) * 1000 AS CPM,
		SUM(link_clicks) AS Clicks,
		CAST(SUM(link_clicks)*1.00 / SUM(impressions)*1.00 as decimal(7,4)) AS CTR,
		SUM(amount_spent) / SUM(link_clicks) AS CPC,
		SUM(signup) AS "Sign Up",
		CAST(SUM(signup)*1.00 / SUM(link_clicks)*1.00 as decimal(7,4))*100 AS "Sign Up Rate",
		SUM(purchase_zlf + purchase_zlp) AS Purchase,
		CAST(SUM(purchase_zlf + purchase_zlp)*1.00 / SUM(link_clicks)*1.00 as decimal(7,4)) AS CVR,
		CASE
			WHEN SUM(purchase_zlf + purchase_zlp) = 0 THEN null
			ELSE SUM(amount_spent) / SUM(purchase_zlf + purchase_zlp)
		END AS CAC
FROM daily d
GROUP BY 1
ORDER BY 2 DESC