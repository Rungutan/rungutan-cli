import os
import simplejson as json
from os.path import expanduser
from rungutan.config import *


def auth_profile(profile_name):

    try:
        # Get credentials from home folder
        home_folder = expanduser("~")
        rungutan_folder = os.path.join(home_folder, os_folder())
        if not os.path.exists(rungutan_folder):
            os.makedirs(rungutan_folder)
        credentials_file = os.path.join(rungutan_folder, os_file())

        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as stream:
                try:
                    local_credentials = json.load(stream)
                    return local_credentials[profile_name]
                except Exception as e:
                    return False
    except Exception as e:
        print(str(e))
        exit(1)
        return False


def auth(profile_name=None):

    # Try first with whatever profile name is defined
    profile_auth = auth_profile(profile_name)
    if profile_auth:
        return profile_auth

    # If that doesn't work, check OS variables
    if os_env_team_id() in os.environ and os_env_api_key() in os.environ:
        return {
            "team_id": os.environ.get(os_env_team_id()),
            "api_key": os.environ.get(os_env_api_key())
        }

    print("Unable to authenticate using either local credentials or environment variables")
    exit(1)
