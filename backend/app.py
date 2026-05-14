from __future__ import annotations

import os
import sys
import json
from typing import Any, Dict

# Add parent directory to path to import ids_ml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS

import ids_ml

import joblib
import matplotlib
matplotlib.use("Agg")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
PLOTS_DIR = os.path.join(BASE_DIR)  # ids_ml.py writes plots into repo root
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(ARTIFACT_DIR, exist_ok=True)

MODEL_PATH = os.path.join(ARTIFACT_DIR, "model.joblib")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "scaler.joblib")
ENCODERS_PATH = os.path.join(ARTIFACT_DIR, "encoders.joblib")
CONFIG_PATH = os.path.join(ARTIFACT_DIR, "config.json")

app = Flask(__name__, static_folder=None)
CORS(app)  # Enable CORS for all routes


def _ensure_plots_exist() -> Dict[str, str]:
    mapping = {
        "confusion_matrix": os.path.join(PLOTS_DIR, "confusion_matrix.png"),
        "roc_curve": os.path.join(PLOTS_DIR, "roc_curve.png"),
        "feature_importance": os.path.join(PLOTS_DIR, "feature_importance.png"),
    }
    out: Dict[str, str] = {}
    for key, path in mapping.items():
        if os.path.exists(path):
            out[key] = f"/plots/{os.path.basename(path)}"
    return out


def _send_png_file(path: str) -> Response:
    with open(path, "rb") as f:
        data = f.read()
    return Response(data, mimetype="image/png")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/train")
def train():
    try:
        ids_ml.train_and_save_artifacts(
            model_path=MODEL_PATH,
            scaler_path=SCALER_PATH,
            encoders_path=ENCODERS_PATH,
            config_path=CONFIG_PATH,
            plots_dir=PLOTS_DIR,
        )

        return jsonify({
            "status": "trained",
            "plots": _ensure_plots_exist(),
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.post("/predict")
def predict():
    try:
        payload = request.get_json(force=True)
        if isinstance(payload, dict) and "features" in payload:
            features = payload["features"]
        else:
            features = payload

        if not (os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(ENCODERS_PATH) and os.path.exists(CONFIG_PATH)):
            raise FileNotFoundError("Model artifacts not found. Train first.")

        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoders = joblib.load(ENCODERS_PATH)

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        feature_order = config["feature_order"]

        result = ids_ml.predict_from_features(
            model=model,
            scaler=scaler,
            encoders=encoders,
            feature_order=feature_order,
            raw_features=features,
        )
        result["plots"] = _ensure_plots_exist()
        return jsonify(result)

    except FileNotFoundError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400


@app.get("/plots/<path:filename>")
def plots(filename: str):
    allowed = {"confusion_matrix.png", "roc_curve.png", "feature_importance.png"}
    if filename not in allowed:
        return jsonify({"status": "error", "error": "Invalid plot"}), 404

    path = os.path.join(PLOTS_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"status": "error", "error": "Plot not found"}), 404

    try:
        return _send_png_file(path)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# Serve frontend files
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

