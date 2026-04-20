
  🗳️ Votely - Modern Multi-Voting Platform

  Votely adalah platform pemungutan suara (voting) modern dengan desain antarmuka (UI) kelas SaaS yang bersih, intuitif, dan responsif.
  Dibangun dengan fokus pada kemudahan penggunaan dan skalabilitas untuk pipeline CI/CD.

  !Python (https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
  !Flask (https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
  !TailwindCSS (https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC?style=for-the-badge&logo=tailwind-css)
  !Docker (https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)

  ---

  ✨ Fitur Utama

   - UI/UX Modern: Desain minimalis yang terinspirasi oleh Stripe dan Linear, menggunakan Tailwind CSS.
   - Pembuatan Poll Dinamis: Tambahkan atau hapus opsi voting secara real-time tanpa refresh halaman.
   - Tipe Voting Fleksibel: Mendukung pilihan tunggal (single choice) maupun banyak pilihan (multiple choice).
   - Pencegahan Duplikasi: Sistem pelacakan alamat IP untuk mencegah pengguna memberikan suara lebih dari sekali pada poll yang sama.
   - Visualisasi Hasil: Grafik progress bar yang elegan dengan animasi halus untuk melihat pemenang.
   - Siap CI/CD: Terintegrasi penuh dengan Docker dan Jenkins menggunakan unit testing Pytest.

  ---

  🛠️ Teknologi yang Digunakan

   - Backend: Python Flask
   - Database: SQLite (SQLAlchemy ORM)
   - Frontend: Jinja2 Templates, Tailwind CSS (via CDN), Vanilla JavaScript
   - Testing: Pytest
   - DevOps: Docker, Jenkins

  ---

  🚀 Cara Menjalankan

  1. Menggunakan Docker (Direkomendasikan)

  Pastikan Docker sudah terinstal di sistem Anda.

   1 # Build image
   2 docker build -t votely-app ./app
   3
   4 # Jalankan container
   5 docker run -p 8081:5000 votely-app
  Aplikasi akan tersedia di: http://localhost:8081

  2. Instalasi Lokal

    1 cd app
    2
    3 # Buat virtual environment
    4 python -m venv venv
    5 source venv/bin/activate  # Linux/macOS
    6 # venv\Scripts\activate   # Windows
    7
    8 # Instal dependensi
    9 pip install -r requirements.txt
   10
   11 # Jalankan aplikasi
   12 python main.py

  ---

  🧪 Pengujian (Testing)

  Proyek ini dilengkapi dengan suite pengujian otomatis untuk memastikan integritas logika bisnis.

   1 cd app
   2 python -m pytest tests/ -v

  Kasus Uji Mencakup:
   - Pembuatan voting baru.
   - Pengambilan data via API.
   - Validasi submit suara.
   - Pencegahan voting ganda (Duplicate IP check).

  ---

  📁 Struktur Proyek

    1 app/
    2 ├── main.py              # Entry point aplikasi
    3 ├── models.py            # Definisi Database (Voting, Option, Vote)
    4 ├── database.py          # Inisialisasi SQLAlchemy
    5 ├── routes/              # Logika API & Routing
    6 ├── templates/           # Halaman HTML (Jinja2)
    7 ├── static/              # Asset CSS & JS
    8 ├── tests/               # Unit Testing (Pytest)
    9 ├── Dockerfile           # Konfigurasi Container
   10 └── requirements.txt     # Daftar Dependensi

  ---

  🔗 API Endpoints

| Method | Endpoint       | Deskripsi                  |
|--------|--------------|---------------------------|
| GET    | /            | Beranda (Daftar Poll)     |
| GET    | /votings     | JSON API Daftar Poll      |
| GET    | /votings/<id>| Detail Poll & Form Vote   |
| POST   | /votings     | Membuat Poll Baru         |
| POST   | /vote        | Mengirim Suara            |
| GET    | /results/<id>| Visualisasi Hasil Voting  |

  ---

  ⚙️ Integrasi Jenkins

  Project ini dirancang untuk bekerja dalam pipeline Jenkins:
   1. Build: Dockerize aplikasi.
   2. Test: Menjalankan pytest di dalam container.
   3. Deploy: Push image ke registry atau deploy ke staging server.
