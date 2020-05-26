from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def notifications(subcommand, profile_name, notification_id,
            notification_channel, notification_destination,
            error_type, error_threshold):

    payload = {}
    if subcommand in ["remove"]:
        payload["notification_id"] = notification_id

    if subcommand in ["add"]:
        payload["notification_channel"] = notification_channel
        payload[error_type] = error_threshold

        if notification_channel == "SLACK":
            payload["notification_webhook"] = notification_destination
        if notification_channel == "EMAIL":
            payload["notification_email"] = notification_destination


    notifications_path = path("notifications", subcommand)

    response = send_request(
        notifications_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)
