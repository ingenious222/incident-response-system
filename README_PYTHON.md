# AI-Enhanced Incident Response System (Python Version)

A comprehensive incident management system with AI-powered analysis, converted from Ruby to Python while maintaining all original features.

## Features

### 🚀 Core Functionality
- **Incident Management**: Create, update, resolve, and delete incidents
- **Priority System**: Automatic and manual priority assignment (Low, Medium, High, Critical)
- **Status Tracking**: Track incident resolution status and timestamps
- **Audit Logging**: Complete action logging with timestamps

### 🤖 AI Enhancement
- **Smart Priority Assessment**: AI analyzes incident descriptions to suggest appropriate priority levels
- **Automatic Categorization**: Classifies incidents into categories (Security, Infrastructure, Application, User Access, Data, General)
- **Risk Assessment**: Evaluates potential impact and assigns risk levels
- **Response Recommendations**: Provides contextual step-by-step response guidance
- **Trend Analysis**: Generates insights and summary reports

### 💻 Multiple Interfaces
- **Web Interface**: Full-featured Flask web application with modern UI
- **Command Line Interface**: Interactive CLI with colorized output
- **REST API**: Complete API for integration with other systems

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd e:\proj\secod
   ```

2. **Create and activate virtual environment** (if not already done)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
Run the startup script to choose your preferred interface:

**Windows:**
```bash
start.bat
```

**Cross-platform:**
```bash
python run.py
```

### Web Interface
Start the Flask web server:
```bash
python app.py
```
Then visit: http://127.0.0.1:4506

### Command Line Interface
Start the interactive CLI:
```bash
python project.py
```

## API Endpoints

### Incidents
- `GET /incidents` - Retrieve all incidents
- `POST /incidents` - Create new incident
- `PUT /incidents/<id>` - Update incident
- `PATCH /incidents/<id>/resolve` - Resolve incident
- `DELETE /incidents/<id>` - Delete incident

### AI Features
- `POST /incidents/analyze` - Analyze incident description with AI
- `GET /reports/summary` - Generate AI summary report
- `GET /insights` - Get dashboard insights

### Utilities
- `GET /logs` - Retrieve action logs
- `GET /` - Serve web interface

## Project Structure

```
├── app.py              # Flask web application
├── project.py          # Command line interface
├── ai_processor.py     # AI analysis module
├── requirements.txt    # Python dependencies
├── start.bat          # Windows startup script
├── run.py             # Cross-platform startup script
├── index.html         # Web interface (from original)
├── incidents.json     # Data storage
└── incident_log.txt   # Action logs
```

## AI Configuration

The system supports configurable AI services through environment variables:

```bash
export AI_API_URL="https://openrouter.ai/api/v1/chat/completions"
export AI_MODEL="x-ai/grok-3.5"
export AI_API_KEY="your-api-key"
```

## Features Comparison: Ruby vs Python

| Feature | Ruby (Original) | Python (Converted) | Status |
|---------|----------------|-------------------|---------|
| Web Server | Sinatra | Flask | ✅ Complete |
| CLI Interface | Colorize gem | Colorama | ✅ Complete |
| AI Processing | Built-in module | Separate module | ✅ Enhanced |
| Data Storage | JSON files | JSON files | ✅ Compatible |
| Logging | File-based | File-based | ✅ Compatible |
| API Endpoints | All routes | All routes | ✅ Complete |
| Priority System | 4 levels | 4 levels | ✅ Complete |
| Incident CRUD | Full support | Full support | ✅ Complete |
| AI Analysis | Basic | Enhanced | ✅ Improved |
| Report Generation | Summary reports | Summary + insights | ✅ Enhanced |

## Dependencies

- **Flask 3.0.0**: Web framework
- **colorama 0.4.6**: Cross-platform colored terminal output
- **requests 2.31.0**: HTTP library for AI API calls
- **Werkzeug 3.0.1**: WSGI utility library

## Data Migration

The Python version is fully compatible with existing Ruby data files:
- `incidents.json` - Same format, seamless migration
- `incident_log.txt` - Compatible logging format
- All existing data will work without modification

## Development

### Running Tests
```bash
python -c "from ai_processor import AIProcessor; ai = AIProcessor(); print('AI Test:', ai.analyze_incident('test'))"
```

### Adding New Features
1. **Web features**: Modify `app.py` and add routes
2. **CLI features**: Extend `project.py` menu system
3. **AI features**: Enhance `ai_processor.py` methods

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure virtual environment is activated
2. **Port conflicts**: Change port in `app.py` if 4506 is occupied
3. **AI analysis errors**: Check AI_API_KEY configuration

### Logs
Check `incident_log.txt` for detailed action history and error tracking.

## License

This project maintains the same licensing as the original Ruby version.

## Contributing

1. Follow the established code structure
2. Maintain compatibility with existing data formats
3. Add appropriate logging for new features
4. Test both web and CLI interfaces