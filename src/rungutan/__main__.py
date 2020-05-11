import argparse
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from rungutan.configure import configure


class RungutanCLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Rungutan CLI utility for interacting with https://rungutan.com',
            usage='''rungutan <command> [<args>]

To see help text, you can run:
    rungutan help
    rungutan <command> help
    rungutan <command> <subcommand> help
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


if __name__ == '__main__':
    RungutanCLI()
