#!/usr/bin/env python3
"""
Simple script to run the IDS ML server
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Check if we're in the right directory
    if not Path("backend/app.py").exists():
        print("❌ Error: backend/app.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if required data files exist
    if not Path("KDDTrain+.txt").exists() or not Path("KDDTest+.txt").exists():
        print("❌ Error: NSL-KDD dataset files not found!")
        print("Please download KDDTrain+.txt and KDDTest+.txt from:")
        print("https://www.unb.ca/cic/datasets/nsl.html")
        print("And place them in the project root directory.")
        sys.exit(1)
    
    print("🚀 Starting IDS ML Server...")
    print("📊 Frontend will be available at: http://127.0.0.1:5000")
    print("🔧 API endpoints:")
    print("   - POST /train - Train the model")
    print("   - POST /predict - Make predictions")
    print("   - GET /plots/<filename> - View generated plots")
    print("\n" + "="*50)
    
    try:
        # Run the Flask server
        os.chdir("backend")
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()