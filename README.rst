What is borg-import?
====================

borg-import can import backups from some other backup software, currently supported are:

- rsnapshot
- simple rsync+hardlinks (One folder per archive, using folder mtime)
- planned: complex rsync+hardlinks (e.g. Multiple hosts, separate backup time)

See ``borg-import -h`` for more information.
