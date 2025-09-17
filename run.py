#!/usr/bin/env python3
"""
Run script for AI-Enhanced Incident Response System (Python Version)
Provides options to start either the web server or CLI interface
"""

import sys
import subprocess
import os

def main():
    print("AI-Enhanced Incident Response System (Python Version)")
    print("=" * 55)
    print("\nChoose an option:")
    print("1. Start Web Server (Flask)")
    print("2. Start Command Line Interface") 
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nStarting Flask web server on http://127.0.0.1:4506")
                print("Press Ctrl+C to stop the server")
                print("-" * 40)
                subprocess.run([sys.executable, "app.py"])
                break
                
            elif choice == "2":
                print("\nStarting Command Line Interface")
                print("-" * 30)
                subprocess.run([sys.executable, "project.py"])
                break
                
            elif choice == "3":
                print("Goodbye!")
                sys.exit(0)
                
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()