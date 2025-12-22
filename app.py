"""
================================================================================
ASISTEN TINJAUAN PUSTAKA (Literature Review Assistant)
================================================================================
Aplikasi web untuk membantu mahasiswa melakukan screening referensi fisik
(buku/jurnal) menggunakan OCR dan Algoritma Rabin-Karp.

Tech Stack:
- Backend: Flask (Python)
- OCR: Pytesseract (Tesseract OCR)
- Algorithm: Rabin-Karp dengan Rolling Hash

Author: Thesis Project
================================================================================
"""

import os
import re
import base64
from io import BytesIO
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, current_user
from PIL import Image
import pytesseract

# Document processing libraries
from docx import Document
import PyPDF2

# Groq AI
from groq import Groq
from dotenv import load_dotenv

# Database and Auth
from models import db, User

# Load environment variables
load_dotenv()

# Configure Groq API (use environment variable or fallback to default)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

# Configure Tesseract path (auto-detect for Docker/Windows)
import shutil
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.path.exists(r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'netra-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register auth blueprint
from auth import auth as auth_blueprint, init_google_oauth
app.register_blueprint(auth_blueprint)

# Create database tables
with app.app_context():
    db.create_all()

# Initialize Google OAuth
init_google_oauth(app)


# ==============================================================================
# RABIN-KARP ALGORITHM IMPLEMENTATION
# ==============================================================================
"""
ALGORITMA RABIN-KARP dengan ROLLING HASH
=========================================

Rabin-Karp adalah algoritma pencarian string yang menggunakan fungsi hash
untuk menemukan pola dalam teks. Keunggulannya adalah efisiensi O(n+m)
dalam kasus rata-rata.

RUMUS ROLLING HASH:
-------------------
Untuk string s[0..m-1], nilai hash dihitung sebagai:

    H(s) = (s[0] × BASE^(m-1) + s[1] × BASE^(m-2) + ... + s[m-1] × BASE^0) mod PRIME

Dimana:
    - BASE = 256 (jumlah karakter ASCII)
    - PRIME = 101 (bilangan prima untuk mengurangi collision)
    - m = panjang pattern yang dicari

ROLLING UPDATE:
---------------
Saat menggeser window dari posisi i ke i+1:

    H_new = ((H_old - s[i] × BASE^(m-1)) × BASE + s[i+m]) mod PRIME

Ini memungkinkan perhitungan hash O(1) untuk setiap posisi baru,
bukan O(m) jika dihitung ulang dari awal.

UNTUK SIDANG THESIS:
--------------------
1. Kompleksitas waktu rata-rata: O(n + m)
2. Kompleksitas waktu terburuk: O(nm) - saat banyak collision
3. Digunakan untuk: plagiarism detection, DNA sequence matching, dll.
"""

# Konstanta untuk Rabin-Karp
BASE = 256      # Jumlah karakter dalam alfabet ASCII
PRIME = 101     # Bilangan prima untuk operasi modulo


# ==============================================================================
# AI SUMMARY FUNCTION (GROQ)
# ==============================================================================

def generate_ai_summary(text: str) -> dict:
    """
    Generate AI summary of document using Groq.
    
    Args:
        text (str): Extracted text from document
        
    Returns:
        dict: Summary with ringkasan, key_points, metodologi, hasil, kesimpulan
    """
    try:
        prompt = f"""
Anda adalah asisten riset akademik. Analisis teks jurnal/dokumen berikut dan berikan output dalam format yang terstruktur.

TEKS DOKUMEN:
{text[:6000]}

Berikan analisis dalam format berikut (gunakan bahasa Indonesia):

## RINGKASAN
[Ringkasan singkat 2-3 kalimat tentang isi dokumen]

## POIN PENTING
- [Poin 1]
- [Poin 2]
- [Poin 3]

## METODOLOGI
[Jelaskan metodologi penelitian jika ada, atau tulis "Tidak terdeteksi" jika tidak ada]

## HASIL PENELITIAN
[Jelaskan hasil utama penelitian jika ada, atau tulis "Tidak terdeteksi" jika tidak ada]

## KESIMPULAN
[Kesimpulan utama dari dokumen]
"""
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        
        ai_text = response.choices[0].message.content
        
        return {
            'success': True,
            'summary': ai_text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'summary': None
        }


def rabin_karp_search(text: str, pattern: str) -> list:
    """
    Implementasi MANUAL Algoritma Rabin-Karp untuk mencari pattern dalam teks.
    TIDAK menggunakan str.find() atau str.index().
    
    Args:
        text (str): Teks yang akan dicari
        pattern (str): Pattern/keyword yang ingin ditemukan
        
    Returns:
        list: Daftar posisi (index) dimana pattern ditemukan
    """
    # Handle edge cases
    if not pattern or not text:
        return []
    
    if len(pattern) > len(text):
        return []
    
    # Case-insensitive search: konversi ke lowercase
    text_lower = text.lower()
    pattern_lower = pattern.lower()
    
    n = len(text_lower)      # Panjang teks
    m = len(pattern_lower)   # Panjang pattern
    
    positions = []  # List untuk menyimpan posisi yang ditemukan
    
    # =========================================================================
    # LANGKAH 1: Hitung nilai h = BASE^(m-1) mod PRIME
    # Nilai ini digunakan untuk menghapus digit terdepan saat rolling
    # =========================================================================
    h = 1
    for i in range(m - 1):
        h = (h * BASE) % PRIME
    
    # =========================================================================
    # LANGKAH 2: Hitung hash awal untuk pattern dan window pertama teks
    # Menggunakan rumus: H = (c[0]*BASE^(m-1) + c[1]*BASE^(m-2) + ... + c[m-1])
    # =========================================================================
    pattern_hash = 0
    text_hash = 0
    
    for i in range(m):
        # ord() mengkonversi karakter ke nilai ASCII
        pattern_hash = (BASE * pattern_hash + ord(pattern_lower[i])) % PRIME
        text_hash = (BASE * text_hash + ord(text_lower[i])) % PRIME
    
    # =========================================================================
    # LANGKAH 3: Slide pattern over text dan bandingkan hash
    # =========================================================================
    for i in range(n - m + 1):
        # Jika hash sama, verifikasi dengan perbandingan karakter
        # (untuk menghindari false positive akibat collision)
        if pattern_hash == text_hash:
            # Verifikasi character-by-character
            match = True
            for j in range(m):
                if text_lower[i + j] != pattern_lower[j]:
                    match = False
                    break
            
            if match:
                positions.append(i)
        
        # =====================================================================
        # LANGKAH 4: Hitung hash untuk window berikutnya (Rolling Hash)
        # Rumus: H_new = ((H_old - leading_char * h) * BASE + trailing_char) mod PRIME
        # =====================================================================
        if i < n - m:
            # Hapus karakter terdepan, geser, dan tambah karakter baru
            leading_char = ord(text_lower[i])
            trailing_char = ord(text_lower[i + m])
            
            text_hash = (BASE * (text_hash - leading_char * h) + trailing_char) % PRIME
            
            # Handle nilai hash negatif
            if text_hash < 0:
                text_hash += PRIME
    
    return positions


def highlight_text(text: str, pattern: str) -> str:
    """
    Highlight semua kemunculan pattern dalam teks dengan tag HTML <mark>.
    Menggunakan Rabin-Karp untuk menemukan posisi, bukan str.find().
    
    Args:
        text (str): Teks asli
        pattern (str): Pattern yang akan di-highlight
        
    Returns:
        str: Teks dengan pattern yang sudah di-highlight
    """
    positions = rabin_karp_search(text, pattern)
    
    if not positions:
        return text
    
    # Build hasil dengan mengganti dari belakang untuk menjaga index
    result = text
    pattern_len = len(pattern)
    
    for pos in sorted(positions, reverse=True):
        original = result[pos:pos + pattern_len]
        highlighted = f'<mark class="highlight">{original}</mark>'
        result = result[:pos] + highlighted + result[pos + pattern_len:]
    
    return result


# ==============================================================================
# OCR FUNCTION
# ==============================================================================

def extract_text_from_image(image_data) -> str:
    """
    Ekstrak teks dari gambar menggunakan Tesseract OCR.
    
    Args:
        image_data: Data gambar (file atau bytes)
        
    Returns:
        str: Teks yang diekstrak dari gambar
    """
    try:
        image = Image.open(image_data)
        
        # Konversi ke RGB jika diperlukan
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Ekstrak teks dengan Tesseract
        text = pytesseract.image_to_string(image, lang='eng+ind')
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"OCR Error: {str(e)}")


