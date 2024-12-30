from flask import Flask
from pathlib import Path

app = Flask(__name__)

# Ensure data directories exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Ensure documents directory exists
docs_dir = Path("documents")
docs_dir.mkdir(exist_ok=True)

from app.tools.appointment import AppointmentTool
from app.tools.contact_tool import ContactTool

from app import validation