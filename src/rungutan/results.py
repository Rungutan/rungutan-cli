from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def results(subcommand, profile_name, test_id, results_region):

    payload = {}
    if subcommand in ["get"]:
        payload["test_id"] = test_id

    if subcommand in ["get"]:
        payload["results_region"] = results_region

    results_path = path("results", subcommand)

    response = send_request(
        results_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
