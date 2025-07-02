#!/usr/bin/env python3
"""
Overwatch Comparison App Launcher
Starts both Django backend and React frontend with a single command
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class AppLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        
    def check_dependencies(self):
        """Check if required directories and files exist"""
        print("🔍 Checking dependencies...")
        
        if not self.backend_dir.exists():
            print(f"❌ Backend directory not found: {self.backend_dir}")
            return False
            
        if not (self.backend_dir / "manage.py").exists():
            print(f"❌ Django manage.py not found in: {self.backend_dir}")
            return False
            
        if not self.frontend_dir.exists():
            print(f"❌ Frontend directory not found: {self.frontend_dir}")
            return False
            
        if not (self.frontend_dir / "package.json").exists():
            print(f"❌ React package.json not found in: {self.frontend_dir}")
            return False
            
        print("✅ All dependencies found!")
        return True
    
    def start_backend(self):
        """Start Django backend server"""
        print("🚀 Starting Django backend...")
        try:
            os.chdir(self.backend_dir)
            self.backend_process = subprocess.Popen(
                [sys.executable, "manage.py", "runserver", "8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            print("✅ Django backend started on http://localhost:8000")
            return True
        except Exception as e:
            print(f"❌ Failed to start Django backend: {e}")
            return False
    
    def start_frontend(self):
        """Start React frontend server"""
        print("🚀 Starting React frontend...")
        try:
            os.chdir(self.frontend_dir)
            
            # Check if node_modules exists
            if not (self.frontend_dir / "node_modules").exists():
                print("📦 Installing npm dependencies...")
                install_process = subprocess.run(
                    ["npm", "install"],
                    capture_output=True,
                    text=True
                )
                if install_process.returncode != 0:
                    print(f"❌ npm install failed: {install_process.stderr}")
                    return False
                print("✅ npm dependencies installed!")
            
            # Start React dev server
            self.frontend_process = subprocess.Popen(
                ["npm", "start"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            print("✅ React frontend started on http://localhost:3000")
            return True
        except Exception as e:
            print(f"❌ Failed to start React frontend: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor backend and frontend processes"""
        def monitor_backend():
            if self.backend_process:
                for line in iter(self.backend_process.stdout.readline, ''):
                    if line.strip():
                        print(f"[BACKEND] {line.strip()}")
                        
        def monitor_frontend():
            if self.frontend_process:
                for line in iter(self.frontend_process.stdout.readline, ''):
                    if line.strip() and "webpack" not in line.lower():
                        print(f"[FRONTEND] {line.strip()}")
        
        # Start monitoring threads
        if self.backend_process:
            backend_thread = threading.Thread(target=monitor_backend, daemon=True)
            backend_thread.start()
            
        if self.frontend_process:
            frontend_thread = threading.Thread(target=monitor_frontend, daemon=True)
            frontend_thread.start()
    
    def cleanup(self):
        """Clean up processes on exit"""
        print("\n🛑 Shutting down servers...")
        
        if self.backend_process:
            try:
                if os.name == 'nt':
                    # Windows
                    self.backend_process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    # Unix/Linux/Mac
                    self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Django backend stopped")
            except:
                self.backend_process.kill()
                print("🔥 Django backend force killed")
        
        if self.frontend_process:
            try:
                if os.name == 'nt':
                    # Windows
                    self.frontend_process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    # Unix/Linux/Mac
                    self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ React frontend stopped")
            except:
                self.frontend_process.kill()
                print("🔥 React frontend force killed")
    
    def run(self):
        """Main run method"""
        print("🎮 Overwatch Comparison App Launcher")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            sys.exit(1)
        
        # Start servers
        if not self.start_backend():
            sys.exit(1)
        
        # Wait a bit for backend to start
        print("⏳ Waiting for backend to initialize...")
        time.sleep(3)
        
        if not self.start_frontend():
            self.cleanup()
            sys.exit(1)
        
        # Monitor processes
        self.monitor_processes()
        
        print("\n" + "=" * 50)
        print("🎉 Both servers are running!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend:  http://localhost:8000")
        print("📊 API:      http://localhost:8000/api/")
        print("=" * 50)
        print("Press Ctrl+C to stop both servers")
        
        try:
            # Keep the main thread alive
            while True:
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died!")
                    break
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend process died!")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Received shutdown signal...")
        finally:
            self.cleanup()

def main():
    launcher = AppLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
