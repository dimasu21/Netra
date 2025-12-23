
from app import app
from models import db

with app.app_context():
    print("Creating all tables (safe mode - only new tables created)...")
    db.create_all()
    print("Database tables updated.")
