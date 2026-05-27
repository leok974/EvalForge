import pytest

def apply_discount(amount, rate):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount * (1 - rate)

def test_discount_negative():
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        apply_discount(-10, 0.1)

if __name__ == "__main__":
    pytest.main([__file__])
