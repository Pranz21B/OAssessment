## Task 1

### Scaling Strategy Approach
Since this strategy uses Python/Pandas with SQL queries, I am currently loading data into RAM. 
While feasible for thousands of rows, this approach will not scale efficiently to millions of rows due to memory constraints.

To optimize for production scale, I recommend the following architecture:
Regulation & Audit Table: Create a dedicated table to store validation rules and audit logs. 
A stored procedure will handle the primary validation logic against this table.
Secondary Verification Job: Implement a scheduled job as a secondary layer of defense. 
This job runs independently to verify data consistency and catch any issues missed by the primary procedure.
Automated Alerting: Configure alerts to trigger immediately if either the stored procedure detects discrepancies or if the scheduled job fails, 
ensuring the team is notified of errors in real-time.


## Task 3
### My Regression Strategy for Task 3


### Context
According to the assessment we must assume a release is going out in two days and only a limited testing window is available. 


### Prioritized Coverage I would choose manually. 
1. Happy Path - Ensuring the primary money allocation movement works End-To-End.
2. Pending State -  Ensures the system handles in-progress states gracefully.
3. Failed State - Must be done given the known bug where a null was detected on fee percentage. 
4. Data Validation - Ensures the service doesn't crash on unexpected or bad data.

### How My Automated Coverage Reflects This Prioritisation
The automated tests I built map directly to the four priorities above:

Happy Path – covered by the primary allocation test (asserts correct amount movement and final state).
Happy Path – test_completed_distribution_returns_status_and_amount asserts the correct status and amount are returned for a completed distribution.
Pending State – test_pending_distribution_returns_pending_with_no_amount asserts an in-progress record returns PENDING with no amount.
Failed State – test_failed_distribution_is_reported_not_swallowed guards against bug by asserting a failed payout surfaces as FAILED rather than being silently dropped.
Data Validation – test_missing_period_fails_validation_before_lookup asserts an empty period raises a ValidationError before any DB access, 
test_invalid_client_id_raises_not_found asserts an unknown client ID raises DistributionNotFoundError.

### Deliberately NOT Covered
- Complete End to End tests. Risk Tradeoff: Accept residual risk of integration-level defects; 
mitigated by the fact (based on the assessment information) that no new integrations were introduced in this release.

- Performance or Security Tests. Risk Tradeoff: Accept risk of regression in throughput or auth behaviour.
no performance-sensitive or security-relevant code changed in this window.

- Schema or DB Tests. Risk Tradeoff: Accept risk of undetected schema drift and DB layer is unchanged and the prior cycle found no defects there.

- UI/UX/Userbility - Risk Tradeoff: Out of scope.

### Automation Vs Manual and Final Consideration
To ensure a blend to achieve optimal value given the deadlines and taking into consideration a time buffer if any bugs may be found, 
in my opionion the below would be my final consideration and approach to testing for the regression phase.

- Where automation is setup, automation tests can be run as part of the regression phase.
- Where manual testing is required and automation is not available we can manually test the regression tests points of concern. 


## AI Usage Disclosure
AI Usage Disclosure
I utilized a Large Language Model (LLM) as a supportive tool to enhance efficiency and code quality during this assessment. 
My usage was strictly limited to:

Logic Verification and SQL wrapping: Validating that pandas was the optimal library for automated financial calculations in Task 1.
Logic guidance on the method to create a one click solution was achievable. 
SQL Syntax Review: Confirming the correctness and efficiency of SQL cleanup queries for Task 2.
Code Structure Guidance: Seeking advice on best practices for Python class structure in Task 3.

Note: Core logic, problem-solving, final code implementation, and strategic decisions were made and executed by me. 
The AI served as a secondary reviewer to ensure accuracy and adherence to industry standards.