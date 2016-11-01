import os

def GetSnapshots(rsnapshot_root):
    snapshots = os.listdir(rsnapshot_root)
    return snapshots
