What is borg-import?
====================

borg-import converts backups made with other backup software into the format used by `BorgBackup <https://github.com/borgbackup/borg>`_.

See ``borg-import -h`` for more information.
Quick Start (Beginner Guide)
===========================

This section helps new users quickly install and use borg-import.

Installation
------------

1. Install BorgBackup:

   On macOS (using Homebrew):

   ``brew install borgbackup``

2. Clone borg-import and install:

   ``git clone https://github.com/borgbackup/borg-import.git``
   ``cd borg-import``
   ``python3 -m venv .venv``
   ``source .venv/bin/activate``
   ``pip install -e .``

Basic Usage Example
-------------------

Import backups from rsnapshot:

``borg-import rsnapshot /path/to/snapshots /path/to/borg-repo``

Get help for any command:

``borg-import -h``

Potential advantages over doing it manually
===========================================

Note: There are different importers, and some may not support all features.

- Automation: less manual work; import many backups into a Borg repository with one command.
- Automatically constructs the Borg archive name from the provided input and the discovered timestamp.
- Sets the Borg archive creation timestamp to the correct historical date and time.
- Temporarily moves the source directory so Borg's files cache can speed up ``borg create``.

Currently supported import formats
==================================

`BorgBackup <https://github.com/borgbackup/borg>`_
--------------------------------------------------

Imports archives from an existing Borg repository into a new one.
This is useful when a Borg repository needs to be rebuilt (e.g., if
your Borg key and passphrase were compromised).

Usage: ``borg-import borg SOURCE_REPOSITORY DESTINATION_REPOSITORY``

See ``borg-import borg -h`` for help.

`rsnapshot <https://github.com/rsnapshot/rsnapshot>`_
-----------------------------------------------------

Usage: ``borg-import rsnapshot SNAPSHOT_ROOT BORG_REPOSITORY``

See ``borg-import rsnapshot -h`` for help.

Simple rsync with hard links
----------------------------

Assumes one folder per archive, with changes being tracked based on last modification time (mtime).

Usage: ``borg-import rsynchl RSYNC_ROOT BORG_REPOSITORY``

See ``borg-import rsynchl -h`` for help.

`rsync-time-backup <https://github.com/laurent22/rsync-time-backup>`_
---------------------------------------------------------------------

Similar to ``rsynchl``, except with timestamp extraction optimized for ``rsync-time-backup`` folder names.

Usage: ``borg-import rsync_tmbackup --prefix=foo- RSYNC_ROOT BORG_REPOSITORY``

See ``borg-import rsync_tmbackup -h`` for help.

Backup tools based on rsync with hard links
-------------------------------------------

borg-import should, in principle, be able to import backups from any backup tool that is
based on rsync with hard links, provided the tool matches the assumptions listed above for simple
rsync.

* `backintime <https://github.com/bit-team/backintime>`_

* others?
