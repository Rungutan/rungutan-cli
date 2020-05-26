from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def domains(subcommand, profile_name, domain_name):

    payload = {}
    if subcommand != "list":
        payload["domain_name"] = domain_name

    domain_path = path("domains", subcommand)

    response = send_request(
        domain_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