def extract_text_from_docx(file_data) -> str:
    """
    Ekstrak teks dari file DOCX.
    
    Args:
        file_data: Data file DOCX (BytesIO)
        
    Returns:
        str: Teks yang diekstrak
    """
    try:
        doc = Document(file_data)
        full_text = []
        
        # Ekstrak dari paragraf
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        
        # Ekstrak dari tabel
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    full_text.append(' | '.join(row_text))
        
        return '\n'.join(full_text)
    
    except Exception as e:
        raise Exception(f"DOCX Error: {str(e)}")


def extract_text_from_pdf(file_data) -> str:
    """
    Ekstrak teks dari file PDF.
    
    Args:
        file_data: Data file PDF (BytesIO)
        
    Returns:
        str: Teks yang diekstrak
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file_data)
        full_text = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                full_text.append(f"--- Halaman {page_num + 1} ---\n{page_text}")
        
        return '\n\n'.join(full_text)
    
    except Exception as e:
        raise Exception(f"PDF Error: {str(e)}")


def get_file_type(filename: str) -> str:
    """Menentukan tipe file berdasarkan ekstensi."""
    if not filename:
        return 'unknown'
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
        return 'image'
    elif ext in ['doc', 'docx']:
        return 'docx'
    elif ext == 'pdf':
        return 'pdf'
    return 'unknown'


# ==============================================================================
# FLASK ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Render halaman utama."""
    return render_template('index.html')


