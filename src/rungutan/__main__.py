import argparse
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from rungutan.configure import *
from rungutan.config import *
from rungutan.domain import *
from rungutan.team import *
from rungutan.tests import *


class RungutanCLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Rungutan CLI utility for interacting with https://rungutan.com',
            usage='''rungutan <command> [<args>]

To see help text, you can run:
    rungutan help
    rungutan configure --help
    rungutan domain --help
    rungutan team --help
    rungutan tests --help
    rungutan crons --help
    rungutan results --help
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
    def domain(self):
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
        domain(args.subcommand, args.profile, args.domain_name)

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
    def tests(self):
        parser = argparse.ArgumentParser(
            description='Tests command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "add", "cancel",
                                                              "get", "preview-credits", "set-sharing"])
        parser.add_argument('--test_id', dest="test_id", default=None
                            , help="Required parameter for subcommand [\"cancel\", \"get\", \"set-sharing\"]\n"
                                   "Optional parameter for subcommand [\"list\"]")
        parser.add_argument('--test_file', dest="test_file", type=argparse.FileType('r', encoding='UTF-8')
                            , default=None
                            , help="Required parameter for subcommand [\"add\", \"preview-credits\"]")
        parser.add_argument('--test_public', dest="test_public", default=None, choices=["public", "private"]
                            , help="Required parameter for subcommand [\"set-sharing\"]")
        parser.add_argument('--test_name', dest="test_name", default=None
                            , help="Optional parameter for subcommand [\"add\", \"preview-credits\"]\n"
                                   "Use it to override or specify a name for the test")
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
            print('A subcommand from list must be supplied ["list", "add", "cancel", '
                  '"get", "preview-credits", "set-sharing"]\n\n')
            parser.print_help()
            exit(1)
        if args.test_id is None and args.subcommand in ["cancel", "get", "set-sharing"]:
            print('Please specify a test ID using --test_id parameter')
            exit(1)
        if args.test_public is None and args.subcommand in ["set-sharing"]:
            print('Please specify a value of either "public" or "private" for --test_public parameter')
            exit(1)
        if args.test_file is None and args.subcommand in ["add", "preview-credits"]:
            print('Please specify a test file using --test_file parameter\n')
            print('Keep in mind the CLI also supports piping stdout to it, as well as specifying a file path:')
            print("echo 'hello' | rungutan --test_file -")
            print("rungutan --test_file file.json")
            exit(1)
        tests(args.subcommand, args.profile, args.test_id, args.test_file,
              args.test_public, args.test_name, args.wait_to_finish)

    # noinspection PyMethodMayBeStatic
    def crons(self):
        parser = argparse.ArgumentParser(
            description='Crons command system')
        parser.add_argument('subcommand', nargs='?', choices=["list", "add", "cancel",
                                                              "get", "preview-credits", "set-sharing"])
        parser.add_argument('--test_id', dest="test_id", default=None
                            , help="Required parameter for subcommand [\"cancel\", \"get\", \"set-sharing\"]\n"
                                   "Optional parameter for subcommand [\"list\"]")
        parser.add_argument('--test_file', dest="test_file", type=argparse.FileType('r', encoding='UTF-8')
                            , default=None
                            , help="Required parameter for subcommand [\"add\", \"preview-credits\"]")
        parser.add_argument('--test_public', dest="test_public", default=None, choices=["public", "private"]
                            , help="Required parameter for subcommand [\"set-sharing\"]")
        parser.add_argument('--test_name', dest="test_name", default=None
                            , help="Optional parameter for subcommand [\"add\", \"preview-credits\"]\n"
                                   "Use it to override or specify a name for the test")
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
            print('A subcommand from list must be supplied ["list", "add", "cancel", '
                  '"get", "preview-credits", "set-sharing"]\n\n')
            parser.print_help()
            exit(1)
        if args.test_id is None and args.subcommand in ["cancel", "get", "set-sharing"]:
            print('Please specify a test ID using --test_id parameter')
            exit(1)
        if args.test_public is None and args.subcommand in ["set-sharing"]:
            print('Please specify a value of either "public" or "private" for --test_public parameter')
            exit(1)
        if args.test_file is None and args.subcommand in ["add", "preview-credits"]:
            print('Please specify a test file using --test_file parameter\n')
            print('Keep in mind the CLI also supports piping stdout to it, as well as specifying a file path:')
            print("echo 'hello' | rungutan --test_file -")
            print("rungutan --test_file file.json")
            exit(1)
        tests(args.subcommand, args.profile, args.test_id, args.test_file,
              args.test_public, args.test_name, args.wait_to_finish)


if __name__ == '__main__':
    RungutanCLI()
