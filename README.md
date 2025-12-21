# 📚 NETRA - Asisten Tinjauan Pustaka

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**Literature Review Assistant dengan AI-Powered Analysis**

</div>

---

## ✨ Fitur Utama

- 🔍 **Document Parser** - Ekstrak dan analisis teks dari PDF, DOCX
- 📷 **OCR Scanner** - Ekstrak teks dari gambar (JPG, PNG) dengan Tesseract
- 📊 **Batch Processing** - Proses multiple dokumen sekaligus
- 🧠 **AI Summary** - Ringkasan otomatis menggunakan Groq AI
- 🔎 **Rabin-Karp Algorithm** - Pencarian pattern dan deteksi plagiarisme
- 📱 **Responsive Design** - Tampilan optimal di desktop dan mobile

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Backend Language |
| **Flask** | Web Framework |
| **Tesseract OCR** | Optical Character Recognition |
| **PyMuPDF (fitz)** | PDF Processing |
| **python-docx** | DOCX Processing |
| **Groq API** | AI-powered Summarization |
| **Docker** | Containerization |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih baru
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) terinstall
- Groq API Key (untuk fitur AI Summary)

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/netra.git
   cd netra
   ```

2. **Buat virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   # Buat file .env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Jalankan aplikasi**
   ```bash
   python app.py
   ```

6. **Buka browser**
   ```
   http://localhost:5000
   ```

### 🐳 Docker Installation

```bash
# Build image
docker build -t netra .

# Run container
docker run -p 5000:5000 netra

# Atau dengan docker-compose
docker-compose up
```

## 📁 Struktur Project

```
netra/
├── app.py                 # Main Flask application
├── rabin_karp.py          # Rabin-Karp algorithm module
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose config
├── Procfile              # Deployment config
├── static/               # CSS, JS, images
└── templates/            # HTML templates
    ├── index.html        # Landing page
    ├── document.html     # Document parser
    ├── ocr.html          # OCR scanner
    ├── batch.html        # Batch processing
    ├── pricing.html      # Pricing page
    ├── about.html        # About page
    ├── contact.html      # Contact page
    ├── login.html        # Login page
    └── signup.html       # Signup page
```

## 🔧 Konfigurasi Tesseract

### Windows
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Linux
```bash
sudo apt install tesseract-ocr tesseract-ocr-ind
```

### macOS
```bash
brew install tesseract
```

## 📖 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Halaman utama |
| GET | `/document` | Document Parser |
| GET | `/ocr` | OCR Scanner |
| GET | `/batch` | Batch Processing |
| POST | `/analyze` | Analisis dokumen |
| GET | `/pricing` | Halaman pricing |
| GET | `/about` | Halaman about |
| GET | `/contact` | Halaman contact |

## 🧮 Algoritma Rabin-Karp

Aplikasi ini menggunakan algoritma **Rabin-Karp** untuk:
- Pencarian pattern dalam teks
- Deteksi plagiarisme
- Highlighting teks yang cocok

```
Time Complexity: O(n + m) average case
Space Complexity: O(1)
```

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Project Link: [https://github.com/yourusername/netra](https://github.com/yourusername/netra)

---

<div align="center">
Made with ❤️ for Indonesian Researchers
</div>
