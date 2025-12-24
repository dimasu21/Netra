from app import app
from models import db
try:
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
