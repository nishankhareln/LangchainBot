import re
from datetime import datetime, timedelta
import calendar

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number format."""
    # Accepts formats: +1-234-567-8900, 1234567890, 123-456-7890
    pattern = r'^(\+\d{1,3}-?)?\d{3}-?\d{3}-?\d{4}$'
    return bool(re.match(pattern, phone))

def parse_date_from_query(query):
    """Extract date from natural language query."""
    query = query.lower()
    today = datetime.now()
    
    # Handle "next" day queries
    days = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 
            'friday': 4, 'saturday': 5, 'sunday': 6}
    
    for day, day_num in days.items():
        if f"next {day}" in query:
            current_day = today.weekday()
            days_ahead = day_num - current_day
            if days_ahead <= 0:  # Target day has already occurred this week
                days_ahead += 7
            target_date = today + timedelta(days=days_ahead)
            return target_date.strftime('%Y-%m-%d')
    
    # Handle "tomorrow" and "day after tomorrow"
    if "tomorrow" in query:
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    elif "day after tomorrow" in query:
        return (today + timedelta(days=2)).strftime('%Y-%m-%d')
    
    return None

def validate_date(date_str):
    """Validate if the date string is in YYYY-MM-DD format and is a future date."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date > datetime.now()
    except ValueError:
        return False