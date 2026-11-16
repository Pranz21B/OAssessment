import re

class ValidationError(Exception):
    pass


class DistributionNotFoundError(Exception):
    def __init__(self, client_id, period):
        self.client_id = client_id
        self.period = period
        super().__init__(f"No distribution found for client '{client_id}' in period '{period}'")


class MockDistributionService:

    def __init__(self, records=None):
        # records: list {client_id, period, status, amount}
        self._records = records or []

    def get_status(self, client_id, period):
        # 1. Validates my inputs
        if not isinstance(client_id, str) or not client_id.strip():
            raise ValidationError("client_id is required and must be a non-empty string")
        if not isinstance(period, str) or not period.strip():
            raise ValidationError("period is required and must be a non-empty string (format YYYY-MM)")
        if not re.fullmatch(r"\d{4}-\d{2}", period):
            raise ValidationError(f"period '{period}' does not match expected format YYYY-MM")

        # 2. Look up the record
        rec = next((r for r in self._records
                    if r["client_id"] == client_id and r["period"] == period), None)
        if rec is None:
            raise DistributionNotFoundError(client_id, period)

        # 3. Return the response for me
        return {
            "client_id": rec["client_id"],
            "period": rec["period"],
            "status": rec["status"],
            "amount": rec["amount"],
        }