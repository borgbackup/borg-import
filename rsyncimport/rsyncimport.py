__version__ = "0.1.0"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
args = parser.parse_args()


def main():
    # print("Executing rsyncimport version", __version__)
    if args.verbose:
        print(args.verbose)