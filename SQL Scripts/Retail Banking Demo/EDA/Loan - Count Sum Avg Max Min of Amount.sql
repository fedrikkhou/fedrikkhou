SELECT count(DISTINCT loan_id), sum(amount), avg(amount), max(amount), min(amount) 
FROM loan l