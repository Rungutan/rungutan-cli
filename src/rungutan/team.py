from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def team(subcommand, profile_name, member_email, member_role):

    payload = {}
    if subcommand in ["change", "remove", "add"]:
        payload["member_email"] = member_email

    if subcommand in ["change", "add"]:
        payload["member_role"] = member_role

    team_path = path("team", subcommand)

    response = send_request(
        team_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
