#!/usr/bin/env python3
"""
Quick test script to verify Flask app endpoints work correctly
"""

import requests
import json
import time
import subprocess
import sys
import threading
from datetime import datetime

def test_flask_app():
    """Test Flask app endpoints"""
    base_url = "http://127.0.0.1:4506"
    
    print("Testing Flask application endpoints...")
    
    # Test basic endpoints
    endpoints_to_test = [
        ("/incidents", "GET"),
        ("/insights", "GET"), 
        ("/reports/summary", "GET"),
        ("/logs", "GET")
    ]
    
    for endpoint, method in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                print(f"✅ {method} {endpoint}: {response.status_code}")
                if response.status_code != 200:
                    print(f"   Response: {response.text}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} {endpoint}: Error - {e}")
    
    # Test POST endpoints with sample data
    try:
        # Test incident creation
        incident_data = {
            "description": "Test server connectivity issue",
            "priority": "Medium",
            "use_ai": True
        }
        
        response = requests.post(f"{base_url}/incidents", 
                               json=incident_data, 
                               timeout=5)
        print(f"✅ POST /incidents (JSON): {response.status_code}")
        
        # Test with form data too
        response = requests.post(f"{base_url}/incidents", 
                               data=incident_data, 
                               timeout=5)
        print(f"✅ POST /incidents (Form): {response.status_code}")
        
        # Test AI analysis
        analysis_data = {"description": "Database connection timeout"}
        response = requests.post(f"{base_url}/incidents/analyze", 
                               json=analysis_data, 
                               timeout=5)
        print(f"✅ POST /incidents/analyze (JSON): {response.status_code}")
        
        response = requests.post(f"{base_url}/incidents/analyze", 
                               data=analysis_data, 
                               timeout=5)
        print(f"✅ POST /incidents/analyze (Form): {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ POST requests: Error - {e}")

if __name__ == "__main__":
    print("Flask App Test Suite")
    print("=" * 40)
    print("Note: Make sure Flask app is running on port 4506")
    print("Run: python app.py in another terminal")
    print("=" * 40)
    
    input("Press Enter when Flask app is running...")
    test_flask_app()