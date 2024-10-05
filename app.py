from flask import Flask, request, jsonify
from calendar_client import NextCloudCalendarClient
from datetime import datetime
import os

app = Flask(__name__)

nextcloud_url = os.getenv('NEXTCLOUD_URL')
username = os.getenv('NEXTCLOUD_USERNAME')
password = os.getenv('NEXTCLOUD_PASSWORD')
verify_ssl = os.getenv('VERIFY_SSL', 'False').lower() in ('true', '1')

calendar_client = NextCloudCalendarClient(nextcloud_url, username, password, verify_ssl)

def parse_event_data(data):
    try:
        return {
            'calendar_name': data.get('calendar_name'),
            'start_time': datetime.fromisoformat(data.get('start_time')),
            'end_time': datetime.fromisoformat(data.get('end_time')),
            'summary': data.get('summary'),
            'description': data.get('description', ''),
            'timezone': data.get('timezone', 'Asia/Tokyo')
        }
    except Exception as e:
        print(f"Error parsing event data: {e}")
        return False

@app.route('/calendars', methods=['GET'])
def get_calendars():
    try:
        calendars = calendar_client.get_calendars()
        if calendars is False:
            return jsonify({"error": "Failed to retrieve calendars"}), 500
        return jsonify({"calendars": calendars})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = parse_event_data(request.json)
    if not event_data:
        return jsonify({"error": "Invalid event data"}), 400
    try:
        result = calendar_client.add_event(
            event_data.get('calendar_name'),
            event_data.get('start_time'),
            event_data.get('end_time'),
            event_data.get('summary'),
            event_data.get('description', ''),
            event_data.get('timezone', 'Asia/Tokyo') 
        )
        if result is False:
            return jsonify({"error": "Failed to add event"}), 500
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/delete_event', methods=['DELETE'])
def delete_event():
    data = request.json
    try:
        result = calendar_client.delete_event(data.get('calendar_name'), data.get('summary'))
        if result is False:
            return jsonify({"error": "Failed to delete event"}), 500
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/events', methods=['GET'])
def get_events():
    calendar_name = request.args.get('calendar_name')
    try:
        events = calendar_client.get_events(calendar_name)
        if events is False:
            return jsonify({"error": "Failed to retrieve events"}), 500
        return jsonify({"events": events})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/event_exists', methods=['GET'])
def event_exists():
    calendar_name = request.args.get('calendar_name')
    summary = request.args.get('summary')

    if not calendar_name or not summary:
        return jsonify({"error": "calendar_name and summary are required"}), 400

    try:
        exists = calendar_client.event_exists(calendar_name, summary)
        return jsonify({"exists": exists})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
