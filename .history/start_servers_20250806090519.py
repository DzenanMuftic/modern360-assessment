#!/usr/bin/env python3
"""
Modern360 Dual Server Launcher
Starts both the main application and admin application on different ports
"""

import subprocess
import sys
import time
import os
from threading import Thread

def run_main_app():
    """Run the main application on port 5000"""
    print("🚀 Starting Main Application on http://localhost:5000")
    subprocess.run([sys.executable, "app.py"], cwd=os.getcwd())

def run_admin_app():
    """Run the admin application on port 5001"""
    print("🔐 Starting Admin Application on http://localhost:5001")
    subprocess.run([sys.executable, "admin_app.py"], cwd=os.getcwd())

def main():
    print("=" * 60)
    print("MODERN360 ASSESSMENT PLATFORM - DUAL SERVER LAUNCHER")
    print("=" * 60)
    print()
    print("🌟 Starting Modern360 Assessment Platform...")
    print()
    print("📊 Main Application:")
    print("   URL: http://localhost:5000")
    print("   Purpose: User assessments, responses, dashboard")
    print()
    print("🔧 Admin Dashboard:")
    print("   URL: http://localhost:5001")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Purpose: User management, assessment creation, reports")
    print()
    print("=" * 60)
    print()
    
    # Start both applications in separate threads
    main_thread = Thread(target=run_main_app, daemon=True)
    admin_thread = Thread(target=run_admin_app, daemon=True)
    
    main_thread.start()
    time.sleep(2)  # Small delay to avoid port conflicts
    admin_thread.start()
    
    try:
        print("✅ Both servers are starting...")
        print("   Main App: http://localhost:5000")
        print("   Admin App: http://localhost:5001")
        print()
        print("Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("Goodbye! 👋")
        sys.exit(0)

if __name__ == "__main__":
    main()
