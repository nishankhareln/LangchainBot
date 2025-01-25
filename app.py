import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import pydantic_core
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from flask import Flask, request, jsonify, render_template

import sys
from pathlib import Path
# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.tools import AppointmentTool, ContactTool

from app.tools.contact_tool import ContactTool
from app.validation import (
    validate_email, validate_phone, validate_date,
    parse_date_from_query
)

# Initialize Flask app
app = Flask(__name__,template_folder='templates')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()  # This will automatically load variables from your .env file

# Initialize Google API client (no need for API key here)
genai.configure()

# Initialize tools
appointment_tool = AppointmentTool()
contact_tool = ContactTool()

# Initialize LangChain components
def initialize_qa_chain():
    # Load and process documents
    loader = TextLoader('documents/knowledge_base.txt')
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Create QA chain
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        convert_system_message_to_human=True
    )
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    
    return qa_chain

qa_chain = initialize_qa_chain()
chat_history = []

def process_appointment_intent(query: str) -> Dict:
    """Process appointment booking intent."""
    # Extract date from query
    date_str = parse_date_from_query(query)
    if not date_str:
        return {
            "status": "error",
            "message": "Could not determine appointment date from query."
        }
    
    # Get available slots
    available_slots = appointment_tool.get_available_slots(date_str)
    if not available_slots:
        return {
            "status": "error",
            "message": f"No available slots for {date_str}"
        }
    
    return {
        "status": "success",
        "date": date_str,
        "available_slots": available_slots
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    # Check for appointment booking intent
    if any(keyword in user_message.lower() 
           for keyword in ['book', 'appointment', 'schedule']):
        return jsonify(process_appointment_intent(user_message))
    
    # Check for contact collection intent
    if any(keyword in user_message.lower() 
           for keyword in ['call me', 'contact me']):
        return jsonify({
            "status": "success",
            "intent": "contact_collection"
        })
    
    # Default to Q&A
    result = qa_chain({
        "question": user_message,
        "chat_history": chat_history
    })
    
    chat_history.append((user_message, result['answer']))
    
    return jsonify({
        "status": "success",
        "answer": result['answer']
    })

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    
    # Validate inputs
    if not all([data.get(f) for f in ['date', 'time', 'name', 'email', 'phone']]):
        return jsonify({
            "status": "error",
            "message": "Missing required fields"
        })
    
    if not validate_email(data['email']):
        return jsonify({
            "status": "error",
            "message": "Invalid email format"
        })
    
    if not validate_phone(data['phone']):
        return jsonify({
            "status": "error",
            "message": "Invalid phone number format"
        })
    
    if not validate_date(data['date']):
        return jsonify({
            "status": "error",
            "message": "Invalid date"
        })
    
    # Book appointment
    result = appointment_tool.book_appointment(
        date=data['date'],
        time=data['time'],
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    
    return jsonify(result)

@app.route('/save-contact', methods=['POST'])
def save_contact():
    data = request.json
    
    # Validate inputs
    if not all([data.get(f) for f in ['name', 'email', 'phone']]):
        return jsonify({
            "status": "error",
            "message": "Missing required fields"
        })
    
    if not validate_email(data['email']):
        return jsonify({
            "status": "error",
            "message": "Invalid email format"
        })
    
    if not validate_phone(data['phone']):
        return jsonify({
            "status": "error",
            "message": "Invalid phone number format"
        })
    
    # Save contact
    result = contact_tool.add_contact(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
