#!/usr/bin/env python3
"""
Railway startup script that properly handles the PORT environment variable
"""
import os
import subprocess
import sys

def main():
    print("� Starting Overwatch Comparison App...")
    
    # Change to the backend directory
    backend_dir = '/app/backend'
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
        print(f"📁 Changed to backend directory: {os.getcwd()}")
    elif os.path.exists('backend'):
        os.chdir('backend')
        print(f"📁 Changed to relative backend directory: {os.getcwd()}")
    
    # Get port from environment variable, default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Run migrations
    print("📋 Running migrations...")
    result = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Migration failed: {result.stderr}")
    else:
        print("✅ Migrations completed successfully")
    
    # Collect static files
    print("📁 Collecting static files...")
    result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Static collection failed: {result.stderr}")
    else:
        print("✅ Static files collected successfully")
    
    # Start server
    print(f"🌐 Starting server on 0.0.0.0:{port}")
    subprocess.run([sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'])

if __name__ == '__main__':
    main()
