#!/usr/bin/env python3
"""
Railway startup script that properly handles the PORT environment variable
"""
import os
import subprocess
import sys

def main():
    print("🔧 Railway startup script starting...")
    print(f"🐍 Python executable: {sys.executable}")
    print(f"🐍 Python version: {sys.version}")
    
    # Debug: Print environment variables
    print("=== ENVIRONMENT VARIABLES DEBUG ===")
    print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
    print(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'NOT SET')}")
    print(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
    print(f"SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}")
    print(f"CORS_ALLOWED_ORIGINS: {os.environ.get('CORS_ALLOWED_ORIGINS', 'NOT SET')}")
    print("===================================")
    
    # Ensure we're in the right directory
    print(f"📍 Current working directory: {os.getcwd()}")
    print(f"📁 Directory contents: {os.listdir('.')}")
    
    # Change to the backend directory
    backend_dir = '/app/backend'
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
        print(f"📁 Changed to backend directory: {os.getcwd()}")
    else:
        print(f"❌ Backend directory not found: {backend_dir}")
        # Try relative path
        if os.path.exists('backend'):
            os.chdir('backend')
            print(f"📁 Changed to relative backend directory: {os.getcwd()}")
        else:
            print("❌ No backend directory found, staying in current directory")
    
    print(f"📁 Backend directory contents: {os.listdir('.')}")
    
    # Get port from environment variable, default to 8000
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 Starting Django on port {port}")
    
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
