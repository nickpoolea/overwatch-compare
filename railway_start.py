#!/usr/bin/env python3
"""
Railway startup script that properly handles the PORT environment variable
"""
import os
import subprocess
import sys

def main():
    # Get port from environment variable, default to 8000
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 Starting Django on port {port}")
    
    # Run migrations
    print("📋 Running migrations...")
    subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
    
    # Collect static files
    print("📁 Collecting static files...")
    subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
    
    # Start server
    print(f"🌐 Starting server on 0.0.0.0:{port}")
    subprocess.run([sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'])

if __name__ == '__main__':
    main()
