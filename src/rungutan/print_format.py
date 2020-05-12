import simplejson as json


def print_message(message, output_format="json"):
    if output_format == "json":
        print(json.dumps(message, indent=4))
