import json
from pathlib import Path
from typing import Dict, Optional

class ContactTool:
    def __init__(self, contacts_file: str = 'data/contacts.json'):
        self.contacts_file = Path(contacts_file)
        self.contacts_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.contacts_file.exists():
            self.contacts_file.write_text('[]')
    
    def load_contacts(self) -> list:
        """Load contacts from JSON file."""
        try:
            return json.loads(self.contacts_file.read_text())
        except:
            return []
    
    def save_contacts(self, contacts: list):
        """Save contacts to JSON file."""
        self.contacts_file.write_text(json.dumps(contacts, indent=2))
    
    def add_contact(self, name: str, email: str, phone: str) -> Dict[str, str]:
        """Add a new contact."""
        contacts = self.load_contacts()
        
        # Check if contact already exists
        for contact in contacts:
            if contact['email'] == email:
                return {
                    "status": "error",
                    "message": "Contact with this email already exists."
                }
        
        # Add new contact
        new_contact = {
            "name": name,
            "email": email,
            "phone": phone
        }
        
        contacts.append(new_contact)
        self.save_contacts(contacts)
        
        return {
            "status": "success",
            "message": f"Contact information saved successfully for {name}"
        }
    
    def get_contact(self, email: str) -> Optional[Dict]:
        """Get contact by email."""
        contacts = self.load_contacts()
        for contact in contacts:
            if contact['email'] == email:
                return contact
        return None