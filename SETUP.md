# 🛠️ Setup Instructions

## Prerequisites

- **Python 3.8+** installed on your system
- **Git** installed (for cloning the repository)
- **Web browser** for accessing the interface

## Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/intrusion-detection-system.git
cd intrusion-detection-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download NSL-KDD Dataset
1. Visit: https://www.unb.ca/cic/datasets/nsl.html
2. Download these files:
   - `KDDTrain+.txt`
   - `KDDTest+.txt`
3. Place them in the project root directory

### 4. Run the Application

**Option A: Using the startup script**
```bash
python run_server.py
```

**Option B: Windows users**
```cmd
run_server.bat
```

**Option C: Manual startup**
```bash
cd backend
python app.py
```

### 5. Access the Application
Open your browser and go to: **http://127.0.0.1:5000**

## Usage

1. **Train the Model**: Click "🚀 Start Training" (takes 2-3 minutes)
2. **Make Predictions**: Use the form to analyze network traffic
3. **View Analytics**: Check the generated performance plots

## Troubleshooting

### Common Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Dataset not found" error:**
- Ensure `KDDTrain+.txt` and `KDDTest+.txt` are in the project root
- Check file names are exactly as shown (case-sensitive)

**Port already in use:**
- Change the port in `backend/app.py` line: `app.run(host="127.0.0.1", port=5001)`

### Testing the API
```bash
python test_api.py
```

## Project Structure
```
├── 🧠 ids_ml.py              # Core ML pipeline
├── 🌐 backend/app.py         # Flask server
├── 🎨 frontend/              # Web interface
├── 📊 artifacts/             # Generated models
├── 🚀 run_server.py          # Startup script
├── 🧪 test_api.py            # API tests
└── 📖 README.md              # Documentation
```

## Development

### Adding New Features
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### API Endpoints
- `GET /` - Web interface
- `POST /train` - Train model
- `POST /predict` - Make predictions
- `GET /plots/<filename>` - View plots

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the server logs for error messages
3. Open an issue on GitHub with details