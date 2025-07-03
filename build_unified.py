#!/usr/bin/env python3
"""
Single-platform deployment script
Builds React frontend and serves everything through Django
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    frontend_dir = base_dir / "frontend"
    backend_dir = base_dir / "backend"
    
    print("🚀 Building Overwatch App for Single-Platform Deployment")
    print("=" * 60)
    
    # Build React frontend
    print("📦 Building React frontend...")
    os.chdir(frontend_dir)
    
    # Install npm dependencies
    result = subprocess.run(["npm", "install"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ npm install failed: {result.stderr}")
        sys.exit(1)
    
    # Build React app
    result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ React build failed: {result.stderr}")
        sys.exit(1)
    
    print("✅ React frontend built successfully!")
    
    # Setup Django backend
    print("⚙️  Setting up Django backend...")
    os.chdir(backend_dir)
    
    # Install Python dependencies
    python_cmd = "python3" if sys.platform != "win32" else "python"
    result = subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ pip install failed: {result.stderr}")
        sys.exit(1)
    
    # Run migrations
    result = subprocess.run([python_cmd, "manage.py", "migrate"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Migration warning: {result.stderr}")
    
    # Collect static files
    result = subprocess.run([python_cmd, "manage.py", "collectstatic", "--noinput"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Static files warning: {result.stderr}")
    
    print("✅ Django backend configured!")
    
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETE!")
    print("📁 React app built to: frontend/build/")
    print("🔧 Django configured to serve frontend")
    print("=" * 60)
    
    # Ask if user wants to start the server
    response = input("\n🚀 Start the unified server now? (y/n): ").lower()
    if response == 'y':
        print("\n🌐 Starting server on http://localhost:8000")
        print("Press Ctrl+C to stop")
        try:
            subprocess.run([python_cmd, "manage.py", "runserver"])
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")
    else:
        print("\n📝 To start the server later, run:")
        print(f"   cd {backend_dir}")
        print("   python manage.py runserver")
        print("\n🌐 Your app will be available at: http://localhost:8000")

if __name__ == "__main__":
    main()
