#!/usr/bin/env python3
"""
Modern360 Assessment - Universal Startup Script
Handles development, production, and deployment scenarios
"""

import os
import sys
import argparse
import subprocess
import multiprocessing
from multiprocessing import Process
import time
import signal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def run_development():
    """Run applications in development mode"""
    from multiprocessing import Process
    
    def run_main_dev():
        """Run main app in development"""
        from app import app
        port = int(os.environ.get('PORT', 5000))
        print(f"🔥 Starting main app (development) on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    
    def run_admin_dev():
        """Run admin app in development"""
        from admin_app import admin_app
        port = int(os.environ.get('ADMIN_PORT', 5001))
        print(f"🔧 Starting admin app (development) on port {port}")
        admin_app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    
    processes = []
    
    try:
        # Start main app
        main_process = Process(target=run_main_dev, name="MainApp-Dev")
        main_process.start()
        processes.append(main_process)
        
        time.sleep(2)
        
        # Start admin app
        admin_process = Process(target=run_admin_dev, name="AdminApp-Dev")
        admin_process.start()
        processes.append(admin_process)
        
        print("🌟 Development servers running!")
        print(f"📱 Main App: http://localhost:{os.environ.get('PORT', 5000)}")
        print(f"🔧 Admin App: http://localhost:{os.environ.get('ADMIN_PORT', 5001)}")
        print("Press Ctrl+C to stop")
        
        # Wait for processes
        for process in processes:
            process.join()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()

def run_production():
    """Run applications with Gunicorn for production"""
    try:
        import gunicorn
    except ImportError:
        print("❌ Gunicorn not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn"])
    
    from gunicorn_app import main as run_gunicorn
    run_gunicorn()

def run_main_only():
    """Run only the main application"""
    from app import app
    
    # Auto-detect production environment for render.com and other platforms
    is_production = (
        os.environ.get('DEPLOYMENT_ENV') == 'production' or
        os.environ.get('RENDER') or  # Render.com sets this
        os.environ.get('HEROKU_APP_NAME') or  # Heroku
        os.environ.get('RAILWAY_ENVIRONMENT')  # Railway
    )
    
    if is_production:
        # Use Gunicorn for production
        port = int(os.environ.get('PORT', 5000))
        workers = int(os.environ.get('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
        
        cmd = [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', str(workers),
            '--timeout', '30',
            '--keep-alive', '2',
            '--max-requests', '1000',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'wsgi:app'
        ]
        
        print(f"🚀 Starting main app with Gunicorn on port {port} (Production)")
        subprocess.run(cmd)
    else:
        # Development mode
        port = int(os.environ.get('PORT', 5000))
        print(f"🔥 Starting main app (development) on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)

def run_admin_only():
    """Run only the admin application"""
    from admin_app import admin_app
    
    if os.environ.get('DEPLOYMENT_ENV') == 'production':
        # Use Gunicorn for production
        port = int(os.environ.get('ADMIN_PORT', 5001))
        workers = int(os.environ.get('ADMIN_WEB_CONCURRENCY', 2))
        
        cmd = [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', str(workers),
            '--timeout', '60',
            '--keep-alive', '2',
            '--max-requests', '500',
            '--access-logfile', '-',
            '--error-logfile', '-',
            'admin_app:admin_app'
        ]
        
        print(f"🔧 Starting admin app with Gunicorn on port {port}")
        subprocess.run(cmd)
    else:
        # Development mode
        port = int(os.environ.get('ADMIN_PORT', 5001))
        print(f"🔧 Starting admin app (development) on port {port}")
        admin_app.run(host='0.0.0.0', port=port, debug=True)

def setup_database():
    """Initialize database and ensure template questions"""
    print("🗄️  Setting up database...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
            
            # Ensure template questions are loaded
            print("📝 Ensuring template questions are loaded...")
            from ensure_template_questions import add_predefined_questions
            add_predefined_questions()
            print("✅ Template questions verified")
            
        print("✅ Database setup complete")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='Modern360 Assessment Platform Startup Script')
    parser.add_argument('--mode', choices=['dev', 'prod', 'main', 'admin'], 
                       default='dev', help='Application mode')
    parser.add_argument('--install', action='store_true', help='Install requirements first')
    parser.add_argument('--setup-db', action='store_true', help='Setup database')
    
    args = parser.parse_args()
    
    print("🌟 Modern360 Assessment Platform")
    print("=" * 50)
    
    if args.install:
        install_requirements()
    
    if args.setup_db:
        setup_database()
    
    # Always run the specified mode (don't exit after setup)
    if args.mode == 'dev':
        print("🔥 Starting in DEVELOPMENT mode")
        run_development()
    elif args.mode == 'prod':
        print("🚀 Starting in PRODUCTION mode")
        run_production()
    elif args.mode == 'main':
        print("📱 Starting MAIN application only")
        run_main_only()
    elif args.mode == 'admin':
        print("🔧 Starting ADMIN application only")
        run_admin_only()

if __name__ == '__main__':
    main()
