import requests
import json
from datetime import datetime, timedelta

# Shoutcast JSON stats endpoint — sid=1 is the default stream ID
URL = "http://live4.rcast.net:8368/stats?sid=1&json=1"

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Shoutcast uses 'songtitle', not 'title'
    current_song = data.get("songtitle", "Unknown")

    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "song": current_song
    }

    # Load existing history
    try:
        with open("playlist.json", "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # Duplicate check against the most recent entry
    if not history or history[0]["song"] != current_song:
        history.insert(0, new_entry)
        print(f"Added new song: {current_song}")
    else:
        print("Song hasn't changed. Skipping.")

    # Rolling 7-day cleanup
    seven_days_ago = datetime.now() - timedelta(days=7)
    history = [
        entry for entry in history
        if datetime.fromisoformat(entry["timestamp"]) > seven_days_ago
    ]

    # Save
    with open("playlist.json", "w") as f:
        json.dump(history, f, indent=4)

except Exception as e:
    print(f"Error: {e}")
