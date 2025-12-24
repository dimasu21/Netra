"""
================================================================================
DATABASE MODELS - SQLite with SQLAlchemy
================================================================================
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Model untuk menyimpan data user.
    Mendukung registrasi reguler (email + password) dan Google Sign-In.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=True)  # Nullable untuk Google users
    name = db.Column(db.String(100), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=True)  # Untuk Google Sign-In
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)  # Admin access
    
    def set_password(self, password):
        """Hash dan simpan password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifikasi password."""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class History(db.Model):
    """
    Model untuk menyimpan riwayat analisis dokumen user.
    """
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # 'OCR', 'DOC', 'BATCH'
    extracted_text = db.Column(db.Text, nullable=True)  # Hasil OCR/Parse
    ai_summary = db.Column(db.Text, nullable=True)      # Hasil AI Analysis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke User
    user = db.relationship('User', backref=db.backref('history', lazy=True))

    def __repr__(self):
        return f'<History {self.filename}>'
