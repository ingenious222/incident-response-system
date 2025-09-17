from flask import Flask, request, jsonify, send_file
import json
import uuid
import os
from datetime import datetime, date, timedelta
from ai_processor import AIProcessor

app = Flask(__name__)

# Configuration
INCIDENT_FILE = 'incidents.json'
LOG_FILE = 'incident_log.txt'

# Initialize AI processor
ai_processor = AIProcessor()

def load_incidents():
    """Load incidents from JSON file"""
    if os.path.exists(INCIDENT_FILE):
        with open(INCIDENT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_incidents(data):
    """Save incidents to JSON file"""
    with open(INCIDENT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def log_action(action):
    """Log actions to file"""
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
        f.write(f"{action} at {timestamp}\n")

# Routes

@app.route('/')
def index():
    """Serve static HTML"""
    return send_file('index.html')

@app.route('/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents"""
    incidents = load_incidents()
    return jsonify(incidents)

@app.route('/incidents/analyze', methods=['POST'])
def analyze_incident():
    """AI Analysis endpoint"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()
    
    description = data.get('description', '').strip()
    
    if not description:
        return jsonify({'error': 'Description cannot be blank'}), 400
    
    analysis = ai_processor.analyze_incident(description)
    log_action(f"AI analysis performed for: {description}")
    
    return jsonify(analysis)

@app.route('/incidents', methods=['POST'])
def create_incident():
    """Create a new incident with AI analysis"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()
    
    description = data.get('description', '').strip()
    priority = data.get('priority', 'Medium')
    use_ai = data.get('use_ai', False)
    
    # Convert string boolean values
    if isinstance(use_ai, str):
        use_ai = use_ai.lower() in ['true', '1', 'yes']
    
    if not description:
        return jsonify({'error': 'Description cannot be blank'}), 400
    
    # Validate priority
    if priority not in ['Low', 'Medium', 'High', 'Critical']:
        priority = 'Medium'
    
    # Perform AI analysis if requested
    ai_analysis = None
    if use_ai:
        ai_analysis = ai_processor.analyze_incident(description)
        # Use AI suggested priority if user hasn't explicitly set one
        if not data.get('priority'):
            priority = ai_analysis.get('suggested_priority', 'Medium')
    
    new_incident = {
        'id': str(uuid.uuid4()),
        'description': description,
        'priority': priority,
        'resolved': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'resolved_at': None,
        'ai_analysis': ai_analysis
    }
    
    incidents = load_incidents()
    incidents.append(new_incident)
    save_incidents(incidents)
    
    # Log the action
    ai_suffix = ' (with AI analysis)' if use_ai else ''
    log_action(f"Incident created{ai_suffix}: {description}")
    
    return jsonify(new_incident), 201

@app.route('/reports/summary', methods=['GET'])
def generate_summary_report():
    """Generate AI summary report"""
    incidents = load_incidents()
    report = ai_processor.generate_summary_report(incidents)
    log_action("AI summary report generated")
    return jsonify(report)

@app.route('/insights', methods=['GET'])
def get_insights():
    """Get AI insights for dashboard"""
    incidents = load_incidents()
    
    # Recent trends
    last_week = []
    for incident in incidents:
        try:
            created_date = datetime.strptime(incident['created_at'], '%Y-%m-%d %H:%M:%S').date()
            if created_date >= date.today() - timedelta(days=7):
                last_week.append(incident)
        except (ValueError, KeyError):
            continue
    
    # High priority incidents
    high_priority = [i for i in incidents if i.get('priority') in ['High', 'Critical'] and not i.get('resolved', False)]
    
    # Category trends (from AI analysis)
    categories = {}
    for incident in incidents:
        if 'ai_analysis' in incident:
            category = incident['ai_analysis'].get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
    
    # Find most affected category
    most_affected = max(categories.items(), key=lambda x: x[1])[0] if categories else 'None'
    
    insights = {
        'alerts': {
            'high_priority_open': len(high_priority),
            'recent_spike': len(last_week) > 10,
            'categories_most_affected': most_affected
        },
        'trends': {
            'weekly_incidents': len(last_week),
            'category_breakdown': categories,
            'resolution_rate': round((sum(1 for i in incidents if i.get('resolved', False)) / len(incidents) * 100), 2) if incidents else 0
        }
    }
    
    return jsonify(insights)

@app.route('/incidents/<incident_id>', methods=['PUT'])
def update_incident(incident_id):
    """Update an incident's description"""
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()
    
    description = data.get('description', '').strip()
    
    incidents = load_incidents()
    incident = next((i for i in incidents if i['id'] == incident_id), None)
    
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    
    if not description:
        return jsonify({'error': 'Description cannot be blank'}), 400
    
    old_description = incident['description']
    incident['description'] = description
    
    # Re-run AI analysis if description changed significantly
    reanalyze = data.get('reanalyze')
    if isinstance(reanalyze, str):
        reanalyze = reanalyze.lower() in ['true', '1', 'yes']
    
    if reanalyze:
        incident['ai_analysis'] = ai_processor.analyze_incident(description)
        log_action(f"Incident updated with AI re-analysis:\nFrom: {old_description}\nTo: {description}")
    else:
        log_action(f"Incident updated:\nFrom: {old_description}\nTo: {description}")
    
    save_incidents(incidents)
    
    return jsonify(incident)

@app.route('/incidents/<incident_id>/resolve', methods=['PATCH'])
def resolve_incident(incident_id):
    """Resolve an incident"""
    incidents = load_incidents()
    incident = next((i for i in incidents if i['id'] == incident_id), None)
    
    if not incident:
        return jsonify({'error': 'Incident not found'}), 404
    
    incident['resolved'] = True
    incident['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_incidents(incidents)
    
    # Log the action
    log_action(f"Incident resolved: {incident['description']}")
    
    return jsonify(incident)

@app.route('/incidents/<incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """Delete an incident"""
    incidents = load_incidents()
    incident_index = next((i for i, inc in enumerate(incidents) if inc['id'] == incident_id), None)
    
    if incident_index is None:
        return jsonify({'error': 'Incident not found'}), 404
    
    deleted = incidents.pop(incident_index)
    save_incidents(incidents)
    
    # Log the action
    log_action(f"Incident deleted: {deleted['description']}")
    
    return jsonify(deleted)

@app.route('/logs', methods=['GET'])
def get_logs():
    """Get logs"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = [line.strip() for line in f.readlines()]
        return jsonify({'logs': logs})
    else:
        return jsonify({'logs': []})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4506, debug=True)