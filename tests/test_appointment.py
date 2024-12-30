from app.tools.appointment import save_appointment

def test_save_appointment():
    response = save_appointment("John Doe", "john@example.com", "+1234567890", "2024-01-01")
    assert "Appointment successfully scheduled" in response
