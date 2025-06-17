import logging
import joblib
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class EnergyPredictor:
    def __init__(self, model_path, data_path):
        """
        Constructor (metode __init__) akan dipanggil saat objek dibuat.
        Tugasnya adalah memuat aset-aset penting (model dan data).
        """
        try:
            logging.info("Memuat model dari path: %s", model_path)
            self.model = joblib.load(model_path)
            logging.info("Model berhasil dimuat.")

            logging.info(f"Memuat data historis dari: {data_path}")
            self.df_history = pd.read_csv(data_path, index_col='datetime', parse_dates=True)
            logging.info("Data historis berhasil dimuat.")
        except FileNotFoundError as e:
            logging.error(f"Error: File tidak ditemukan! Pastikan path benar. {e}")
            raise e
        except Exception as e:
            logging.error(f"Terjadi error saat inisialisasi: {e}")
            raise e

    def forecast(self, steps=24):
        """Metode untuk membuat prediksi konsumsi ke depan."""
        if self.model:
            return self.model.forecast(steps=steps)
        return None

    def get_device_status(self):
        """Metode untuk deteksi status perangkat (menggunakan rule-based)."""
        if not self.df_history.empty:
            data_terakhir = self.df_history.iloc[-1]
            status = {
                'Dapur (Sub_metering_1)': 'Aktif' if data_terakhir['Sub_metering_1'] > 1.0 else 'Tidak Aktif',
                'Laundry (Sub_metering_2)': 'Aktif' if data_terakhir['Sub_metering_2'] > 1.0 else 'Tidak Aktif',
                'AC & Pemanas (Sub_metering_3)': 'Aktif' if data_terakhir['Sub_metering_3'] > 10.0 else 'Tidak Aktif'
            }
            return status
        return {}

    def get_usage_history(self, hours=168):
        """Metode untuk mendapatkan data historis (default 7 hari)."""
        if not self.df_history.empty:
            return self.df_history.tail(hours)
        return pd.DataFrame()

    def get_realtime_usage(self):
        """Metode untuk simulasi data konsumsi real-time."""
        if not self.df_history.empty:
            return self.df_history.iloc[-1]
        return None
