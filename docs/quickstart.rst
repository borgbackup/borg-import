.. include:: global.rst.inc
.. highlight:: bash
.. _quickstart:

Quickstart
==========

This guide will get you started with borg-import.

Getting started quickly
-----------------------

If you just want to try borg-import with minimal setup:

::

    git clone https://github.com/borgbackup/borg-import.git
    cd borg-import
    python -m venv env
    source env/bin/activate
    pip install -e .
    borg-import --help

Import rsync snapshots
----------------------

For example, if an rsync-with-hard-links backup stores one snapshot per
directory::

    /srv/rsync-backups/
    |-- snapshot-2026-08-28/
    `-- snapshot-2026-08-29/

first initialize the destination repository, then import the snapshots::

    borg init --encryption=repokey /srv/borg-repository
    borg-import rsynchl /srv/rsync-backups /srv/borg-repository

The repository path must be absolute (or a remote repository specification).
``borg-import`` creates one archive per snapshot directory, using the directory
name as the archive name and its modification time as the archive timestamp.
Confirm the imported archives with::

    borg list --short /srv/borg-repository

During an import, each snapshot directory is temporarily renamed within the
snapshot root so Borg's files cache can recognize unchanged files efficiently.
The directory is moved back even if ``borg create`` fails. Test with a copy of
your backup first, and make sure the destination has enough free space before
importing a large backup set.
