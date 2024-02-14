"""
file: auth_data_controller.py

description: This module handles saving and loading athletes for the Discord bot.

Author: Julian Friedl
"""

import datetime
import json
import os
from dotenv import load_dotenv
import logging

from config.log_config import setup_logging
from threading import Lock

from models.activity import Activity
from models.athlete import Athlete

file_lock = Lock()  # locking mechanism for threading

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()

YEAR = int(os.getenv("YEAR", datetime.date.today().year))

SRC_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(os.path.dirname(BASE_PATH), 'data')
YEAR_PATH = os.path.join(DATA_PATH, str(YEAR))
ATHLETES = os.path.join(YEAR_PATH, 'athletes.json')
ROUTES = os.path.join(YEAR_PATH, 'routes.json')
RULES_TEMPLATE = os.path.join(os.path.dirname(BASE_PATH), 'rules_template.json')
GLOBAL_RULES_FILE = os.path.join(YEAR_PATH, 'global_rules.json')  # Path to the global_rules.json

# Function to load rules from the JSON file
def load_global_rules():
    # Check if GLOBAL_RULES_FILE exists and has content; if not, copy from RULES_TEMPLATE
    if not os.path.exists(GLOBAL_RULES_FILE) or os.path.getsize(GLOBAL_RULES_FILE) == 0:
        with open(RULES_TEMPLATE, 'r') as template_file:
            rules_data = json.load(template_file)
        with open(GLOBAL_RULES_FILE, 'w') as global_rules_file:
            json.dump(rules_data, global_rules_file, indent=4)
        data = rules_data
    else:
        with open(GLOBAL_RULES_FILE, 'r') as global_rules_file:
            data = json.load(global_rules_file)
    return data['constants']

# Load the constants from the rules_preset.json
constants = load_global_rules()

# Example usage in save_strava_athletes function
def save_strava_athletes(response: json = None, discord_user_id: str = None):
    """
    Saves user athletes to a file.

    This function takes a JSON string containing user athletes, 
    checks if a file for the user already exists, and either appends to or overwrites the file.
    """
    with file_lock:
        logger.info("Saving Credentials.")
        if response:
            json_response = json.loads(response)

        athlete_constants = {
            "rules": constants['RULES'],
            "points_required": constants['POINTS_REQUIRED'],
            "price_per_week": constants['PRICE_PER_WEEK'],
            "spazi": constants['SPAZI'],
            "walking_limit": constants['WALKING_LIMIT'],
            "hit_required": constants['HIT_REQUIRED'],
            "hit_min_time": constants['HIT_MIN_TIME'],
            "min_duration_multi_day": constants['MIN_DURATION_MULTI_DAY'],
            "start_week": constants['CHALLENGE_START_WEEK'],
        }

        athlete_vars = {
            "joker": constants['JOKER'],
            "joker_weeks": [],
            "week_results": []
        }

        athlete = {}
        if 'strava_data' in json_response:
            athlete['strava_data'] = json_response['strava_data']
        else:
            athlete['strava_data'] = json_response
        athlete['constants'] = athlete_constants
        athlete['vars'] = athlete_vars
        athlete['discord_user_id'] = discord_user_id

        data = load_or_create_athletes()

        # Update or append the new athletes
        for existing_cred in data:
            if existing_cred['strava_data']['athlete']['id'] == athlete['strava_data']['athlete']['id']:
                existing_cred['strava_data'] = athlete['strava_data']
                if athlete['discord_user_id']:
                    existing_cred['discord_user_id'] = athlete['discord_user_id']
                break
        else:
            data.append(athlete)

        with open(ATHLETES, 'w') as f:
            json.dump(data, f, default=serialize, indent=4)


def update_athlete_vars(athlete: dict):
    with file_lock:
        data = load_or_create_athletes()
        for existing_cred in data:
            if existing_cred['strava_data']['athlete']['id'] == athlete['strava_data']['athlete']['id']:
                if athlete['vars']:
                    existing_cred['vars'] = athlete['vars']
                break
        with open(ATHLETES, 'w') as f:
            json.dump(data, f, default=serialize, indent=4)


def save_routes(activity: Activity, user: Athlete):
    new_route = {
        "user_id": user.user_id,
        "discord_user_id": user.discord_id,
        "user_name": user.username,
        "activity_id": activity.id,
        "type": activity.type,
        "start_date": activity.start_date,
        "moving_time": activity.duration,
        "distance": activity.distance,
        "total_elevation_gain": activity.elev_gain,
        "map": activity.map
    }
    if new_route["map"]["summary_polyline"] == "":
        return

    with file_lock:
        data = {"metadata": {"total_moving_time": 0, "total_distance": 0, "total_elevation_gain": 0}, "routes": []}
        
        if os.path.exists(ROUTES) and os.path.getsize(ROUTES) > 0:
            with open(ROUTES, 'r') as file:
                data = json.load(file)
                
        existing_route_index = next((index for (index, d) in enumerate(data["routes"]) if d["activity_id"] == new_route["activity_id"]), None)
        
        if existing_route_index is not None:
            # Subtract old values from metadata
            old_route = data["routes"][existing_route_index]
            data["metadata"]["total_moving_time"] -= old_route.get("moving_time", 0)
            data["metadata"]["total_distance"] -= old_route.get("distance", 0)
            data["metadata"]["total_elevation_gain"] -= old_route.get("total_elevation_gain", 0)
            
            # Replace the existing route
            data["routes"][existing_route_index] = new_route
        else:
            # Append the new route
            data["routes"].append(new_route)
        
        # Add new values to metadata
        data["metadata"]["total_moving_time"] += new_route.get("moving_time", 0)
        data["metadata"]["total_distance"] += new_route.get("distance", 0)
        data["metadata"]["total_elevation_gain"] += new_route.get("total_elevation_gain", 0)
        
        with open(ROUTES, 'w') as f:
            json.dump(data, f, default=serialize, indent=4)



def load_or_create_athletes():
    # Create the data directory if it doesn't exist
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    
    if not os.path.exists(YEAR_PATH):
        os.makedirs(YEAR_PATH)

    # Load existing data or initialize it
    if os.path.exists(ATHLETES) and os.path.getsize(ATHLETES) > 0:
        with open(ATHLETES, 'r') as file:
            data = json.load(file)
    else:
        data = []

    return data


def load_athletes():
    """
    Loads user athletes from a file.

    This function checks if a file with user athletes exists, and if so, loads and returns the athletes.
    """
    with file_lock:
        if os.path.exists(ATHLETES) and os.path.getsize(ATHLETES) != 0:
            with open(ATHLETES, 'r') as f:
                athletes = json.load(f)
            return athletes
        return None


def serialize(obj):
    """
    Serializes an object to be saved to a file.

    This function converts set and bytes objects to lists and strings respectively, 
    and recursively applies itself to elements of dictionaries, lists, and tuples.
    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize(i) for i in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj
