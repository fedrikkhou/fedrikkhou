SELECT PolicyStatus,
		EXTRACT(YEAR FROM register_time) AS register_year,
		EXTRACT(quarter  FROM register_time) AS register_month, 
		count(DISTINCT referal_code) AS number_of_customer
FROM insurance_policy ip 
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 2 ASC, 3 ASC