from flask import Flask, jsonify
from ai_processor import AIProcessor
import json
import os
import sys

app = Flask(__name__)

@app.route('/status')
def status():
    """Application status and health check"""
    try:
        # Test AI processor
        ai = AIProcessor()
        ai_test = ai.analyze_incident("test incident")
        ai_status = "OK" if 'suggested_priority' in ai_test else "ERROR"
        
        # Check files
        incidents_exist = os.path.exists('incidents.json')
        logs_exist = os.path.exists('incident_log.txt')
        
        # Test incidents loading
        incidents = []
        try:
            if incidents_exist:
                with open('incidents.json', 'r') as f:
                    incidents = json.load(f)
            incidents_status = "OK"
        except Exception as e:
            incidents_status = f"ERROR: {e}"
        
        return jsonify({
            'status': 'OK',
            'ai_processor': ai_status,
            'incidents_file': 'EXISTS' if incidents_exist else 'NOT_FOUND',
            'logs_file': 'EXISTS' if logs_exist else 'NOT_FOUND', 
            'incidents_count': len(incidents),
            'incidents_load': incidents_status,
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        })
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    import sys
    app.run(host='127.0.0.1', port=4507, debug=True)