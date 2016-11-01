import os


def get_snapshots(rsnapshot_root):
    snapshots = os.listdir(rsnapshot_root)
    return snapshots
