import pytest
from main import PaymentService

def test_payment_service():
    svc = PaymentService()
    assert svc.process(100) is True
    with pytest.raises(ValueError):
        svc.process(-1)