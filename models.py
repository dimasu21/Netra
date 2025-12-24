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


class UsageLimit(db.Model):
    """
    Model untuk tracking penggunaan fitur dengan limit harian.
    Digunakan untuk membatasi batch processing (3x/hari untuk free user).
    """
    __tablename__ = 'usage_limits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feature = db.Column(db.String(50), nullable=False)  # 'batch', 'ai_analysis', dll
    usage_count = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relasi ke User
    user = db.relationship('User', backref=db.backref('usage_limits', lazy=True))

    # Constants untuk limit
    BATCH_DAILY_LIMIT = 10
    AI_DAILY_LIMIT = 10

    @classmethod
    def get_or_create(cls, user_id, feature):
        """Get existing usage record or create new one."""
        usage = cls.query.filter_by(user_id=user_id, feature=feature).first()
        if not usage:
            usage = cls(user_id=user_id, feature=feature, usage_count=0)
            db.session.add(usage)
            db.session.commit()
        return usage

    def check_and_increment(self):
        """
        Check if user can use feature, increment if allowed.
        Returns (allowed: bool, remaining: int, message: str)
        """
        from datetime import datetime, timedelta
        
        # Reset if last reset was more than 24 hours ago
        now = datetime.utcnow()
        if self.last_reset is None or (now - self.last_reset) > timedelta(hours=24):
            self.usage_count = 0
            self.last_reset = now
            db.session.commit()
        
        # Get limit based on feature
        if self.feature == 'batch':
            limit = self.BATCH_DAILY_LIMIT
        elif self.feature == 'ai_analysis':
            limit = self.AI_DAILY_LIMIT
        else:
            limit = 10  # Default limit
        
        remaining = limit - self.usage_count
        
        if self.usage_count >= limit:
            hours_until_reset = 24 - int((now - self.last_reset).total_seconds() / 3600)
            return False, 0, f"Limit harian tercapai ({limit}x/hari). Reset dalam ~{hours_until_reset} jam."
        
        # Increment usage
        self.usage_count += 1
        db.session.commit()
        
        return True, remaining - 1, "OK"

    def __repr__(self):
        return f'<UsageLimit {self.feature}: {self.usage_count}>'


class GuestUsageLimit(db.Model):
    """
    Model untuk tracking penggunaan fitur oleh guest (non-login) berdasarkan IP.
    Limit 3x/hari untuk semua fitur (batch, OCR, parse document).
    """
    __tablename__ = 'guest_usage_limits'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False, index=True)  # IPv6 max 45 chars
    feature = db.Column(db.String(50), nullable=False)  # 'batch', 'ocr', 'document', 'analyze'
    usage_count = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)

    # Constants - Guest limit lebih ketat
    DAILY_LIMIT = 3

    @classmethod
    def get_or_create(cls, ip_address, feature):
        """Get existing usage record or create new one for IP."""
        usage = cls.query.filter_by(ip_address=ip_address, feature=feature).first()
        if not usage:
            usage = cls(ip_address=ip_address, feature=feature, usage_count=0)
            db.session.add(usage)
            db.session.commit()
        return usage

    def check_and_increment(self):
        """
        Check if guest can use feature, increment if allowed.
        Returns (allowed: bool, remaining: int, message: str)
        """
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        
        # Reset if 24 hours passed
        if self.last_reset is None or (now - self.last_reset) > timedelta(hours=24):
            self.usage_count = 0
            self.last_reset = now
            db.session.commit()
        
        remaining = self.DAILY_LIMIT - self.usage_count
        
        if self.usage_count >= self.DAILY_LIMIT:
            hours_until_reset = 24 - int((now - self.last_reset).total_seconds() / 3600)
            return False, 0, f"Limit harian tercapai. Login atau tunggu ~{hours_until_reset} jam."
        
        # Increment usage
        self.usage_count += 1
        db.session.commit()
        
        return True, remaining - 1, "OK"

    def __repr__(self):
        return f'<GuestUsageLimit {self.ip_address}:{self.feature}: {self.usage_count}>'
