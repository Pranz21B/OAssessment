SELECT d.distribution_id, 
       c.client_name,
       d.period, 
       d.distributed_amount
FROM Distributions d
LEFT JOIN Transactions t 
       ON t.distribution_id = d.distribution_id 
      AND t.status = 'APPROVED'
JOIN Clients c 
  ON c.client_id = d.client_id
WHERE t.transaction_id IS NULL;