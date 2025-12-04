"""
IoT Home Security System - Flask Web Application
Main application file with all routes and functionality
"""

from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime, timedelta
import config

app = Flask(__name__)

# Configuration - Load from config.py (which uses .env or environment variables)
AIO_USERNAME = config.AIO_USERNAME
AIO_KEY = config.AIO_KEY
DB_CONNECTION_STRING = config.DATABASE_URL

# Flask secret key for sessions
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY

# Adafruit IO API endpoints
AIO_BASE_URL = 'https://io.adafruit.com/api/v2'

# Feed names from config
FEEDS = config.FEEDS


# Helper Functions
def get_aio_headers():
    """Return headers for Adafruit IO API requests"""
    return {
        'X-AIO-Key': AIO_KEY,
        'Content-Type': 'application/json'
    }


def get_feed_value(feed_key):
    """Get the latest value from an Adafruit IO feed"""
    try:
        url = f"{AIO_BASE_URL}/{FEEDS[feed_key]}/data/last"
        response = requests.get(url, headers=get_aio_headers(), timeout=5)
        if response.status_code == 200:
            return response.json()['value']
        return None
    except Exception as e:
        print(f"Error fetching {feed_key}: {e}")
        return None


def send_feed_value(feed_key, value):
    """Send a value to an Adafruit IO feed"""
    try:
        url = f"{AIO_BASE_URL}/{FEEDS[feed_key]}/data"
        data = {"value": str(value)}
        response = requests.post(url, headers=get_aio_headers(), json=data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to {feed_key}: {e}")
        return False


def get_historical_data(feed_key, start_date, end_date):
    """Get historical data from Adafruit IO for a date range"""
    try:
        # Format dates for API
        start_time = f"{start_date}T00:00:00Z"
        end_time = f"{end_date}T23:59:59Z"

        url = f"{AIO_BASE_URL}/{FEEDS[feed_key]}/data"
        params = {
            'start_time': start_time,
            'end_time': end_time,
            'limit': 1000  # Maximum allowed by Adafruit IO
        }

        response = requests.get(url, headers=get_aio_headers(), params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Parse and return in format suitable for Chart.js
            timestamps = []
            values = []
            for item in reversed(data):  # Reverse to get chronological order
                timestamps.append(item['created_at'])
                values.append(float(item['value']))
            return {'timestamps': timestamps, 'values': values}
        return {'timestamps': [], 'values': []}
    except Exception as e:
        print(f"Error fetching historical data for {feed_key}: {e}")
        return {'timestamps': [], 'values': []}


def get_intrusion_events(date):
    """Get intrusion events for a specific date from database or local logs"""
    # TODO: Implement database query when Neon.tech is set up
    # For now, return mock data
    intrusions = []

    # Example: Read from local CSV files if database not available
    try:
        import csv
        log_file = f"../data/{date}_home_env.csv"
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('event_type') == 'motion_detected':
                    intrusions.append({
                        'timestamp': row['timestamp'],
                        'details': row.get('details', 'Motion detected')
                    })
    except FileNotFoundError:
        pass

    return intrusions


# Routes
@app.route('/')
def index():
    """Home page / Main Dashboard"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')


@app.route('/environmental')
def environmental():
    """Environmental data page with historical charts"""
    return render_template('environmental.html')


@app.route('/security')
def security():
    """Security management page"""
    return render_template('security.html')


@app.route('/control')
def control():
    """Device control page"""
    return render_template('control.html')


# API Endpoints
@app.route('/api/live-data')
def api_live_data():
    """Proxy live data request to Adafruit IO"""
    sensors = ['temperature', 'humidity', 'motion', 'light', 'fan', 'mode']
    data = {}
    for sensor in sensors:
        url = f"{AIO_BASE_URL}/{FEEDS[sensor]}/data/last"
        try:
            response = requests.get(url, headers=get_aio_headers(), timeout=5)
            if response.status_code == 200:
                data[sensor] = response.json().get('value')
            else:
                data[sensor] = None
        except Exception as e:
            data[sensor] = None
    data['timestamp'] = datetime.now().isoformat()
    return jsonify(data)


@app.route('/api/historical-data')
def api_historical_data():
    """Proxy historical data request to Adafruit IO"""
    sensor = request.args.get('sensor', 'temperature')
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    start_time = f"{date}T00:00:00Z"
    end_time = f"{date}T23:59:59Z"
    url = f"{AIO_BASE_URL}/{FEEDS[sensor]}/data"
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'limit': 1000
    }
    try:
        response = requests.get(url, headers=get_aio_headers(), params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            timestamps = [item['created_at'] for item in reversed(data)]
            values = [float(item['value']) for item in reversed(data)]
            return jsonify({'timestamps': timestamps, 'values': values})
        else:
            return jsonify({'timestamps': [], 'values': []})
    except Exception as e:
        return jsonify({'timestamps': [], 'values': []})


@app.route('/api/intrusions')
def api_intrusions():
    """Proxy intrusion events request to Adafruit IO (motion feed)"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    start_time = f"{date}T00:00:00Z"
    end_time = f"{date}T23:59:59Z"
    url = f"{AIO_BASE_URL}/{FEEDS['motion']}/data"
    params = {
        'start_time': start_time,
        'end_time': end_time,
        'limit': 1000
    }
    intrusions = []
    try:
        response = requests.get(url, headers=get_aio_headers(), params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                if item.get('value') == '1':
                    intrusions.append({
                        'timestamp': item['created_at'],
                        'details': 'Motion detected'
                    })
        return jsonify({'intrusions': intrusions})
    except Exception as e:
        return jsonify({'intrusions': []})


@app.route('/api/control/<device>', methods=['POST'])
def api_control_device(device):
    """Proxy device control request to Adafruit IO"""
    data = request.get_json()
    value = data.get('value')
    if device in ['light', 'fan', 'mode']:
        url = f"{AIO_BASE_URL}/{FEEDS[device]}/data"
        payload = {"value": str(value)}
        try:
            response = requests.post(url, headers=get_aio_headers(), json=payload, timeout=5)
            success = response.status_code == 200
        except Exception as e:
            success = False
        return jsonify({'success': success, 'device': device, 'value': value})
    return jsonify({'success': False, 'error': 'Invalid device'}), 400


@app.route('/api/system-status')
def api_system_status():
    """Proxy system status request to Adafruit IO"""
    def get_value(feed):
        url = f"{AIO_BASE_URL}/{FEEDS[feed]}/data/last"
        try:
            response = requests.get(url, headers=get_aio_headers(), timeout=5)
            if response.status_code == 200:
                return response.json().get('value')
        except Exception:
            pass
        return None
    mode = get_value('mode')
    motion = get_value('motion')
    light = get_value('light')
    fan = get_value('fan')
    status = {
        'mode': mode,
        'motion_detected': motion == '1',
        'devices': {
            'light': light == '1',
            'fan': fan == '1'
        },
        'last_update': datetime.now().isoformat()
    }
    return jsonify(status)


# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Run in debug mode for development
    # Set debug=False for production
    app.run(host='0.0.0.0', port=5000, debug=True)