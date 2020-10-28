from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def raw_results(subcommand, profile_name, test_id, results_region, results_type, results_path,
                results_method, min_timestamp, max_timestamp):

    payload = {}
    if subcommand in ["get"]:
        payload["test_id"] = test_id
        payload["results_region"] = results_region
        payload["results_type"] = results_type
        payload["results_path"] = results_path
        payload["results_method"] = results_method
        payload["min_timestamp"] = min_timestamp
        payload["max_timestamp"] = max_timestamp

    results_path = path("raw_results", subcommand)

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
