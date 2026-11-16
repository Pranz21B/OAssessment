SELECT 
    client_id, 
    client_name, 
    period, 
    expected_amount, 
    distributed_amount, 
    ABS(distributed_amount - expected_amount) AS variance
FROM (
    SELECT 
        s.client_id,
        c.client_name,
        s.period,
        s.source_amount * (1 - s.fee_pct) AS expected_amount,
        d.distributed_amount
    FROM SourceCalculations s
    JOIN Distributions d ON s.client_id = d.client_id AND s.period = d.period
    JOIN Clients c ON s.client_id = c.client_id
) AS calc
WHERE ABS(distributed_amount - expected_amount) > 0.01
ORDER BY variance DESC;