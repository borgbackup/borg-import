What is borg-import?
====================

Scripts to imports backups from other backup software into `BorgBackup <https://github.com/borgbackup/borg>` 's archive format.

`BorgWeb <https://borgweb.readthedocs.io/>`

See ``borg-import -h`` for general help.

Currently supported imports
===========================

rsnapshot
---------

Usage ``borg-import rsnapshot SNAPSHOT_ROOT BORG_REPOSITORY``.

See ``borg-import rsnapshot -h`` for help.

Simple rsync with hard links
----------------------------

Assumes one folder per archive, using folder mtime

Usage ``borg-import rsynchl RSYNC_ROOT BORG_REPOSITORY``

See ``borg-import rsynchl -h`` for help.

Backup tools based on rsync with hard links
-------------------------------------------

Requires the tool match the assumptions listed for plain rsync with hard links

* backintime

* others?
