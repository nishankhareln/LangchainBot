import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

class AppointmentTool:
    def __init__(self, appointments_file: str = 'data/appointments.json'):
        self.appointments_file = Path(appointments_file)
        self.appointments_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.appointments_file.exists():
            self.appointments_file.write_text('[]')
    
    def load_appointments(self) -> list:
        """Load appointments from JSON file."""
        try:
            return json.loads(self.appointments_file.read_text())
        except:
            return []
    
    def save_appointments(self, appointments: list):
        """Save appointments to JSON file."""
        self.appointments_file.write_text(json.dumps(appointments, indent=2))
    
    def book_appointment(self, date: str, time: str, name: str, 
                        email: str, phone: str) -> Dict[str, str]:
        """Book a new appointment."""
        appointments = self.load_appointments()
        
        # Check if slot is available
        for appt in appointments:
            if appt['date'] == date and appt['time'] == time:
                return {
                    "status": "error",
                    "message": "This time slot is already booked."
                }
        
        # Add new appointment
        new_appointment = {
            "date": date,
            "time": time,
            "name": name,
            "email": email,
            "phone": phone,
            "created_at": datetime.now().isoformat()
        }
        
        appointments.append(new_appointment)
        self.save_appointments(appointments)
        
        return {
            "status": "success",
            "message": f"Appointment booked successfully for {date} at {time}"
        }
    
    def get_available_slots(self, date: str) -> list:
        """Get available time slots for a given date."""
        all_slots = [
            "09:00", "10:00", "11:00", "12:00", "14:00", 
            "15:00", "16:00", "17:00"
        ]
        
        # Get booked slots
        appointments = self.load_appointments()
        booked_slots = [
            appt['time'] for appt in appointments 
            if appt['date'] == date
        ]
        
        # Return available slots
        return [slot for slot in all_slots if slot not in booked_slots]