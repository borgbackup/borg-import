__version__ = "0.1.0"

import argparse
from . import rsnapshots

parser = argparse.ArgumentParser()
parser.add_argument("--rsnapshot-root", help="Path to saved rsnapshots")
args = parser.parse_args()


def main():
    if args.rsnapshot_root:
        rsnapshot_root = args.rsnapshot_root
        for rsnapshot in rsnapshots.GetSnapshots(rsnapshot_root):
            print(rsnapshot)


if __name__ == "__main__":
    main()
