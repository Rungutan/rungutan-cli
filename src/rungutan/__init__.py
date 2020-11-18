import argparse
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from rungutan.configure import *
from rungutan.config import *
from rungutan.domains import *
from rungutan.team import *
from rungutan.tests import *
from rungutan.templates import *
from rungutan.results import *
from rungutan.raw_results import *
from rungutan.crons import *
from rungutan.notifications import *
from rungutan.vault import *


class RungutanCLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Rungutan CLI utility for interacting with https://rungutan.com',
            usage='''rungutan <command> [<args>]

To see help text, you can run:
    rungutan help
    rungutan version
    rungutan configure --help
    rungutan domains --help
    rungutan team --help
    rungutan results --help
    rungutan raw_results --help
    rungutan tests --help
    rungutan templates --help
    rungutan crons --help
    rungutan notifications --help
    rungutan vault --help
''')
        parser.add_argument('command', help='Command to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    # noinspection PyMethodMayBeStatic
    def configure(self):
        parser = argparse.ArgumentParser(
            description='Configure local authentication system')
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used')
        args = parser.parse_args(sys.argv[2:])
        configure(args.profile)

    # noinspection PyMethodMayBeStatic
    def version(self):
        print("1.6.0")

    # noinspection PyMethodMayBeStatic
    def domains(self):
        parser = argparse.ArgumentParser(
            description='Domain command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "validate", "remove", "add"])
        parser.add_argument('--domain_name', dest="domain_name", default=None
                            , help="Required parameter for subcommand [\"validate\", \"remove\", \"add\"]")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "validate", "remove", "add"]\n\n')
            parser.print_help()
            exit(1)
        if args.domain_name is None and args.subcommand in ["validate", "remove", "add"]:
            print('Please specify a domain name using --domain_name parameter')
            exit(1)
        domains(args.subcommand, args.profile, args.domain_name)

    # noinspection PyMethodMayBeStatic
    def notifications(self):
        parser = argparse.ArgumentParser(
            description='Notification command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "remove", "add"])
        parser.add_argument('--notification_id', dest="notification_id", default=None
                            , help="Required parameter for subcommand [\"remove\"]")
        parser.add_argument('--notification_channel', dest="notification_channel", default=None
                            , help="Required parameter for subcommand [\"add\"]")
        parser.add_argument('--notification_destination', dest="notification_destination", default=None
                            , help="Required parameter for subcommand [\"add\"].\n"
                                   "Based on whether the notification_channel is SLACK or EMAIL, provide"
                                   "a valid Slack Incoming Webhook or a valid Email Address for this param")
        parser.add_argument('--notification_failure_occurrences_threshold',
                            dest="notification_failure_occurrences_threshold", default=None
                            , help="Optional parameter for subcommand [\"add\"].\n"
                                   "If this parameter is present, "
                                   "then notification_success_response_time_threshold must"
                                   "not be invoked")
        parser.add_argument('--notification_success_response_time_threshold',
                            dest="notification_success_response_time_threshold", default=None
                            , help="Optional parameter for subcommand [\"add\"].\n"
                                   "If this parameter is present, "
                                   "then notification_failure_occurrences_threshold must"
                                   "not be invoked")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "remove", "add"]\n\n')
            parser.print_help()
            exit(1)
        if args.notification_id is None and args.subcommand in ["remove"]:
            print('Please specify a notification id using --notification_id parameter')
            exit(1)
        if args.notification_channel is None and args.subcommand in ["add"]:
            print('Please specify a notification channel using --notification_channel parameter')
            exit(1)
        if args.notification_destination is None and args.subcommand in ["add"]:
            print('Please specify a notification endpoint using --notification_destination parameter')
            exit(1)
        if args.notification_failure_occurrences_threshold is None and args.subcommand in ["add"]:
            if args.notification_success_response_time_threshold is None and args.subcommand in ["add"]:
                print('Please specify a notification type using EITHER --notification_failure_occurrences_threshold '
                      'parameter or --notification_success_response_time_threshold')
                exit(1)
        if args.notification_failure_occurrences_threshold is not None and args.subcommand in ["add"]:
            if args.notification_success_response_time_threshold is not None and args.subcommand in ["add"]:
                print('Please specify a notification type using EITHER --notification_failure_occurrences_threshold '
                      'parameter or --notification_success_response_time_threshold')
                exit(1)
        error_type = None
        error_threshold = 0
        if args.notification_failure_occurrences_threshold is not None and args.subcommand in ["add"]:
            error_type = "notification_failure_occurrences_threshold"
            error_threshold = args.notification_failure_occurrences_threshold
        if args.notification_success_response_time_threshold is not None and args.subcommand in ["add"]:
            error_type = "notification_success_response_time_threshold"
            error_threshold = args.notification_success_response_time_threshold

        notifications(args.subcommand, args.profile, args.notification_id, args.notification_channel,
                      args.notification_destination, error_type, error_threshold)

    # noinspection PyMethodMayBeStatic
    def team(self):
        parser = argparse.ArgumentParser(
            description='Team command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "change", "remove", "add", "get"])
        parser.add_argument('--member_email', dest="member_email", default=None
                            , help="Required parameter for subcommand [\"change\", \"remove\", \"add\"]")
        parser.add_argument('--member_role', dest="member_role", default=None
                            , choices=["Reader", "Editor", "Admin"]
                            , help="Required parameter for subcommand [\"change\", \"add\"]")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "change", "remove", "add", "get"]\n\n')
            parser.print_help()
            exit(1)
        if args.member_email is None and args.subcommand in ["change", "remove", "add"]:
            print('Please specify a member email using --member_email parameter')
            exit(1)
        if args.member_role is None and args.subcommand in ["change", "add"]:
            print('Please specify a member role using --member_role parameter')
            exit(1)
        team(args.subcommand, args.profile, args.member_email, args.member_role)

    # noinspection PyMethodMayBeStatic
    def results(self):
        parser = argparse.ArgumentParser(
            description='Results command system')
        parser.add_argument('subcommand', nargs='?', choices=["get"])
        parser.add_argument('--test_id', dest="test_id", default=None
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('--results_region', dest="results_region", default=None
                            , choices=["overall",
                                       "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
                                       "eu-central-1", "eu-west-2", "eu-west-3", "eu-west-1", "us-east-1", "us-east-2",
                                       "us-west-1", "us-west-2", "ca-central-1", "ap-south-1", "sa-east-1"]
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["get"]\n\n')
            parser.print_help()
            exit(1)
        if args.test_id is None and args.subcommand in ["get"]:
            print('Please specify a test ID using --test_id parameter')
            exit(1)
        if args.results_region is None and args.subcommand in ["get"]:
            print('Please specify a region to fetch results for using --results_region parameter')
            exit(1)
        results(args.subcommand, args.profile, args.test_id, args.results_region)

    # noinspection PyMethodMayBeStatic
    def raw_results(self):
        parser = argparse.ArgumentParser(
            description='Raw results command system')
        parser.add_argument('subcommand', nargs='?', choices=["get"])
        parser.add_argument('--test_id', dest="test_id", default=None
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('--results_region', dest="results_region", default=None
                            , choices=["overall",
                                       "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
                                       "eu-central-1", "eu-west-2", "eu-west-3", "eu-west-1", "us-east-1", "us-east-2",
                                       "us-west-1", "us-west-2", "ca-central-1", "ap-south-1", "sa-east-1"]
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('--results_type', dest="results_type", default="success"
                            , choices=["success", "failure"])
        parser.add_argument('--results_path', dest="results_path", default=None
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('--results_method', dest="results_method", default=None
                            , choices=["GET", "POST", "PATCH", "HEAD", "PUT", "DELETE", "OPTIONS"]
                            , help="Required parameter for subcommand [\"get\"]")
        parser.add_argument('--min_timestamp', dest="min_timestamp", default=None
                            , help="EPOCH TIME FORMAT -> Required parameter for subcommand [\"get\"]")
        parser.add_argument('--max_timestamp', dest="max_timestamp", default=None
                            , help="EPOCH TIME FORMAT -> Required parameter for subcommand [\"get\"]")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["get"]\n\n')
            parser.print_help()
            exit(1)
        if args.test_id is None and args.subcommand in ["get"]:
            print('Please specify a test ID using --test_id parameter')
            exit(1)
        if args.results_region is None and args.subcommand in ["get"]:
            print('Please specify a region to fetch results for using --results_region parameter')
            exit(1)
        if args.results_type is None and args.subcommand in ["get"]:
            print('Please specify a type of result using --results_type parameter')
            exit(1)
        if args.results_path is None and args.subcommand in ["get"]:
            print('Please specify a path within your workflow\'s test_id using --results_path parameter for which '
                  'you\'d like to get the raw results')
            exit(1)
        if args.results_method is None and args.subcommand in ["get"]:
            print('Please specify the method related to the path within your workflow\'s test_id using '
                  '--results_method '
                  'parameter for which you\'d like to get the raw results')
            exit(1)
        if args.min_timestamp is None and args.subcommand in ["get"]:
            print('Please specify the minimum timestamp in EPOCH TIME specific for your test_id  using '
                  '--min_timestamp '
                  'parameter for which you\'d like to get the raw results')
            exit(1)
        if args.max_timestamp is None and args.subcommand in ["get"]:
            print('Please specify the maximum timestamp in EPOCH TIME specific for your test_id  using '
                  '--max_timestamp '
                  'parameter for which you\'d like to get the raw results')
            exit(1)
        raw_results(args.subcommand, args.profile, args.test_id, args.results_region,
                    args.results_type, args.results_path, args.results_method,
                    args.min_timestamp, args.max_timestamp)

    # noinspection PyMethodMayBeStatic
    def tests(self):
        parser = argparse.ArgumentParser(
            description='Tests command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "add", "cancel", "remove",
                                                              "get", "preview-credits", "set-sharing"])
        parser.add_argument('--test_id', dest="test_id", default=None
                            , help="Required parameter for subcommand [\"cancel\", \"get\", "
                                   "\"set-sharing\", \"remove\"].\n"
                                   "Optional parameter for subcommand [\"list\"]")

        test_case = parser.add_mutually_exclusive_group(required=True)

        test_case.add_argument('--test_file', dest="test_file", type=argparse.FileType('r', encoding='UTF-8')
                               , default=None
                               , help="Required parameter for subcommand [\"add\", \"preview-credits\"]. \n"
                                      "You can specify --test_file or --template_id, but not both!")

        test_case.add_argument('--template_id', dest="template_id"
                               , default=None
                               , help="Required parameter for subcommand [\"add\", \"preview-credits\"]. \n"
                                      "You can specify --test_file or --template_id, but not both!")

        parser.add_argument('--test_public', dest="test_public", default=None, choices=["public", "private"]
                            , help="Required parameter for subcommand [\"set-sharing\"]")
        parser.add_argument('--test_name', dest="test_name", default=None
                            , help="Optional parameter for subcommand [\"add\", \"preview-credits\"].\n"
                                   "Use it to override the value for \"test_name\" in your test_file "
                                   "or to simply specify a name for the test")
        parser.add_argument('--wait_to_finish', dest="wait_to_finish", action="store_true", default=False
                            , help="Optional parameter for subcommand [\"add\"]\n"
                                   "Use it to set the CLI to wait for the test to finish before exiting.")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "add", "cancel", "remove", '
                  '"get", "preview-credits", "set-sharing"]\n\n')
            parser.print_help()
            exit(1)
        if args.test_id is None and args.subcommand in ["cancel", "get", "set-sharing", "remove"]:
            print('Please specify a test ID using --test_id parameter')
            exit(1)
        if args.test_public is None and args.subcommand in ["set-sharing"]:
            print('Please specify a value of either "public" or "private" for --test_public parameter')
            exit(1)
        if args.test_file is None and args.template_id is None and args.subcommand in ["add", "preview-credits"]:
            print('Please specify a test case using either --test_file or --template_id parameters\n')
            print('Keep in mind the CLI also supports piping stdout to it, as well as specifying a file path:')
            print("echo 'hello' | rungutan tests --test_file -")
            print("rungutan tests --test_file file.json")
            exit(1)
        tests(args.subcommand, args.profile, args.test_id, args.test_file, args.template_id,
              args.test_public, args.test_name, args.wait_to_finish)

    # noinspection PyMethodMayBeStatic
    def templates(self):
        parser = argparse.ArgumentParser(
            description='Templates command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "add", "remove", "get"])
        parser.add_argument('--template_id', dest="template_id", default=None
                            , help="Required parameter for subcommand [\"remove\", \"get\"].\n"
                                   "Optional parameter for subcommand [\"list\"]")
        parser.add_argument('--test_file', dest="test_file", type=argparse.FileType('r', encoding='UTF-8')
                            , default=None
                            , help="Required parameter for subcommand [\"add\"]")
        parser.add_argument('--test_name', dest="test_name", default=None
                            , help="Optional parameter for subcommand [\"add\"].\n"
                                   "Use it to override the value for \"test_name\" in your test_file "
                                   "or to simply specify a name for the template")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "add", "remove", "get"]\n\n')
            parser.print_help()
            exit(1)
        if args.template_id is None and args.subcommand in ["remove", "get"]:
            print('Please specify a template ID using --template_id parameter')
            exit(1)
        if args.test_file is None and args.subcommand in ["add"]:
            print('Please specify a test file using --test_file parameter\n')
            print('Keep in mind the CLI also supports piping stdout to it, as well as specifying a file path:')
            print("echo 'hello' | rungutan templates --test_file -")
            print("rungutan templates --test_file file.json")
            exit(1)
        templates(args.subcommand, args.profile, args.template_id, args.test_file, args.test_name)

    # noinspection PyMethodMayBeStatic
    def crons(self):
        parser = argparse.ArgumentParser(
            description='Crons command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "add", "remove",
                                                              "get", "preview-credits", "set-status"])
        parser.add_argument('--cron_id', dest="cron_id", default=None
                            , help="Required parameter for subcommand [\"remove\", \"get\", \"set-status\"].\n"
                                   "Optional parameter for subcommand [\"list\"]")
        parser.add_argument('--test_file', dest="test_file", type=argparse.FileType('r', encoding='UTF-8')
                            , default=None
                            , help="Required parameter for subcommand [\"add\", \"preview-credits\"]")
        parser.add_argument('--cron_enabled', dest="cron_enabled", default=None
                            , choices=["true", "false"]
                            , help="Required parameter for subcommand [\"set-status\"]")
        parser.add_argument('--test_name', dest="test_name", default=None
                            , help="Optional parameter for subcommand [\"add\", \"preview-credits\"].\n"
                                   "Use it to override or specify a name for the test")
        parser.add_argument('--schedule_type', dest="schedule_type", default=None
                            , choices=["DAILY", "WEEKLY", "MONTHLY"]
                            , help="Required parameter for subcommand [\"add\"]")
        parser.add_argument('--schedule_hour', dest="schedule_hour", default=None
                            , help="Required parameter for subcommand [\"add\"]")
        parser.add_argument('--schedule_minute', dest="schedule_minute", default=None
                            , help="Required parameter for subcommand [\"add\"]")
        parser.add_argument('--schedule_weekday', dest="schedule_weekday", default=None
                            , choices=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                            , help="Required parameter for subcommand [\"add\"] when the value of "
                                   "--schedule_type is set  to WEEKLY.")
        parser.add_argument('--schedule_day_of_month', dest="schedule_day_of_month", default=None
                            , help="Required parameter for subcommand [\"add\"] when the value of "
                                   "--schedule_type is set  to MONTHLY.")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "add", "remove", '
                  '"get", "preview-credits", "set-status"]\n\n')
            parser.print_help()
            exit(1)
        if args.cron_id is None and args.subcommand in ["remove", "get", "set-status"]:
            print('Please specify a cron ID using --cron_id parameter')
            exit(1)
        if args.cron_enabled is None and args.subcommand in ["set-status"]:
            print('Please specify a value of either "true" or "false" for --cron_enabled parameter')
            exit(1)
        if args.test_file is None and args.subcommand in ["add", "preview-credits"]:
            print('Please specify a test file using --test_file parameter\n')
            print('Keep in mind the CLI also supports piping stdout to it, as well as specifying a file path:')
            print("echo 'hello' | rungutan --test_file -")
            print("rungutan --test_file file.json")
            exit(1)
        if args.schedule_type is None and args.subcommand in ["add"]:
            print('Please specify a value for the schedule type using --schedule_type parameter\n')
            print('Accepted values are:')
            print('* DAILY')
            print('* WEEKLY')
            print('* MONTHLY')
            exit(1)
        if args.schedule_hour is None and args.subcommand in ["add"]:
            print('Please specify a value for the schedule hour using --schedule_hour parameter\n')
            print('Accepted values are -> any integer between 0 and 23')
            exit(1)
        if args.schedule_minute is None and args.subcommand in ["add"]:
            print('Please specify a value for the schedule minute using --schedule_minute parameter\n')
            print('Accepted values are -> any integer between 0 and 59')
            exit(1)
        crons(args.subcommand, args.profile, args.cron_id, args.test_file,
              args.cron_enabled, args.test_name, args.schedule_type, args.schedule_hour,
              args.schedule_minute, args.schedule_weekday, args.schedule_day_of_month)

    # noinspection PyMethodMayBeStatic
    def vault(self):
        parser = argparse.ArgumentParser(
            description='Vault command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "remove", "add", "get", "edit"])
        parser.add_argument('--vault_id', dest="vault_id", default=None
                            , help="Required parameter for subcommand [\"remove\", \"get\", \"edit\"]. \n"
                                   "Optional parameter for subcommand [\"list\"].")
        parser.add_argument('--key_storage_type', dest="key_storage_type", default=None
                            , choices=["SENSITIVE", "PLAINTEXT"]
                            , help="Required parameter for subcommand [\"add\", \"edit\"]")
        parser.add_argument('--key_name', dest="key_name", default=None
                            , help="Required parameter for subcommand [\"add\", \"edit\"]")
        parser.add_argument('--key_value', dest="key_value", default=None
                            , help="Required parameter for subcommand [\"add\", \"edit\"]")
        parser.add_argument('-p', '--profile', dest='profile', default='default'
                            , help='The profile you\'ll be using.\n'
                                   'If not specified, the "default" profile will be used. \n'
                                   'If no profiles are defined, the following env variables will be checked:\n'
                                   '* {}\n'
                                   '* {}'.format(os_env_team_id(), os_env_api_key()))

        args = parser.parse_args(sys.argv[2:])
        if args.subcommand is None:
            print('A subcommand from list must be supplied ["list", "remove", "add", "get", "edit"]\n\n')
            parser.print_help()
            exit(1)
        if args.vault_id is None and args.subcommand in ["remove", "get", "edit"]:
            print('Please specify a vault id using --vault_id parameter')
            exit(1)
        if args.key_storage_type is None and args.subcommand in ["add", "edit"]:
            print('Please specify a storage type using --key_storage_type parameter')
            exit(1)
        if args.key_name is None and args.subcommand in ["add", "edit"]:
            print('Please specify a key name using --key_name parameter')
            exit(1)
        if args.key_value is None and args.subcommand in ["add", "edit"]:
            print('Please specify a key value using --key_value parameter')
            exit(1)

        vault(args.subcommand, args.profile, args.vault_id, args.key_storage_type, args.key_name, args.key_value)

def main():
    RungutanCLI()


if __name__ == '__main__':
    RungutanCLI()
