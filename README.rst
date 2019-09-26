What is borg-import?
====================

A set of scripts to import from other backup software into the archive format used by `BorgBackup <https://github.com/borgbackup/borg>`_.

See ``borg-import -h`` for general help.

Currently supported imports
===========================

`rsnapshot <https://github.com/rsnapshot/rsnapshot>`_
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

* `backintime <https://github.com/bit-team/backintime>`_

* others?

Planned
=======

Complex rsync with hard links (e.g. multiple hosts, separate backup time).
