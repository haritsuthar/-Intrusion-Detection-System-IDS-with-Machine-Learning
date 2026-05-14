# 🛡️ Intrusion Detection System (IDS) - Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/intrusion-detection-system.svg)](https://github.com/YOUR_USERNAME/intrusion-detection-system/stargazers)

A comprehensive machine learning-based intrusion detection system using the NSL-KDD dataset. This project features a Random Forest classifier with a modern web interface for training models and detecting network intrusions.

## ⚠️ **Important: Dataset Required**

This project requires the NSL-KDD dataset files. **Due to licensing restrictions, these files are not included in the repository.**

### 📥 **Download Dataset:**
1. Visit: **https://www.unb.ca/cic/datasets/nsl.html**
2. Download these files:
   - `KDDTrain+.txt` (Training data)
   - `KDDTest+.txt` (Testing data)
3. Place both files in the **project root directory**

**File structure should look like:**
```
intrusion-detection-system/
├── KDDTrain+.txt          ← Download this
├── KDDTest+.txt           ← Download this
├── ids_ml.py
├── backend/
├── frontend/
└── ...
```

## ✨ Features

- **🤖 Machine Learning**: Random Forest classifier trained on NSL-KDD dataset
- **🌐 Web Interface**: Modern, responsive frontend with real-time predictions
- **📊 Visualizations**: Confusion matrix, ROC curve, and feature importance plots
- **🔍 Real-time Analysis**: Instant threat detection with confidence scores
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🚀 Easy Setup**: One-click startup scripts

## 🏗️ Architecture

```
├── ids_ml.py           # Core ML pipeline and model training
├── backend/
│   └── app.py          # Flask API server
├── frontend/
│   ├── index.html      # Modern web interface
│   └── app.js          # Frontend JavaScript
├── artifacts/          # Generated model files
├── requirements.txt    # Python dependencies
└── run_server.py       # Startup script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- NSL-KDD dataset files (see setup instructions below)

### 1. Download Dataset

Download the NSL-KDD dataset files and place them in the project root:
- `KDDTrain+.txt`
- `KDDTest+.txt`

**Download from**: https://www.unb.ca/cic/datasets/nsl.html

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

**Option A: Python script**
```bash
python run_server.py
```

**Option B: Windows batch file**
```cmd
run_server.bat
```

**Option C: Manual startup**
```bash
cd backend
python app.py
```

### 4. Access the Application

Open your browser and navigate to: **http://127.0.0.1:5000**

## 🎯 Usage

### Training the Model

1. Click **"🚀 Start Training"** in the web interface
2. Wait for the training process to complete (may take a few minutes)
3. View the generated performance plots and metrics

### Making Predictions

**Quick Predict:**
- Use the simplified form with common network features
- Adjust protocol, service, bytes, and connection parameters
- Click **"🔮 Predict Threat"** to analyze

**Advanced Analysis:**
- Use the JSON input for all 41 features
- Paste custom network connection data
- Get detailed threat analysis with confidence scores

## 📊 Model Performance

The Random Forest classifier achieves:
- **High Accuracy**: Typically >95% on the NSL-KDD test set
- **Low False Positives**: Optimized for real-world deployment
- **Fast Predictions**: Real-time threat detection

### Visualizations

- **Confusion Matrix**: Shows prediction accuracy breakdown
- **ROC Curve**: Displays model performance across thresholds
- **Feature Importance**: Identifies key network features for detection

## 🔧 API Endpoints

### Training
```http
POST /train
```
Trains the model and generates performance plots.

### Prediction
```http
POST /predict
Content-Type: application/json

{
  "features": {
    "protocol_type": "tcp",
    "service": "http",
    "flag": "SF",
    "duration": 0,
    "src_bytes": 181,
    "dst_bytes": 5450,
    ...
  }
}
```

### Plots
```http
GET /plots/confusion_matrix.png
GET /plots/roc_curve.png
GET /plots/feature_importance.png
```

## 🛠️ Development

### Project Structure

- **`ids_ml.py`**: Core machine learning pipeline
  - Data loading and preprocessing
  - Model training and evaluation
  - Visualization generation

- **`backend/app.py`**: Flask web server
  - REST API endpoints
  - Model serving
  - Static file serving

- **`frontend/`**: Modern web interface
  - Responsive design
  - Real-time predictions
  - Interactive visualizations

### Key Features

- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error messages
- **Memory Management**: Proper plot cleanup
- **Responsive UI**: Mobile-friendly interface

## 📈 Network Features

The system analyzes 41 network connection features:

**Basic Features:**
- Duration, protocol type, service, flag
- Source/destination bytes
- Connection counts and rates

**Content Features:**
- Failed logins, compromised conditions
- Root shell access, file operations

**Traffic Features:**
- Same service rates, error rates
- Host-based network statistics

## 🔒 Security Classifications

**Attack Types Detected:**
- **DoS**: Denial of Service attacks
- **Probe**: Surveillance and probing
- **R2L**: Remote to Local attacks
- **U2R**: User to Root attacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- NSL-KDD dataset creators
- scikit-learn community
- Flask framework developers

---

**Made with ❤️ for network security**