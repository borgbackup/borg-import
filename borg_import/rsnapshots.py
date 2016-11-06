import os


def get_snapshots(rsnapshot_root):
    """Get all snapshot directories within the rsnapshot root directory."""
    snapshots = os.listdir(rsnapshot_root)
    return snapshots
