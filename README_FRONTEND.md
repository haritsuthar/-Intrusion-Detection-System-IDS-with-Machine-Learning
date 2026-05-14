# IDS ML Frontend (Flask + HTML/JS)

## What this provides
- `POST /train` trains the RandomForest on `KDDTrain+.txt` / `KDDTest+.txt` and generates:
  - `confusion_matrix.png`
  - `roc_curve.png`
  - `feature_importance.png`
- `POST /predict` predicts **Normal vs Attack** from input features
- `GET /plots/<name>` serves those PNGs
- `frontend/index.html` is a simple UI calling the endpoints.

## Requirements
Make sure you have the dataset files in the repo root:
- `KDDTrain+.txt`
- `KDDTest+.txt`

Install Python deps:
```bash
pip install -r requirements.txt
```

## Run backend
```bash
python -c "from backend.app import app; app.run(host='127.0.0.1', port=5000, debug=True)"
```

## Open frontend
Open this file in your browser:
- `frontend/index.html`

Then:
1. Click **Train model**
2. Fill features (or use JSON textarea) and click **Predict**
3. View plots below

## Model artifacts
Artifacts are saved into `artifacts/` after training:
- `model.joblib`
- `scaler.joblib`
- `encoders.joblib`
- `config.json`

## Notes
- Training can take a while.
- Feature inputs must match the names used in `frontend/app.js`.
