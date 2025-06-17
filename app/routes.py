from flask import Blueprint, jsonify
import pandas as pd
import logging
from ml.prediction import EnergyPredictor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

MODEL_PATH = 'data/model_prediksi_listrik.pkl'
DATA_PATH = 'data/data_listrik_bersih_per_jam.csv'

logging.info("Inisialisasi EnergyPredictor dengan model dan data.")
predictor = EnergyPredictor(model_path=MODEL_PATH, data_path=DATA_PATH)
logging.info("EnergyPredictor berhasil diinisialisasi.")


main_api = Blueprint('main_api', __name__)


@main_api.route('/api/predict')
def predict_route():
    """Endpoint untuk mendapatkan prediksi konsumsi listrik 24 jam ke depan."""
    try:
        prediction = predictor.forecast(steps=24)

        prediction_json = {
            (prediction.index[i]).strftime('%Y-%m-%d %H:%M:%S'): prediction.iloc[i]
            for i in range(len(prediction))
        }
        return jsonify(prediction_json)
    except Exception as e:
        logging.error(f"Error saat mendapatkan prediksi: {e}")
        return jsonify({'error': str(e)}), 500


@main_api.route('/api/device_breakdown')
def device_breakdown_route():
    """Endpoint untuk mendapatkan status perangkat berdasarkan data terakhir."""
    try:
        status = predictor.get_device_status()
        return jsonify(status)
    except Exception as e:
        logging.error(f"Error saat mendapatkan status perangkat: {e}")
        return jsonify({'error': str(e)}), 500


@main_api.route('/api/usage/history')
def usage_history_route():
    """Endpoint untuk mendapatkan data historis konsumsi (7 hari terakhir)."""
    try:
        history_data = predictor.get_usage_history(hours=168) # 7 hari terakhir
        history_json = {
            (history_data.index[i]).strftime('%Y-%m-%d %H:%M:%S'): history_data['Global_active_power'].iloc[i]
            for i in range(len(history_data))
        }
        return jsonify(history_json)
    except Exception as e:
        logging.error(f"Error saat mendapatkan data historis: {e}")
        return jsonify({'error': str(e)}), 500

@main_api.route('/api/usage/realtime')
def usage_realtime_route():
    """Endpoint untuk simulasi data konsumsi real-time."""
    try:
        realtime_data = predictor.get_realtime_usage()
        realtime_json = {
            'timestamp': realtime_data.name.strftime('%Y-%m-%d %H:%M:%S'),
            'konsumsi_kw': realtime_data['Global_active_power']
        }
        return jsonify(realtime_json)
    except Exception as e:
        logging.error(f"Error saat mendapatkan data konsumsi real-time: {e}")
        return jsonify({'error': str(e)}), 500
