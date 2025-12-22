"""
================================================================================
AUTHENTICATION ROUTES
================================================================================
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
import re

auth = Blueprint('auth', __name__)


def is_valid_email(email):
    """Validasi format email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validasi input
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Nama harus minimal 2 karakter.')
        
        if not email or not is_valid_email(email):
            errors.append('Email tidak valid.')
        
        if not password or len(password) < 6:
            errors.append('Password harus minimal 6 karakter.')
        
        if password != confirm_password:
            errors.append('Password dan konfirmasi password tidak cocok.')
        
        # Cek apakah email sudah terdaftar
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            errors.append('Email sudah terdaftar. Silakan login atau gunakan email lain.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('signup.html', name=name, email=email)
        
        # Buat user baru
        new_user = User(
            name=name,
            email=email
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan. Silakan coba lagi.', 'error')
            return render_template('signup.html', name=name, email=email)
    
    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email dan password harus diisi.', 'error')
            return render_template('login.html', email=email)
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Email atau password salah.', 'error')
            return render_template('login.html', email=email)
        
        if not user.is_active:
            flash('Akun Anda telah dinonaktifkan.', 'error')
            return render_template('login.html', email=email)
        
        login_user(user, remember=bool(remember))
        flash(f'Selamat datang, {user.name}!', 'success')
        
        # Redirect ke halaman yang diminta sebelumnya atau index
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('index'))


# ==============================================================================
# GOOGLE OAUTH
# ==============================================================================

import os
from authlib.integrations.flask_client import OAuth

# Initialize OAuth (will be configured in app.py)
oauth = OAuth()

def init_google_oauth(app):
    """Initialize Google OAuth with app context."""
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@auth.route('/login/google')
def login_google():
    """Redirect to Google OAuth."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Check if Google OAuth is configured
    if not os.environ.get('GOOGLE_CLIENT_ID'):
        flash('Google Sign-In belum dikonfigurasi.', 'error')
        return redirect(url_for('auth.login'))
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route('/callback')
def google_callback():
    """Handle Google OAuth callback."""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Gagal mendapatkan informasi dari Google.', 'error')
            return redirect(url_for('auth.login'))
        
        email = user_info.get('email', '').lower()
        name = user_info.get('name', '')
        google_id = user_info.get('sub')  # Google's unique user ID
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            # Create new user from Google
            user = User(
                email=email,
                name=name,
                google_id=google_id
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Akun berhasil dibuat! Selamat datang, {name}!', 'success')
        else:
            # Update google_id if not set
            if not user.google_id:
                user.google_id = google_id
                db.session.commit()
            flash(f'Selamat datang kembali, {user.name}!', 'success')
        
        login_user(user, remember=True)
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
        return redirect(url_for('auth.login'))

