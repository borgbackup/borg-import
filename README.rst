What is borg-import?
====================

borg-import imports backups from other backup software into BorgBackup's archive format.

See ``borg-import -h`` for general help.

Currently supported imports
===========================

rsnapshot
---------

```
borg-import rsnapshot SNAPSHOT_ROOT BORG_REPOSITORY
```

See ``borg-import rsnapshot -h`` for help.

Simple rsync with hard links
----------------------------

Assumes one folder per archive, using folder mtime

```
borg-import rsynchl RSYNC_ROOT BORG_REPOSITORY
```

See ``borg-import rsynchl -h`` for help.

Backup tools based on rsync with hard links
-------------------------------------------

Requires the tool match the assumptions listed for plain rsync with hard links

* backintime

* others?