@app.route('/pricing')
def pricing():
    """Render halaman pricing."""
    return render_template('pricing.html')


@app.route('/about')
def about():
    """Render halaman about."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render halaman contact."""
    return render_template('contact.html')


@app.route('/batch')
def batch():
    """Render halaman batch processing."""
    return render_template('batch.html')


@app.route('/ocr')
def ocr():
    """Render halaman OCR Scanner."""
    return render_template('ocr.html')


@app.route('/document')
def document():
    """Render halaman Document Parser."""
    return render_template('document.html')


# Login and Signup routes are now handled by auth blueprint


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint untuk menganalisis relevansi dokumen.
    Mendukung: Image (JPG, PNG), DOCX, PDF
    """
    try:
        # Validasi input - support both 'file' and 'image' keys
        uploaded_file = request.files.get('file') or request.files.get('image')
        
        if not uploaded_file:
            return jsonify({'success': False, 'error': 'Tidak ada file yang diunggah'}), 400
        
        keyword = request.form.get('keyword', '').strip()
        
        if uploaded_file.filename == '':
            return jsonify({'success': False, 'error': 'Tidak ada file yang dipilih'}), 400
        
        if not keyword:
            return jsonify({'success': False, 'error': 'Variabel riset tidak boleh kosong'}), 400
        
        # Tentukan tipe file
        filename = uploaded_file.filename
        file_type = get_file_type(filename)
        file_bytes = BytesIO(uploaded_file.read())
        
        # Ekstrak teks berdasarkan tipe file
        if file_type == 'image':
            extracted_text = extract_text_from_image(file_bytes)
            # Generate preview untuk gambar
            file_bytes.seek(0)
            image_base64 = base64.b64encode(file_bytes.read()).decode('utf-8')
            file_bytes.seek(0)
            img = Image.open(file_bytes)
            mime = f"image/{img.format.lower()}" if img.format else "image/png"
            file_preview = f"data:{mime};base64,{image_base64}"
            
        elif file_type == 'docx':
            extracted_text = extract_text_from_docx(file_bytes)
            file_preview = None  # Tidak ada preview untuk dokumen
            
        elif file_type == 'pdf':
            extracted_text = extract_text_from_pdf(file_bytes)
            file_preview = None  # Tidak ada preview untuk PDF
            
        else:
            return jsonify({
                'success': False, 
                'error': 'Tipe file tidak didukung. Gunakan: JPG, PNG, DOCX, atau PDF'
            }), 400
        
        if not extracted_text:
            return jsonify({
                'success': True,
                'is_relevant': False,
                'extracted_text': '(Tidak ada teks yang terdeteksi)',
                'highlighted_text': '(Tidak ada teks yang terdeteksi)',
                'match_count': 0,
                'positions': [],
                'image_preview': None,
                'file_type': file_type,
                'filename': filename
            })
        
        # Cari keyword menggunakan Rabin-Karp
        positions = rabin_karp_search(extracted_text, keyword)
        is_relevant = len(positions) > 0
        
        # Highlight teks jika ditemukan
        highlighted_text = highlight_text(extracted_text, keyword) if is_relevant else extracted_text
        
        # Generate AI Summary
        ai_result = generate_ai_summary(extracted_text)
        
        return jsonify({
            'success': True,
            'is_relevant': is_relevant,
            'extracted_text': extracted_text,
            'highlighted_text': highlighted_text,
            'match_count': len(positions),
            'positions': positions,
            'keyword': keyword,
            'image_preview': file_preview,
            'file_type': file_type,
            'filename': filename,
            'ai_summary': ai_result.get('summary') if ai_result.get('success') else None,
            'ai_error': ai_result.get('error') if not ai_result.get('success') else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                    ASISTEN TINJAUAN PUSTAKA                          ║
    ║         Screening Referensi Fisik Berbasis OCR & Rabin-Karp          ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║   Teknologi:                                                         ║
    ║   • OCR: Tesseract (pytesseract)                                     ║
    ║   • Algorithm: Rabin-Karp dengan Rolling Hash                        ║
    ║   • Frontend: Bootstrap 5                                            ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║   Buka di browser: http://127.0.0.1:5000                             ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
