from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def certificate(subcommand, profile_name,  certificate_id):

    payload = {}
    if subcommand in ["get", "list", "remove"]:
        if certificate_id is not None:
            payload["certificate_id"] = certificate_id

    certificate_path = path("certificate", subcommand)

    response = send_request(
        certificate_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
