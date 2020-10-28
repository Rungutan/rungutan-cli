import time

import simplejson as json

from rungutan.authentication import auth
from rungutan.send_request import send_request
from rungutan.config import path
from rungutan.print_format import print_message
from rungutan.config import sleep_timeout
from rungutan.config import test_running_status
from rungutan.config import test_error_status
from rungutan.config import test_finished_status
from rungutan.config import test_cancelled_status


def tests(subcommand, profile_name, test_id, test_file, template_id, test_public, test_name, wait_to_finish):

    payload = {}
    if subcommand in ["cancel", "get", "set-sharing", "list", "remove"]:
        if test_id is not None:
            payload["test_id"] = test_id

    if subcommand in ["set-sharing"]:
        payload["test_public"] = test_public

    if subcommand in ["add", "preview-credits"]:
        if template_id is None:
            try:
                test_file = json.load(test_file)
                for key in test_file:
                    payload[key] = test_file[key]
            except Exception as e:
                print(e)
                exit(1)
        else:
            payload_template = {
                "template_id": template_id
            }
            templates_path = path("templates", "get")
            templates_response = send_request(
                templates_path,
                payload_template,
                auth(profile_name)
            )
            if templates_response["success"]:
                for key in templates_response["response_json"]["TestData"]:
                    payload[key] = templates_response["response_json"]["TestData"][key]
            else:
                print_message(templates_response["error"])
                exit(1)

    if test_name is not None:
        payload["test_name"] = test_name

    tests_path = path("tests", subcommand)

    response = send_request(
        tests_path,
        payload,
        auth(profile_name)
    )
    if response["success"]:
        print_message(response["response_json"])

        if wait_to_finish and subcommand in ["add"]:
            still_running = True
            print("Waiting for test to finish...")
            test_id = response["response_json"]["test_id"]

            # Wait for completion
            test_status = None
            while still_running:
                tests_path = path("tests", "list")
                response = send_request(
                    tests_path,
                    {"test_id": test_id},
                    auth(profile_name)
                )
                if "Tests" in response["response_json"]:
                    test_status = str(response["response_json"]['Tests'][0]["test_status"]).upper()
                    if test_status in test_running_status():
                        time.sleep(sleep_timeout())
                    elif test_status in test_error_status():
                        print("Test with ID {} has finished running with status {}".format(test_id, test_status))
                        exit(1)
                    else:
                        print("Test with ID {} has finished running with status {}".format(test_id, test_status))
                        still_running = False

            # Print summary results
            if test_status not in test_cancelled_status():
                results_path = path("results", "get")
                response = send_request(
                    results_path,
                    {"test_id": test_id, "results_region": "overall"},
                    auth(profile_name)
                )
                if response["success"]:
                    print_message(response["response_json"])
                    exit(0)
                else:
                    print_message(response["error"])
                    exit(1)
            else:
                print("Summary results are only available for non-cancelled tests.\n"
                      "Please see web-platform for raw results captured before cancelling the test.")

        exit(0)
    else:
        print_message(response["error"])
        exit(1)

