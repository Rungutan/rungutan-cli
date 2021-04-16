from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def file(subcommand, profile_name,  file_id):

    payload = {}
    if subcommand in ["get", "list", "remove"]:
        if file_id is not None:
            payload["file_id"] = file_id

    file_path = path("file", subcommand)

    response = send_request(
        file_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
