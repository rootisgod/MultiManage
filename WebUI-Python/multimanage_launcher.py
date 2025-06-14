#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import time
import webbrowser
import signal
import platform
import atexit

# Determine if we're running from a PyInstaller bundle
RUNNING_BUNDLED = getattr(sys, 'frozen', False)

# Get the appropriate base directory
if RUNNING_BUNDLED:
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up paths for both bundled and development environments
API_DIR = os.path.join(BASE_DIR, 'api') if not RUNNING_BUNDLED else BASE_DIR
WEB_DIR = os.path.join(BASE_DIR, 'web') if not RUNNING_BUNDLED else BASE_DIR

# Global variables to store process information
api_process = None
web_process = None

def clean_up():
    """Clean up processes on exit"""
    if api_process:
        try:
            if platform.system() == 'Windows':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(api_process.pid)])
            else:
                os.killpg(os.getpgid(api_process.pid), signal.SIGTERM)
        except:
            pass
    
    if web_process:
        try:
            if platform.system() == 'Windows':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(web_process.pid)])
            else:
                os.killpg(os.getpgid(web_process.pid), signal.SIGTERM)
        except:
            pass
    
    print("MultiManage has been shut down.")

# Register the cleanup function to be called on exit
atexit.register(clean_up)

def start_api_server():
    """Start the FastAPI backend server"""
    global api_process
    
    print("Starting FastAPI backend server...")
    
    os.chdir(API_DIR)
    
    if RUNNING_BUNDLED:
        # When bundled, we need to run uvicorn directly
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", "--host", "0.0.0.0", "--port", "8001"
        ]
    else:
        # In development, use the start script
        cmd = ['./start.sh']
        if platform.system() == 'Windows':
            # On Windows, we need to handle this differently
            os.chdir(API_DIR)
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "main:app", "--host", "0.0.0.0", "--port", "8001"
            ]
    
    # Start the API server process
    api_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=(platform.system() == 'Windows'),
        preexec_fn=None if platform.system() == 'Windows' else os.setsid
    )
    
    # Give the API server time to start
    time.sleep(2)
    
    # Check if API server is running
    try:
        import requests
        response = requests.get("http://127.0.0.1:8001")
        if response.status_code == 200:
            print("FastAPI server started successfully on http://127.0.0.1:8001")
            return True
    except:
        print("Warning: FastAPI server may not have started correctly")
        return False

def start_web_server():
    """Start the Flask web server"""
    global web_process
    
    print("Starting Flask web server...")
    
    os.chdir(WEB_DIR)
    
    if RUNNING_BUNDLED:
        # When bundled, we need to run Flask directly
        cmd = [
            sys.executable, "-c", 
            "from app import app; app.run(port=5000)"
        ]
    else:
        # In development, use the start script
        cmd = ['./start.sh']
        if platform.system() == 'Windows':
            # On Windows, we need to handle this differently
            os.chdir(WEB_DIR)
            cmd = [
                sys.executable, "-c", 
                "from app import app; app.run(port=5000)"
            ]
    
    # Start the web server process
    web_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=(platform.system() == 'Windows'),
        preexec_fn=None if platform.system() == 'Windows' else os.setsid
    )
    
    # Give the web server time to start
    time.sleep(2)
    
    # Check if web server is running
    try:
        import requests
        response = requests.get("http://127.0.0.1:5000")
        if response.status_code == 200:
            print("Flask server started successfully on http://127.0.0.1:5000")
            return True
    except:
        print("Warning: Flask server may not have started correctly")
        return False

def output_monitor(process, prefix):
    """Monitor and print output from a subprocess"""
    for line in iter(process.stdout.readline, ''):
        print(f"{prefix}: {line.strip()}")
    
    process.stdout.close()

def main():
    """Main function to start the application"""
    print("Starting MultiManage...")
    
    # Start the API server
    api_started = start_api_server()
    
    if not api_started:
        print("Failed to start API server. Exiting.")
        sys.exit(1)
    
    # Start output monitoring for API server in a separate thread
    api_monitor = threading.Thread(
        target=output_monitor, 
        args=(api_process, "API"),
        daemon=True
    )
    api_monitor.start()
    
    # Start the web server
    web_started = start_web_server()
    
    if not web_started:
        print("Failed to start web server. Exiting.")
        clean_up()
        sys.exit(1)
    
    # Start output monitoring for web server in a separate thread
    web_monitor = threading.Thread(
        target=output_monitor, 
        args=(web_process, "WEB"),
        daemon=True
    )
    web_monitor.start()
    
    # Open the web browser
    print("Opening web browser...")
    webbrowser.open("http://127.0.0.1:5000")
    
    print("MultiManage is now running!")
    print("Press Ctrl+C to exit.")
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down MultiManage...")
        clean_up()

if __name__ == "__main__":
    main()
