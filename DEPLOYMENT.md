# 🚀 Panduan Deploy Netra ke VPS

Aplikasi ini **sangat bisa** dan **siap** untuk dideploy ke VPS (Virtual Private Server). Karena sudah menggunakan Docker, prosesnya menjadi sangat mudah.

## 🛠️ Persyaratan VPS
- **OS**: Ubuntu 20.04 / 22.04 LTS (Rekomendasi)
- **RAM**: Minimal 2GB (karena menjalankan Tesseract OCR dan Gunicorn)
- **Disk**: Minimal 10GB
- **Cores**: 1-2 vCPU

## ⚡ Langkah-langkah Deploy

### 1. Masuk ke VPS
SSH ke server VPS kamu:
```bash
ssh root@ip-vps-kamu
```

### 2. Install Docker & Docker Compose
Jalankan perintah ini satu per satu:
```bash
# Update repository
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose Plugin
sudo apt install docker-compose-plugin -y
```

### 3. Clone Repository
Ambil kode terbaru dari GitHub:
```bash
git clone https://github.com/dimasu21/Netra.git
cd Netra
```

### 4. Setup Environment Variable
Buat file `.env` di server (karena file ini tidak di-upload ke GitHub):
```bash
nano .env
```
Isi dengan API Key kamu:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Tekan `Ctrl+X`, lalu `Y`, lalu `Enter` untuk save)*

### 5. Jalankan Aplikasi
Build dan jalankan container di background:
```bash
docker compose up -d --build
```

### 6. Cek Status
Pastikan container berjalan:
```bash
docker compose ps
```

Aplikasi sekarang aktif di: `http://ip-vps-kamu:5000`

---

## 🌐 (Opsional) Setup Domain & HTTPS
Jika ingin menggunakan domain (misal: `netra.com`) dan HTTPS, gunakan **Nginx Proxy Manager** atau setup Nginx manual sebagai Reverse Proxy.

### Konfigurasi Nginx Sederhana
1. Install Nginx: `sudo apt install nginx`
2. Buat config: `sudo nano /etc/nginx/sites-available/netra`
```nginx
server {
    server_name domain-kamu.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
3. Aktifkan: `sudo ln -s /etc/nginx/sites-available/netra /etc/nginx/sites-enabled/`
4. Restart Nginx: `sudo systemctl restart nginx`
