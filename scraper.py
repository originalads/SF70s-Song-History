import requests
import json
from datetime import datetime, timedelta

URL = "http://live4.rcast.net"

try:
    response = requests.get(URL, timeout=10)
    data = response.json()
    
    # 1. Grab the current song (Adjusted to 'title' based on your stream)
    current_song = data.get('title', 'Unknown')
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "song": current_song
    }

    # 2. Load the existing file (if it exists)
    try:
        with open('playlist.json', 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # 3. DUPLICATE CHECK: Look at the very first item in the list
    if not history or history[0]['song'] != current_song:
        history.insert(0, new_entry)
        print(f"Added new song: {current_song}")
    else:
        print("Song hasn't changed. Skipping.")


    # 4. ROLLING 7-DAY CLEANUP
    seven_days_ago = datetime.now() - timedelta(days=7)
    history = [entry for entry in history if datetime.fromisoformat(entry['timestamp']) > seven_days_ago]

    # 5. Save it back
    with open('playlist.json', 'w') as f:
        json.dump(history, f, indent=4)

except Exception as e:
    print(f"Error: {e}")

