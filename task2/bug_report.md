Bug ID -(ID001)
Title - BatchDistributionJob crashes when fee_pct is NULL 

Severity - High
Occurence - Happens All The Time
Priority - High

Defect Status - Active (In Current Master)
Date Reported - 12/11/2026
Reported By - PraneshB
Assigned To - Developer Mr Awesome

Business Impact
Client C0453 receives no payout for 2026-06.
Failures are invisible to monitoring; detection requires manual reconciliation.
Any client with NULL fee_pct will be silently skipped in future runs.


Preconditions:
1. Ensure you have the latest version of the codebase installed in your environment with fresh cache and settings where applicable.

Steps to Reproduce:
1. Ensure a client exists with fee_pct = NULL in SourceCalculations.
2. Run BatchDistributionJob for that period.
3. Observe the crash and skipped distribution in error logs. 

Expected Results:
1. The NULL fee_pct should either default to 0% or route the record to a review queue 
with a clear error message. No raw arithmetic exception should occur.

Actual Result:
1. 2026-06-14 02:14:22 ERROR BatchDistributionJob - java.lang.ArithmeticException: / by zero
    at com.x.finance.distribution.FeeCalculator.applyFee(FeeCalculator.java:87)
    at com.x.finance.distribution.DistributionProcessor.process(DistributionProcessor.java:142)
    at com.x.finance.distribution.BatchDistributionJob.run(BatchDistributionJob.java:64)
The distribution is then skipped and client does not receive a payout. 

Test Case Result: FAILED

Environment and Configuration Details:
1. Latest codebase - Master001
2. Sandbox Sygnia Test 1A

Attachments: N/A

Root Cause Analysis:
FeeCalculator.applyFee() performs a division involving fee_pct without a null
guard. The NULL value is forced to 0, producing divide-by-zero. 


Notes:
Recommended Fix
1. Add a null/zero guard in FeeCalculator.applyFee() before any division.
2. Enforce fee_pct IS NOT NULL at the schema level.
3. Emit an alert when failed_count > 0 so batches cannot report false success.
4. Backfill: re-process C0453 and audit all periods for NULL fee_pct rows.