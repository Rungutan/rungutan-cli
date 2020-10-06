import time

import simplejson as json

from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def templates(subcommand, profile_name, template_id, test_file, test_name):

    payload = {}
    if subcommand in ["remove", "get", "list"]:
        if template_id is not None:
            payload["template_id"] = template_id

    if subcommand in ["add"]:
        try:
            test_file = json.load(test_file)
            for key in test_file:
                payload[key] = test_file[key]
        except Exception as e:
            print(e)
            exit(1)

    if test_name is not None:
        payload["test_name"] = test_name

    templates_path = path("templates", subcommand)

    response = send_request(
        templates_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)

