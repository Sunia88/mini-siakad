# mini-SIAKAD

Aplikasi contoh untuk Bab 16 buku ajar *Pengujian dan Pemeliharaan Sistem*.
Hanya untuk praktikum; jangan digunakan sebagai sistem produksi.

Langkah cepat (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements-dev.txt
    python app.py                      # jendela 1
    pytest tests/unit tests/api        # jendela 2
    playwright install chromium
    pytest tests/e2e
    k6 run tests/kinerja/krs.js
    cd uat; python sus.py              # Praktikum 10 (skor SUS)

Lihat Bab 16 untuk langkah lengkap setiap praktikum.
