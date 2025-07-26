.. include:: global.rst.inc
.. _quickstart:

Quick Start
===========

This chapter will get you started with Borg-Import.

Prerequisites
-------------

Before using borg-import, you need:

1. **BorgBackup installed**: borg-import requires the ``borg`` command to be available in your PATH.
    Install it following the `BorgBackup installation guide <https://borgbackup.readthedocs.io/en/stable/installation.html>`_.

2. **Python 3.9 or newer**: borg-import is written in Python and requires a modern Python version.

3. **Sufficient disk space**: Import operations may require temporary space for intermediate processing.

Basic Usage Pattern
-------------------

All borg-import commands follow this general pattern::

    borg-import <IMPORTER> [OPTIONS] <SOURCE> <DESTINATION_REPOSITORY>

Where:

- ``<IMPORTER>`` is one of: ``borg``, ``rsnapshot``, ``rsynchl``, or ``rsync_tmbackup``
- ``<SOURCE>`` is the path to your existing backup directory or repository
- ``<DESTINATION_REPOSITORY>`` is the BorgBackup repository where archives will be imported

**Important**: Always use absolute paths or SSH URLs for repositories to avoid issues during import.

Quick Examples
--------------

**Import from rsnapshot backups**::

    # Create a new Borg repository first
    borg init --encryption=repokey /path/to/new/borg/repo
    
    # Import rsnapshot backups
    borg-import rsnapshot /path/to/rsnapshot/root /path/to/new/borg/repo

**Import from rsync+hardlinks backups**::

    # Create a new Borg repository first
    borg init --encryption=repokey /path/to/new/borg/repo
    
    # Import rsync backups
    borg-import rsynchl /path/to/rsync/backups /path/to/new/borg/repo

**Import from rsync-time-backup**::

    # Requires a prefix for archive naming
    borg-import rsync_tmbackup --prefix=mybackup- /path/to/rsync/backups /path/to/new/borg/repo

**Import from another Borg repository**::

    # Useful for rebuilding or migrating Borg repositories
    borg-import borg /path/to/old/borg/repo /path/to/new/borg/repo

Common Options
--------------

**Add prefix to archive names**::

    borg-import rsnapshot --prefix=imported- /source /destination

**Pass additional options to borg create**::

    borg-import rsynchl -o="--compression lz4" /source /destination

**Debug mode for troubleshooting**::

    borg-import --debug rsnapshot /source /destination

How It Works
------------

borg-import uses a smart approach to preserve Borg's file cache efficiency:

1. **Temporary relocation**: Source directories are temporarily moved to a common name (``borg-import-dir``)
2. **Archive creation**: Borg creates archives from this temporary location
3. **Restoration**: Original directories are moved back to their original locations
4. **Timestamp preservation**: Original backup timestamps are preserved in Borg archives

This process ensures that Borg's deduplication and file cache work optimally across imports.

Safety Features
---------------

- **Non-destructive**: Original backup structures are preserved
- **Resume capability**: If interrupted, the process can be safely restarted
- **Duplicate detection**: Archives already present in the destination are automatically skipped
- **Journal tracking**: A ``.snapshot`` file tracks the current operation for recovery

Getting Help
------------

For detailed help on any importer::

    borg-import <IMPORTER> -h

For example::

    borg-import rsnapshot -h
    borg-import borg -h

Common Issues
-------------

**"borg command not found"**
    Install BorgBackup first. See the `installation guide <https://borgbackup.readthedocs.io/en/stable/installation.html>`_.

**"borg-import-dir exists. Cannot continue"**
    A previous import was interrupted. Check the directory and ``.snapshot`` file to understand what happened, then manually clean up if safe to do so.

**Permission errors**
    Ensure you have read access to source backups and write access to the destination repository.

**Out of space**
    Some importers (especially ``borg``) require substantial temporary space. Ensure adequate free space in the working directory.

Next Steps
----------

- Read the detailed documentation for your specific backup format
- Consider setting up automated backups with your new Borg repository
- Learn about Borg's powerful features like mounting, pruning, and compression options
