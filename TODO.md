# TODO: Frontend for IDS ML

- [ ] Step 1: Refactor `ids_ml.py` to expose reusable functions and enable saving/loading model artifacts (joblib), and avoid `plt.show()` for API use.
- [x] Step 2: Create Flask backend (`backend/app.py`) with endpoints for:
  - [x] `POST /train` (train + save artifacts + generate plots)
  - [x] `POST /predict` (run preprocessing + predict using saved artifacts)
  - [x] `GET /plots/<name>` (serve generated PNGs)
- [x] Step 3: Create frontend (`frontend/index.html`, `frontend/app.js`) that:
  - [x] Calls `/train` via button
  - [x] Provides prediction input form
  - [x] Displays prediction result and confidence
  - [x] Displays confusion matrix / ROC images after training
- [x] Step 4: Add `README_FRONTEND.md` with run steps.
- [ ] Step 5: Test locally by running backend and using browser to train + predict.



