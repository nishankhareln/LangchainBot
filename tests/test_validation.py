from app.validation import validate_email, validate_phone, validate_date

def test_validate_email():
    assert validate_email("test@example.com")
    assert not validate_email("invalid-email")

def test_validate_phone():
    assert validate_phone("+1234567890")
    assert not validate_phone("invalid-phone")

def test_validate_date():
    assert validate_date("2024-01-01")
    assert not validate_date("invalid-date")
