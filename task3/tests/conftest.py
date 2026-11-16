
import pytest
from mocks import MockDistributionService


@pytest.fixture
def service():
    """Mock service preloaded with known-good and known-bad records."""
    records = [
        {"client_id": "C101",  "period": "2026-04", "status": "COMPLETED", "amount": 7840.00},
        {"client_id": "C101",  "period": "2026-05", "status": "PENDING",   "amount": None},
        {"client_id": "C109",  "period": "2026-04", "status": "COMPLETED", "amount": 4900.00},
        {"client_id": "C0453", "period": "2026-06", "status": "FAILED",    "amount": None},
    ]
    return MockDistributionService(records)