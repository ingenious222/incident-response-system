import re
import json
import requests
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

class AIProcessor:
    """AI-enhanced incident analysis and processing module"""
    
    def __init__(self):
        self.ai_config = {
            'api_url': os.getenv('AI_API_URL', 'https://openrouter.ai/api/v1/chat/completions'),
            'model': os.getenv('AI_MODEL', 'x-ai/grok-3.5'),
            'api_key': os.getenv('AI_API_KEY', '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')
        }
    
    def analyze_incident(self, description: str) -> Dict[str, Any]:
        """Analyze incident and provide AI-enhanced insights"""
        try:
            # Priority assessment based on keywords and context
            priority = self._assess_priority(description)
            
            # Generate suggested response steps
            response_steps = self._generate_response_steps(description)
            
            # Categorize the incident
            category = self._categorize_incident(description)
            
            # Risk assessment
            risk_level = self._assess_risk(description)
            
            return {
                'suggested_priority': priority,
                'category': category,
                'risk_level': risk_level,
                'response_steps': response_steps,
                'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            return {
                'suggested_priority': 'Medium',
                'category': 'Unknown',
                'risk_level': 'Medium',
                'response_steps': ['Manual assessment required'],
                'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': str(e)
            }
    
    def _assess_priority(self, description: str) -> str:
        """Enhanced priority assessment using keyword analysis"""
        critical_keywords = ['ransomware', 'data breach', 'security breach', 'hack', 'malware', 'virus', 'ddos', 'attack', 'critical system down', 'outage']
        high_keywords = ['server down', 'network issue', 'database error', 'login problem', 'payment system', 'customer data']
        medium_keywords = ['slow performance', 'minor bug', 'update needed', 'configuration']
        
        desc_lower = description.lower()
        
        if any(keyword in desc_lower for keyword in critical_keywords):
            return 'Critical'
        elif any(keyword in desc_lower for keyword in high_keywords):
            return 'High'
        elif any(keyword in desc_lower for keyword in medium_keywords):
            return 'Medium'
        
        return 'Low'
    
    def _categorize_incident(self, description: str) -> str:
        """Simple categorization based on keywords"""
        categories = {
            'Security': ['security', 'breach', 'hack', 'malware', 'virus', 'ransomware', 'attack'],
            'Infrastructure': ['server', 'network', 'hardware', 'outage', 'connectivity'],
            'Application': ['bug', 'error', 'crash', 'performance', 'slow'],
            'User Access': ['login', 'password', 'account', 'access', 'authentication'],
            'Data': ['database', 'data', 'backup', 'corruption']
        }
        
        desc_lower = description.lower()
        for category, keywords in categories.items():
            if any(keyword in desc_lower for keyword in keywords):
                return category
        
        return 'General'
    
    def _assess_risk(self, description: str) -> str:
        """Risk assessment based on potential impact"""
        desc_lower = description.lower()
        
        if re.search(r'critical|breach|attack|ransomware|data loss', desc_lower):
            return 'High'
        elif re.search(r'server|network|database|payment', desc_lower):
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_response_steps(self, description: str) -> List[str]:
        """Generate contextual response steps"""
        desc_lower = description.lower()
        
        # Security incident steps
        if re.search(r'security|breach|hack|malware|ransomware', desc_lower):
            return [
                "1. Isolate affected systems immediately",
                "2. Preserve forensic evidence", 
                "3. Notify security team and management",
                "4. Document all observed indicators",
                "5. Begin containment procedures",
                "6. Assess scope of compromise"
            ]
        # Infrastructure issues
        elif re.search(r'server|network|outage|connectivity', desc_lower):
            return [
                "1. Verify system status and availability",
                "2. Check network connectivity and routing",
                "3. Review system logs for errors",
                "4. Test failover systems if available",
                "5. Notify affected users if necessary",
                "6. Implement workaround if possible"
            ]
        # Application issues
        elif re.search(r'bug|error|crash|performance', desc_lower):
            return [
                "1. Reproduce the issue if possible",
                "2. Check application logs for errors",
                "3. Verify recent deployments or changes",
                "4. Test in staging environment",
                "5. Implement temporary fix if available",
                "6. Plan permanent solution"
            ]
        else:
            return [
                "1. Gather detailed information about the issue",
                "2. Assess impact and affected systems",
                "3. Determine urgency and priority",
                "4. Assign to appropriate team member",
                "5. Document troubleshooting steps",
                "6. Monitor for resolution"
            ]
    
    def generate_summary_report(self, incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive summary report from incidents"""
        total = len(incidents)
        resolved = sum(1 for i in incidents if i.get('resolved', False))
        open_incidents = total - resolved
        
        # Priority breakdown
        priority_breakdown = {}
        for incident in incidents:
            priority = incident.get('priority', 'Medium')
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
        
        # Category breakdown (if available)
        category_breakdown = {}
        for incident in incidents:
            if 'ai_analysis' in incident:
                category = incident['ai_analysis'].get('category', 'Unknown')
                category_breakdown[category] = category_breakdown.get(category, 0) + 1
        
        # Recent trends
        recent_incidents = []
        for incident in incidents:
            try:
                created_date = datetime.strptime(incident['created_at'], '%Y-%m-%d %H:%M:%S').date()
                if created_date >= date.today() - timedelta(days=7):
                    recent_incidents.append(incident)
            except (ValueError, KeyError):
                continue
        
        return {
            'summary': {
                'total_incidents': total,
                'resolved_incidents': resolved,
                'open_incidents': open_incidents,
                'resolution_rate': round((resolved / total * 100), 2) if total > 0 else 0
            },
            'priority_breakdown': priority_breakdown,
            'category_breakdown': category_breakdown,
            'recent_activity': {
                'incidents_last_7_days': len(recent_incidents),
                'average_per_day': round(len(recent_incidents) / 7.0, 2)
            },
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }