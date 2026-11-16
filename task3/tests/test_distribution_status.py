import pytest
from mocks import MockDistributionService, ValidationError, DistributionNotFoundError


class TestStatusCheckPositive:
    def test_completed_distribution_returns_status_and_amount(self, service):
        result = service.get_status("C101", "2026-04")
        assert result["status"] == "COMPLETED"
        assert result["amount"] == 7840.00

    def test_pending_distribution_returns_pending_with_no_amount(self, service):
        result = service.get_status("C101", "2026-05")
        assert result["status"] == "PENDING"
        assert result["amount"] is None

    def test_failed_distribution_is_reported_not_swallowed(self, service):
        # Regression guard for BUG-1042: failed payouts must surface as FAILED
        result = service.get_status("C0453", "2026-06")
        assert result["status"] == "FAILED"


class TestStatusCheckNegative:
    def test_invalid_client_id_raises_not_found(self, service):
        with pytest.raises(DistributionNotFoundError):
            service.get_status("C999", "2026-04")

    def test_missing_period_fails_validation_before_lookup(self, service):
        with pytest.raises(ValidationError):
            service.get_status("C101", "")