async function sendMessage() {
    const inputElement = document.getElementById('user-input');
    const message = inputElement.value.trim();
    
    if (!message) return;
    
    // Clear input
    inputElement.value = '';
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (data.intent === 'contact_collection') {
            showContactModal();
        } else if (data.available_slots) {
            showAppointmentModal(data.date, data.available_slots);
        } else {
            addMessageToChat('bot', data.answer);
        }
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('bot', 'Sorry, there was an error processing your request.');
    }
}

function addMessageToChat(sender, message) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showContactModal() {
    const modal = document.getElementById('contact-modal');
    modal.style.display = 'block';
}

function showAppointmentModal(date, availableSlots) {
    const modal = document.getElementById('appointment-modal');
    const timeSelect = document.getElementById('appointment-time');
    const dateInput = document.getElementById('appointment-date');
    
    // Clear previous options
    timeSelect.innerHTML = '<option value="">Select Time</option>';
    
    // Add available slots
    availableSlots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot;
        option.textContent = slot;
        timeSelect.appendChild(option);
    });
    
    // Set date
    dateInput.value = date;
    
    modal.style.display = 'block';
}

// Event Listeners
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('contact-name').value,
        email: document.getElementById('contact-email').value,
        phone: document.getElementById('contact-phone').value
    };
    
    try {
        const response = await fetch('/save-contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        document.getElementById('contact-modal').style.display = 'none';
        addMessageToChat('bot', data.message);
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('bot', 'Sorry, there was an error saving your contact information.');
    }
});

document.getElementById('appointment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        date: document.getElementById('appointment-date').value,
        time: document.getElementById('appointment-time').value,
        name: document.getElementById('appointment-name').value,
        email: document.getElementById('appointment-email').value,
        phone: document.getElementById('appointment-phone').value
    };
    
    try {
        const response = await fetch('/book-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        document.getElementById('appointment-modal').style.display = 'none';
        addMessageToChat('bot', data.message);
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('bot', 'Sorry, there was an error booking your appointment.');
    }
});

// Close modals when clicking outside
window.onclick = function(event) {
    const contactModal = document.getElementById('contact-modal');
    const appointmentModal = document.getElementById('appointment-modal');
    
    if (event.target === contactModal) {
        contactModal.style.display = 'none';
    }
    if (event.target === appointmentModal) {
        appointmentModal.style.display = 'none';
    }
}

// Handle enter key in chat input
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});