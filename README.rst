What is borg-import?
====================

borg-import converts backups made with other backup software into the format used by `BorgBackup <https://github.com/borgbackup/borg>`_.

See ``borg-import -h`` for more information.

Currently supported import formats
==================================

`rsnapshot <https://github.com/rsnapshot/rsnapshot>`_
-----------------------------------------------------

Usage: ``borg-import rsnapshot SNAPSHOT_ROOT BORG_REPOSITORY``

See ``borg-import rsnapshot -h`` for help.

Simple rsync with hard links
----------------------------

Assumes one folder per archive, with changes being tracked based on last modification time (mtime).

Usage: ``borg-import rsynchl RSYNC_ROOT BORG_REPOSITORY``

See ``borg-import rsynchl -h`` for help.

Backup tools based on rsync with hard links
-------------------------------------------

borg-import should, in principle, be able to import backups from any backup tool that is
based on rsync with hard links. This requires that the tool matches the assumptions listed above for simple
rsync.

* `backintime <https://github.com/bit-team/backintime>`_

* others?

Planned
=======

Complex rsync with hard links (e.g. multiple hosts, separate backup time).
