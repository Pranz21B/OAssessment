SELECT substr(processed_at, 1, 7) AS month,
       SUM(distributed_amount) AS total_distributed
FROM Distributions
GROUP BY month
ORDER BY month;