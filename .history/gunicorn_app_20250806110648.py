#!/usr/bin/env python3
"""
Modern360 Assessment - Gunicorn WSGI Application
This script handles both the main user application and admin application
"""

import os
import multiprocessing
from multiprocessing import Process
import time
import signal
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_main_app():
    """Run the main user application with Gunicorn"""
    from app import app
    
    # Gunicorn configuration for main app
    bind_host = os.environ.get('HOST', '0.0.0.0')
    main_port = int(os.environ.get('PORT', 5000))
    workers = int(os.environ.get('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
    
    # Import and configure Gunicorn
    from gunicorn.app.base import BaseApplication
    
    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()
        
        def load_config(self):
            config = {key: value for key, value in self.options.items()
                     if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)
        
        def load(self):
            return self.application
    
    options = {
        'bind': f'{bind_host}:{main_port}',
        'workers': workers,
        'worker_class': 'sync',
        'worker_connections': 1000,
        'timeout': 30,
        'keepalive': 2,
        'max_requests': 1000,
        'max_requests_jitter': 100,
        'preload_app': True,
        'accesslog': '-',
        'errorlog': '-',
        'capture_output': True,
        'enable_stdio_inheritance': True,
    }
    
    print(f"Starting main application on {bind_host}:{main_port} with {workers} workers")
    
    gunicorn_app = GunicornApp(app, options)
    gunicorn_app.run()

def run_admin_app():
    """Run the admin application with Gunicorn"""
    from admin_app import admin_app
    
    # Gunicorn configuration for admin app
    bind_host = os.environ.get('ADMIN_HOST', '0.0.0.0')
    admin_port = int(os.environ.get('ADMIN_PORT', 5001))
    admin_workers = int(os.environ.get('ADMIN_WEB_CONCURRENCY', 2))  # Fewer workers for admin
    
    # Import and configure Gunicorn
    from gunicorn.app.base import BaseApplication
    
    class GunicornAdminApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()
        
        def load_config(self):
            config = {key: value for key, value in self.options.items()
                     if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)
        
        def load(self):
            return self.application
    
    options = {
        'bind': f'{bind_host}:{admin_port}',
        'workers': admin_workers,
        'worker_class': 'sync',
        'worker_connections': 100,
        'timeout': 60,
        'keepalive': 2,
        'max_requests': 500,
        'max_requests_jitter': 50,
        'preload_app': True,
        'accesslog': '-',
        'errorlog': '-',
        'capture_output': True,
        'enable_stdio_inheritance': True,
    }
    
    print(f"Starting admin application on {bind_host}:{admin_port} with {admin_workers} workers")
    
    gunicorn_admin_app = GunicornAdminApp(admin_app, options)
    gunicorn_admin_app.run()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\nReceived signal {signum}. Shutting down applications...")
    sys.exit(0)

def main():
    """Main function to start both applications"""
    print("🚀 Starting Modern360 Assessment Platform...")
    print("=" * 60)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start both applications as separate processes
    processes = []
    
    try:
        # Start main application process
        main_process = Process(target=run_main_app, name="MainApp")
        main_process.start()
        processes.append(main_process)
        print("✅ Main application process started")
        
        # Small delay to avoid port conflicts
        time.sleep(2)
        
        # Start admin application process
        admin_process = Process(target=run_admin_app, name="AdminApp")
        admin_process.start()
        processes.append(admin_process)
        print("✅ Admin application process started")
        
        print("=" * 60)
        print("🌟 Modern360 Assessment Platform is running!")
        print(f"📱 Main Application: http://localhost:{os.environ.get('PORT', 5000)}")
        print(f"🔧 Admin Dashboard: http://localhost:{os.environ.get('ADMIN_PORT', 5001)}")
        print("=" * 60)
        print("Press Ctrl+C to stop all applications")
        
        # Wait for all processes
        for process in processes:
            process.join()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down applications...")
        
    except Exception as e:
        print(f"❌ Error starting applications: {e}")
        
    finally:
        # Terminate all processes
        for process in processes:
            if process.is_alive():
                print(f"🔄 Terminating {process.name}...")
                process.terminate()
                process.join(timeout=5)
                
                if process.is_alive():
                    print(f"⚠️  Force killing {process.name}...")
                    process.kill()
                    process.join()
        
        print("✅ All applications stopped")

# WSGI entry points for deployment platforms
from app import app as main_app
from admin_app import admin_app

# Default app for gunicorn (main application)
app = main_app

# Alternative: admin app for admin deployment
# app = admin_app

if __name__ == '__main__':
    main()
