import json
import os
import uuid
from datetime import datetime
from colorama import Fore, Style, init
from ai_processor import AIProcessor

# Initialize colorama for Windows support
init()

class IncidentManager:
    """Command-line incident management system"""
    
    def __init__(self):
        self.INCIDENT_FILE = 'incidents.json'
        self.LOG_FILE = 'incident_log.txt'
        self.incidents = self.load_incidents()
        self.ai_processor = AIProcessor()
    
    def load_incidents(self):
        """Load incidents from JSON file"""
        if os.path.exists(self.INCIDENT_FILE):
            with open(self.INCIDENT_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_incidents(self):
        """Save incidents to JSON file"""
        with open(self.INCIDENT_FILE, 'w') as f:
            json.dump(self.incidents, f, indent=2)
    
    def log_action(self, action):
        """Log actions to file"""
        with open(self.LOG_FILE, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {action}\n")
    
    def create_incident(self):
        """Create a new incident"""
        description = input("Enter incident description: ").strip()
        if not description:
            print(f"{Fore.RED}Description cannot be blank.{Style.RESET_ALL}")
            return
        
        priority = input("Enter priority [Low/Medium/High/Critical]: ").strip().capitalize()
        if priority not in ['Low', 'Medium', 'High', 'Critical']:
            priority = 'Medium'
        
        # Ask if user wants AI analysis
        use_ai = input("Use AI analysis? [y/N]: ").strip().lower() in ['y', 'yes']
        
        # Perform AI analysis if requested
        ai_analysis = None
        if use_ai:
            print("Performing AI analysis...")
            ai_analysis = self.ai_processor.analyze_incident(description)
            print(f"{Fore.CYAN}AI Suggested Priority: {ai_analysis.get('suggested_priority', 'Medium')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Category: {ai_analysis.get('category', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Risk Level: {ai_analysis.get('risk_level', 'Medium')}{Style.RESET_ALL}")
            
            # Ask if user wants to use AI suggested priority
            use_ai_priority = input(f"Use AI suggested priority ({ai_analysis.get('suggested_priority', 'Medium')})? [y/N]: ").strip().lower()
            if use_ai_priority in ['y', 'yes']:
                priority = ai_analysis.get('suggested_priority', 'Medium')
        
        incident = {
            'id': str(uuid.uuid4()),
            'description': description,
            'priority': priority,
            'resolved': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'resolved_at': None,
            'ai_analysis': ai_analysis
        }
        
        self.incidents.append(incident)
        self.save_incidents()
        
        ai_suffix = ' (with AI analysis)' if use_ai else ''
        self.log_action(f"Incident created{ai_suffix}: {description}")
        print(f"{Fore.GREEN}Incident created successfully!{Style.RESET_ALL}")
        
        # Show AI response steps if available
        if ai_analysis and 'response_steps' in ai_analysis:
            print(f"\n{Fore.YELLOW}AI Suggested Response Steps:{Style.RESET_ALL}")
            for step in ai_analysis['response_steps']:
                print(f"  {step}")
    
    def update_incident(self):
        """Update an existing incident"""
        self.view_incidents()
        if not self.incidents:
            return
        
        incident_id = input("Enter ID of incident to update: ").strip()
        
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        if not incident:
            print(f"{Fore.RED}Incident not found!{Style.RESET_ALL}")
            return
        
        new_desc = input("Enter new description: ").strip()
        if new_desc:
            old_desc = incident['description']
            incident['description'] = new_desc
            
            # Ask if user wants to re-run AI analysis
            if incident.get('ai_analysis'):
                reanalyze = input("Re-run AI analysis with new description? [y/N]: ").strip().lower()
                if reanalyze in ['y', 'yes']:
                    print("Re-analyzing with AI...")
                    incident['ai_analysis'] = self.ai_processor.analyze_incident(new_desc)
                    print(f"{Fore.CYAN}Updated AI Analysis:{Style.RESET_ALL}")
                    print(f"  Priority: {incident['ai_analysis'].get('suggested_priority', 'Medium')}")
                    print(f"  Category: {incident['ai_analysis'].get('category', 'Unknown')}")
                    print(f"  Risk Level: {incident['ai_analysis'].get('risk_level', 'Medium')}")
            
            self.save_incidents()
            self.log_action(f"Incident updated:\nFrom: {old_desc}\nTo: {new_desc}")
            print(f"{Fore.GREEN}Incident updated successfully!{Style.RESET_ALL}")
    
    def resolve_incident(self):
        """Resolve an incident"""
        self.view_incidents()
        if not self.incidents:
            return
        
        incident_id = input("Enter ID of incident to resolve: ").strip()
        
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        if not incident:
            print(f"{Fore.RED}Incident not found!{Style.RESET_ALL}")
            return
        
        incident['resolved'] = True
        incident['resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_incidents()
        self.log_action(f"Incident resolved: {incident['description']}")
        print(f"{Fore.GREEN}Incident resolved!{Style.RESET_ALL}")
    
    def delete_incident(self):
        """Delete an incident"""
        self.view_incidents()
        if not self.incidents:
            return
        
        incident_id = input("Enter ID of incident to delete: ").strip()
        
        incident_index = next((i for i, inc in enumerate(self.incidents) if inc['id'] == incident_id), None)
        if incident_index is None:
            print(f"{Fore.RED}Incident not found!{Style.RESET_ALL}")
            return
        
        deleted = self.incidents.pop(incident_index)
        self.save_incidents()
        self.log_action(f"Incident deleted: {deleted['description']}")
        print(f"{Fore.GREEN}Incident deleted!{Style.RESET_ALL}")
    
    def view_incidents(self):
        """View all incidents"""
        self.incidents = self.load_incidents()
        if not self.incidents:
            print("No incidents found.")
            return
        
        print("\nList of Incidents:")
        for incident in self.incidents:
            # Color based on priority
            if incident['priority'] == 'Critical':
                color = Fore.RED + Style.BRIGHT
            elif incident['priority'] == 'High':
                color = Fore.RED
            elif incident['priority'] == 'Medium':
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
            
            status = "[Resolved]" if incident['resolved'] else "[Open]"
            resolved_at = incident.get('resolved_at', '-')
            
            print(f"{color}{status} ID: {incident['id']} | {incident['description']} [{incident['priority']}]{Style.RESET_ALL}")
            
            # Show AI analysis summary if available
            if incident.get('ai_analysis'):
                ai_info = incident['ai_analysis']
                print(f"  {Fore.CYAN}AI: {ai_info.get('category', 'Unknown')} | Risk: {ai_info.get('risk_level', 'Medium')}{Style.RESET_ALL}")
    
    def view_ai_summary(self):
        """View AI-generated summary report"""
        if not self.incidents:
            print("No incidents found for summary.")
            return
        
        print("Generating AI summary report...")
        report = self.ai_processor.generate_summary_report(self.incidents)
        
        print(f"\n{Fore.CYAN}=== AI INCIDENT SUMMARY REPORT ==={Style.RESET_ALL}")
        print(f"Generated at: {report['generated_at']}")
        
        summary = report['summary']
        print(f"\n{Fore.YELLOW}Overview:{Style.RESET_ALL}")
        print(f"  Total Incidents: {summary['total_incidents']}")
        print(f"  Resolved: {summary['resolved_incidents']}")
        print(f"  Open: {summary['open_incidents']}")
        print(f"  Resolution Rate: {summary['resolution_rate']}%")
        
        if report['priority_breakdown']:
            print(f"\n{Fore.YELLOW}Priority Breakdown:{Style.RESET_ALL}")
            for priority, count in report['priority_breakdown'].items():
                print(f"  {priority}: {count}")
        
        if report['category_breakdown']:
            print(f"\n{Fore.YELLOW}Category Breakdown:{Style.RESET_ALL}")
            for category, count in report['category_breakdown'].items():
                print(f"  {category}: {count}")
        
        recent = report['recent_activity']
        print(f"\n{Fore.YELLOW}Recent Activity (Last 7 days):{Style.RESET_ALL}")
        print(f"  Incidents: {recent['incidents_last_7_days']}")
        print(f"  Average per day: {recent['average_per_day']}")

def main():
    """Main program loop"""
    manager = IncidentManager()
    
    while True:
        print("\n" + "=" * 80)
        print("*           AI-Enhanced Incident Response Automation         *".center(80))
        print("=" * 80)
        print("\nMain Menu:")
        print("1. View Incidents")
        print("2. Create Incident")
        print("3. Update Incident")
        print("4. Resolve Incident")
        print("5. Delete Incident")
        print("6. AI Summary Report")
        print("7. Exit")
        
        try:
            choice = int(input("\nEnter your choice: ").strip())
        except ValueError:
            print(f"{Fore.RED}Invalid choice! Please enter a number.{Style.RESET_ALL}")
            continue
        
        if choice == 1:
            manager.view_incidents()
        elif choice == 2:
            manager.create_incident()
        elif choice == 3:
            manager.update_incident()
        elif choice == 4:
            manager.resolve_incident()
        elif choice == 5:
            manager.delete_incident()
        elif choice == 6:
            manager.view_ai_summary()
        elif choice == 7:
            print("Exiting... Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()