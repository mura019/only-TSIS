import json
import os
from datetime import datetime

#Handles loading/saving settings and leaderboard data for the Racer game.
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


#Default settings for the game. These will be used if the settings file is missing or corrupted.
DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "gray",
    "difficulty": "normal"
}

def _atomic_write(path, data):
    #Write JSON to a temp file and replace target to reduce corruption risk
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    os.replace(tmp, path)

def load_settings():
    """
    Load settings from SETTINGS_FILE.
    If file missing or invalid, create it with DEFAULT_SETTINGS and return default.
    """
    if not os.path.exists(SETTINGS_FILE):
        #Create default file
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        #Ensure required keys exist; if not, fill from defaults
        changed = False
        for k, v in DEFAULT_SETTINGS.items():
            if k not in data:
                data[k] = v
                changed = True
        if changed:
            save_settings(data)
        return data
    except Exception:
        #On error (corrupt file etc.) overwrite with defaults
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """
    Save settings dict to SETTINGS_FILE.
    Normalizes expected keys and types where reasonable.
    """
    #Ensure keys exist and types are sane
    out = {}
    out["sound"] = bool(settings.get("sound", DEFAULT_SETTINGS["sound"]))
    out["car_color"] = str(settings.get("car_color", DEFAULT_SETTINGS["car_color"]))
    out["difficulty"] = str(settings.get("difficulty", DEFAULT_SETTINGS["difficulty"]))
    _atomic_write(SETTINGS_FILE, out)

def load_leaderboard():
    """
    Load leaderboard list from LEADERBOARD_FILE.
    Returns list of entries (possibly empty). Each entry is a dict with at least 'name' and 'score'.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        #Create empty leaderboard file
        _atomic_write(LEADERBOARD_FILE, [])
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("leaderboard.json has invalid format")
        return data
    except Exception:
        #On error, reset to empty list
        _atomic_write(LEADERBOARD_FILE, [])
        return []

def save_score(name, score, distance):
    """
    Append a new score entry and keep top 10 by score (descending).
    Entry fields: name, score, distance, date.
    """
    try:
        board = load_leaderboard()
        entry = {
            "name": str(name)[:12] if name else "Player",
            "score": int(score) if isinstance(score, (int, float, str)) and str(score).lstrip("-").isdigit() else int(float(score)) if isinstance(score, str) and score.replace('.','',1).isdigit() else int(score) if isinstance(score, (int,)) else 0,
            "distance": int(distance) if isinstance(distance, (int, float, str)) and str(distance).lstrip("-").isdigit() else int(float(distance)) if isinstance(distance, str) and distance.replace('.','',1).isdigit() else int(distance) if isinstance(distance, (int,)) else 0,
            "date": datetime.utcnow().isoformat() + "Z"
        }
    except Exception:
        #Fallback minimal entry
        entry = {"name": "Player", "score": 0, "distance": 0, "date": datetime.utcnow().isoformat() + "Z"}

    board.append(entry)
    #Sort by score desc, then distance desc, then date
    try:
        board = sorted(board, key=lambda e: (int(e.get("score", 0)), int(e.get("distance", 0))), reverse=True)
    except Exception:
        #If sorting fails for some reason, keep insertion order
        pass
    #Keep top 10
    board = board[:10]
    _atomic_write(LEADERBOARD_FILE, board)
