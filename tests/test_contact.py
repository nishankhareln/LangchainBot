from app.tools.contact_tool import save_contact

def test_save_contact():
    response = save_contact("Jane Doe", "jane@example.com", "+1234567890")
    assert "Contact information saved" in response
