#!/usr/bin/env python3
"""
Test script for the IDS ML API endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False

def test_prediction():
    """Test the prediction endpoint with sample data"""
    print("🔍 Testing prediction endpoint...")
    
    sample_data = {
        "features": {
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "duration": 0,
            "src_bytes": 181,
            "dst_bytes": 5450,
            "land": 0,
            "wrong_fragment": 0,
            "urgent": 0,
            "hot": 0,
            "num_failed_logins": 0,
            "logged_in": 1,
            "num_compromised": 0,
            "root_shell": 0,
            "su_attempted": 0,
            "num_root": 0,
            "num_file_creations": 0,
            "num_shells": 0,
            "num_access_files": 0,
            "num_outbound_cmds": 0,
            "is_host_login": 0,
            "is_guest_login": 0,
            "count": 8,
            "srv_count": 8,
            "serror_rate": 0.0,
            "srv_serror_rate": 0.0,
            "rerror_rate": 0.0,
            "srv_rerror_rate": 0.0,
            "same_srv_rate": 1.0,
            "diff_srv_rate": 0.0,
            "srv_diff_host_rate": 0.0,
            "dst_host_count": 9,
            "dst_host_srv_count": 9,
            "dst_host_same_srv_rate": 1.0,
            "dst_host_diff_srv_rate": 0.0,
            "dst_host_same_src_port_rate": 0.11,
            "dst_host_srv_diff_host_rate": 0.0,
            "dst_host_serror_rate": 0.0,
            "dst_host_srv_serror_rate": 0.0,
            "dst_host_rerror_rate": 0.0,
            "dst_host_srv_rerror_rate": 0.0
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful")
            print(f"   Result: {result.get('prediction', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            return True
        elif response.status_code == 400:
            error = response.json()
            if "Model artifacts not found" in error.get('error', ''):
                print("⚠️  Model not trained yet. Train the model first.")
                return False
            else:
                print(f"❌ Prediction failed: {error.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        return False

def test_training():
    """Test the training endpoint"""
    print("🔍 Testing training endpoint...")
    print("⚠️  This may take several minutes...")
    
    try:
        response = requests.post(f"{BASE_URL}/train")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Training successful")
            print(f"   Status: {result.get('status', 'Unknown')}")
            if 'plots' in result:
                print(f"   Plots generated: {len(result['plots'])}")
            return True
        else:
            error = response.json()
            print(f"❌ Training failed: {error.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Training test failed: {e}")
        return False

def main():
    print("🧪 IDS ML API Test Suite")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health():
        print("❌ Server is not responding. Please start the server first.")
        return
    
    print()
    
    # Test prediction (might fail if model not trained)
    prediction_works = test_prediction()
    
    print()
    
    # If prediction failed due to missing model, offer to train
    if not prediction_works:
        user_input = input("Would you like to train the model now? (y/N): ")
        if user_input.lower() in ['y', 'yes']:
            if test_training():
                print("\n🔄 Retesting prediction after training...")
                test_prediction()
    
    print("\n✅ Test suite completed!")

if __name__ == "__main__":
    main()