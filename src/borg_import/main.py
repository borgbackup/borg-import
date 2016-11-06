import argparse

from .rsnapshots import get_snapshots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rsnapshot-root", help="Path to rsnapshot root directory")
    args = parser.parse_args()

    if args.rsnapshot_root:
        for rsnapshot in get_snapshots(args.rsnapshot_root):
            print(rsnapshot)


if __name__ == "__main__":
    main()
