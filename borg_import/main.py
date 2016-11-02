__version__ = "0.1.0"

import argparse
from . import rsnapshots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rsnapshot-root", help="Path to saved rsnapshots")
    args = parser.parse_args()

    if args.rsnapshot_root:
        rsnapshot_root = args.rsnapshot_root
        for rsnapshot in rsnapshots.get_snapshots(rsnapshot_root):
            print(rsnapshot)


if __name__ == "__main__":
    main()
