from flask import Flask, render_template, redirect, url_for, request, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'multipass_manager_secret_key'  # Needed for flash messages

# FastAPI backend URL
API_URL = 'http://localhost:8001'

@app.route('/')
def index():
    """Main page with multipass instances table"""
    # Get multipass version
    try:
        version_response = requests.get(f"{API_URL}/version")
        version_data = version_response.json().get('version', {})
    except Exception as e:
        version_data = {"error": str(e)}

    # Get multipass instances
    try:
        instances_response = requests.get(f"{API_URL}/list")
        instances_data = instances_response.json().get('list', [])
    except Exception as e:
        instances_data = []
        flash(f"Error fetching instances: {str(e)}", "error")

    return render_template('index.html', 
                          version=version_data, 
                          instances=instances_data)

@app.route('/start/<name>', methods=['POST'])
def start_instance(name):
    """Start a multipass instance"""
    try:
        response = requests.get(f"{API_URL}/start/{name}")
        if response.status_code == 200:
            flash(f"Started instance {name}", "success")
        else:
            flash(f"Failed to start instance {name}: {response.text}", "error")
    except Exception as e:
        flash(f"Error starting instance {name}: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/stop/<name>', methods=['POST'])
def stop_instance(name):
    """Stop a multipass instance"""
    try:
        response = requests.get(f"{API_URL}/stop/{name}")
        if response.status_code == 200:
            flash(f"Stopped instance {name}", "success")
        else:
            flash(f"Failed to stop instance {name}: {response.text}", "error")
    except Exception as e:
        flash(f"Error stopping instance {name}: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/info/<name>')
def instance_info(name):
    """Show detailed information about a multipass instance"""
    try:
        response = requests.get(f"{API_URL}/info/{name}")
        info_data = response.json()
    except Exception as e:
        info_data = {"error": str(e)}
        flash(f"Error fetching info for {name}: {str(e)}", "error")

    return render_template('info.html', name=name, info=info_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
