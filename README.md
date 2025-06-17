# Leastric – Prediksi dan Monitoring Energi Cerdas

**Leastric** adalah solusi MVP (Minimum Viable Product) yang dikembangkan untuk menjawab tantangan teknologi dari startup dengan nama yang sama dalam kompetisi IDCamp 2024 Developer Challenge #2 x SheHacks. Fokus utama dari proyek ini adalah menciptakan sistem prediksi dan monitoring energi berbasis data yang dapat membantu pengguna dalam mengelola konsumsi listrik secara efisien.

Live Demo: [https://leastric.pythonanywhere.com](https://leastric.pythonanywhere.com)

## Deskripsi Singkat

Leastric menyediakan dashboard analitik yang mampu memproyeksikan konsumsi listrik selama 24 jam ke depan menggunakan model time-series SARIMA. Selain itu, aplikasi ini juga memantau aktivitas perangkat seperti Dapur, Laundry, AC, dan Pemanas berdasarkan data sub-metering terbaru, serta menampilkan visualisasi data historis selama 7 hari terakhir.

Dengan fitur-fitur tersebut, Leastric diharapkan dapat membantu pengguna, khususnya pengelola gedung dan sektor industri, dalam merencanakan anggaran energi, mengantisipasi beban puncak, dan mengambil keputusan strategis terkait efisiensi energi.

## Teknologi yang Digunakan

Solusi ini dikembangkan menggunakan Python sebagai bahasa utama. Proses analisis dan pemodelan dilakukan dengan bantuan Pandas, NumPy, dan Statsmodels. Model yang telah dilatih disimpan dalam format `.pkl` menggunakan Joblib.

Untuk backend, digunakan Flask sebagai web framework RESTful API yang menyuplai data ke frontend. Antarmuka pengguna dibangun dengan HTML, CSS, dan JavaScript, serta Chart.js untuk visualisasi data. Aplikasi ini dihosting secara publik melalui PythonAnywhere.

## Instalasi & Menjalankan Aplikasi

1. Clone repositori:
   
   ```bash
   git clone https://github.com/RozhakDev/Leastric.git
   cd Leastric
   ```

2. Install dependensi:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:
   
   ```bash
   python run.py
   ```

Aplikasi dapat diakses melalui `http://127.0.0.1:5000` di browser.

## Struktur Direktori

```
Leastric/
├── app/
│   ├── __init__.py      # Factory aplikasi Flask
│   └── routes.py        # Mendefinisikan endpoint API
├── data/
│   ├── household_power_consumption.csv  # Dataset mentah
│   └── data_listrik_bersih_per_jam.csv  # Dataset yang sudah diolah
├── ml/
│   └── prediction.py    # Kelas untuk prediksi & logika bisnis
├── notebooks/
│   └── Leastric_Energy_Efficiency.ipynb  # Notebook analisis & training model
├── static/
│   ├── css/
│   │   └── style.css    # File styling
│   └── js/
│       └── script.js    # Logika interaktif frontend
├── templates/
│   └── index.html       # Halaman utama dashboard
├── run.py               # Titik masuk untuk menjalankan aplikasi
└── requirements.txt     # Daftar dependensi Python
```

## Kontribusi & Masukan

Solusi ini masih dalam tahap MVP dan terbuka untuk pengembangan lebih lanjut. Jika Anda menemukan bug, memiliki masukan, atau ide pengembangan, silakan ajukan melalui fitur Issues di repositori ini.