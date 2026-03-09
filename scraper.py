import requests
import json
from datetime import datetime, timedelta

# Your Stream URL
URL = "http://live4.rcast.net:8368/stats?sid=1&json=1"

try:
    response = requests.get(URL, timeout=10)
    data = response.json()
    
    # Extracting Artist - Title (Adjusting for your specific JSON structure)
    current_song = data.get('songtitle', 'Unknown')
    
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "song": current_song
    }

    # Load existing history or start new
    try:
        with open('playlist.json', 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    # Add new song if it's different from the last one
    if not history or history[0]['song'] != current_song:
        history.insert(0, new_entry)

    # Keep only 7 days (168 hours)
    seven_days_ago = datetime.now() - timedelta(days=7)
    history = [entry for entry in history if datetime.fromisoformat(entry['timestamp']) > seven_days_ago]

    with open('playlist.json', 'w') as f:
        json.dump(history, f, indent=4)

except Exception as e:
    print(f"Error: {e}")
