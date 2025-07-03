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
        
        # Check Python executable
        try:
            result = subprocess.run([self.get_python_executable(), "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Python executable not found")
                return False
            print(f"✅ Python found: {result.stdout.strip()}")
        except FileNotFoundError:
            print("❌ Python executable not found")
            return False
            
        print("✅ All dependencies found!")
        return True
    
    def check_ports(self):
        """Check if required ports are available"""
        import socket
        
        def is_port_available(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    return True
                except OSError:
                    return False
        
        print("🔌 Checking port availability...")
        
        if not is_port_available(8000):
            print("⚠️  Port 8000 is in use, attempting to free it...")
            try:
                # Try to kill processes on port 8000
                subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True, check=True)
                subprocess.run("lsof -ti:8000 | xargs kill -9 2>/dev/null || true", shell=True)
                time.sleep(2)
                if not is_port_available(8000):
                    print("❌ Could not free port 8000. Please manually stop any Django servers.")
                    return False
                else:
                    print("✅ Port 8000 freed")
            except:
                print("❌ Port 8000 is in use and could not be freed")
                return False
        
        if not is_port_available(3000):
            print("⚠️  Port 3000 is in use, attempting to free it...")
            try:
                subprocess.run("lsof -ti:3000 | xargs kill -9 2>/dev/null || true", shell=True)
                time.sleep(2)
                if not is_port_available(3000):
                    print("❌ Could not free port 3000. Please manually stop any React servers.")
                    return False
                else:
                    print("✅ Port 3000 freed")
            except:
                print("❌ Port 3000 is in use and could not be freed")
                return False
        
        print("✅ Ports 8000 and 3000 are available!")
        return True
    
    def get_python_executable(self):
        """Get the appropriate Python executable"""
        # Try python3 first, then python
        for cmd in ["python3", "python"]:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except FileNotFoundError:
                continue
        return "python3"  # Default fallback
        """Get the appropriate Python executable"""
        # Try python3 first, then python
        for cmd in ["python3", "python"]:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return cmd
            except FileNotFoundError:
                continue
        return "python3"  # Default fallback
    
    def check_and_install_python_deps(self):
        """Check and install Python dependencies"""
        print("📦 Checking Python dependencies...")
        
        python_cmd = self.get_python_executable()
        
        # Check if Django is installed
        try:
            result = subprocess.run([python_cmd, "-c", "import django; print('Django', django.VERSION)"], 
                                  capture_output=True, text=True, cwd=self.backend_dir)
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
                return True
        except:
            pass
        
        print("📦 Installing Python dependencies from requirements.txt...")
        try:
            # Check if requirements.txt exists
            requirements_file = self.backend_dir / "requirements.txt"
            if requirements_file.exists():
                print("Installing from requirements.txt...")
                result = subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                                      capture_output=True, text=True, cwd=self.backend_dir)
                if result.returncode != 0:
                    print(f"❌ Failed to install from requirements.txt: {result.stderr}")
                    return False
                print("✅ Python dependencies installed from requirements.txt!")
                return True
            else:
                # Fallback to individual package installation
                print("requirements.txt not found, installing individual packages...")
                packages = [
                    "django",
                    "djangorestframework", 
                    "django-cors-headers",
                    "requests"
                ]
                
                for package in packages:
                    print(f"Installing {package}...")
                    result = subprocess.run([python_cmd, "-m", "pip", "install", package], 
                                          capture_output=True, text=True)
                    if result.returncode != 0:
                        print(f"❌ Failed to install {package}: {result.stderr}")
                        return False
                
                print("✅ Python dependencies installed!")
                return True
        except Exception as e:
            print(f"❌ Failed to install Python dependencies: {e}")
            return False
    
    def start_backend(self):
        """Start Django backend server"""
        print("🚀 Starting Django backend...")
        try:
            os.chdir(self.backend_dir)
            python_cmd = self.get_python_executable()
            
            # Run migrations first
            print("📋 Running Django migrations...")
            migrate_result = subprocess.run([python_cmd, "manage.py", "migrate"], 
                                          capture_output=True, text=True)
            if migrate_result.returncode != 0:
                print(f"⚠️  Migration warning: {migrate_result.stderr}")
            else:
                print("✅ Migrations completed!")
            
            self.backend_process = subprocess.Popen(
                [python_cmd, "manage.py", "runserver", "8000"],
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
                try:
                    while True:
                        output = self.backend_process.stdout.readline()
                        if output:
                            print(f"[BACKEND] {output.strip()}")
                        else:
                            break
                except:
                    pass
                    
                try:
                    while True:
                        error = self.backend_process.stderr.readline()
                        if error:
                            print(f"[BACKEND ERROR] {error.strip()}")
                        else:
                            break
                except:
                    pass
                        
        def monitor_frontend():
            if self.frontend_process:
                try:
                    while True:
                        output = self.frontend_process.stdout.readline()
                        if output:
                            line = output.strip()
                            if line and "webpack" not in line.lower():
                                print(f"[FRONTEND] {line}")
                        else:
                            break
                except:
                    pass
                    
                try:
                    while True:
                        error = self.frontend_process.stderr.readline()
                        if error:
                            print(f"[FRONTEND ERROR] {error.strip()}")
                        else:
                            break
                except:
                    pass
        
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
        
        # Check port availability
        if not self.check_ports():
            sys.exit(1)
        
        # Check and install Python dependencies
        if not self.check_and_install_python_deps():
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
                    # Print any remaining output
                    if self.backend_process.stderr:
                        stderr_output = self.backend_process.stderr.read()
                        if stderr_output:
                            print(f"Backend error: {stderr_output}")
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
