import simplejson as json

from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message


def crons(subcommand, profile_name, cron_id, test_file, cron_enabled,
          test_name, schedule_type, schedule_hour, schedule_minute,
          schedule_weekday, schedule_day_of_month):

    payload = {}
    if subcommand in ["remove", "get", "set-status", "list"]:
        if cron_id is not None:
            payload["cron_id"] = cron_id

    if subcommand in ["set-status"]:
        payload["cron_enabled"] = cron_enabled

    if subcommand in ["add", "preview-credits"]:
        try:
            test_file = json.load(test_file)
            for key in test_file:
                payload[key] = test_file[key]
            payload["test_type"] = "CRON"
        except Exception as e:
            print(e)
            exit(1)

    if test_name is not None:
        payload["test_name"] = test_name

    if schedule_type is not None:
        payload["schedule_type"] = schedule_type

    if schedule_hour is not None:
        payload["schedule_hour"] = schedule_hour

    if schedule_minute is not None:
        payload["schedule_minute"] = schedule_minute

    if schedule_weekday is not None:
        payload["schedule_weekday"] = schedule_weekday

    if schedule_day_of_month is not None:
        payload["schedule_day_of_month"] = schedule_day_of_month

    crons_path = path("crons", subcommand)

    response = send_request(
        crons_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])
        exit(0)
    else:
        print_message(response["error"])
        exit(1)

