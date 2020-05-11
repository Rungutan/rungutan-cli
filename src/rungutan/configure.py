import os
import simplejson as json
from os.path import expanduser
from rungutan.config import os_folder
from rungutan.config import os_file
import re


def valid_team_id(team_id):
    if type(team_id) is not str:
        return False

    if len(team_id) > 20:
        return False

    pattern = re.compile("^[^0-9][a-zA-Z0-9]+$")
    return pattern.match(team_id)


def configure(profile_name):
    try:
        # Get team_id
        team_id = input("TEAM_ID: ")
        while not valid_team_id(team_id):
            print("Invalid team_id. Try again.")
            team_id = input("TEAM_ID: ")

        # Lowercase and strip it
        team_id = team_id.strip().lower()

        # Get api key
        api_key = input("API_KEY: ")
        while type(api_key) is not str:
            print("Invalid api_key. Try again.")
            api_key = input("API_KEY: ")

        # Strip it
        api_key = api_key.strip()

        # Save credentials
        home_folder = expanduser("~")
        rungutan_folder = os.path.join(home_folder, os_folder())
        if not os.path.exists(rungutan_folder):
            os.makedirs(rungutan_folder)
        credentials_file = os.path.join(rungutan_folder, os_file())

        local_credentials = {}
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as stream:
                try:
                    local_credentials = json.load(stream)
                except Exception as e:
                    print(str(e))
                    exit(1)

        local_credentials[profile_name] = {
            "team_id": team_id,
            "api_key": api_key
        }

        try:
            with open(credentials_file, 'w', encoding='utf-8') as f:
                json.dump(local_credentials, f, indent=4)
        except Exception as e:
            print(str(e))
            exit(1)

    except Exception as e:
        print(str(e))
        exit(1)
