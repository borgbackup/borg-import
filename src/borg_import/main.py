import argparse
import logging
import shutil
import sys

from .rsnapshots import get_snapshots

log = logging.getLogger(__name__)


def main():
    if not shutil.which('borg'):
        print('Borg does not seem to be installed. Please install Borg first.')
        print('See instructions at https://borgbackup.readthedocs.io/en/stable/installation.html')
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--rsnapshot-root", help="Path to rsnapshot root directory")

    parser.set_defaults(log_level=logging.WARNING)
    parser.add_argument("--debug", action='store_const', dest='log_level', const=logging.DEBUG)

    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)

    if args.rsnapshot_root:
        for rsnapshot in get_snapshots(args.rsnapshot_root):
            print(rsnapshot)


if __name__ == "__main__":
    sys.exit(main())
