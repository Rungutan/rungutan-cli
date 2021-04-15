from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def csv(subcommand, profile_name,  csv_id):

    payload = {}
    if subcommand in ["get", "list", "remove"]:
        if csv_id is not None:
            payload["csv_id"] = csv_id

    csv_path = path("csv", subcommand)

    response = send_request(
        csv_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
