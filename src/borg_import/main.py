import argparse
import logging
import shutil
import shlex
import subprocess
import sys
import textwrap
from pathlib import Path

from .rsnapshots import get_snapshots
from .rsynchl import get_rsyncsnapshots

log = logging.getLogger(__name__)


def borg_import(args, archive_name, path, timestamp=None):
    borg_cmdline = ['borg', 'create']
    if timestamp:
        borg_cmdline += '--timestamp', timestamp.isoformat()
    if args.create_options:
        borg_cmdline += args.create_options.split()

    repository = repo_resolve(args.repository)
    location = '{}::{}'.format(repository, archive_name)
    borg_cmdline.append(location)
    borg_cmdline.append('.')

    log.debug('Borg command line: %r', borg_cmdline)
    log.debug('Borg working directory: %s', path)
    try:
        subprocess.check_call(borg_cmdline, cwd=str(path))
    except subprocess.CalledProcessError as cpe:
        if cpe.returncode != 1:
            raise
        log.debug('Borg exited with a warning (being quiet about it since Borg spoke already)')


def list_borg_archives(args):
    borg_cmdline = ['borg', 'list', '--short']
    repository = repo_resolve(args.repository)
    borg_cmdline.append(str(repository))
    return subprocess.check_output(borg_cmdline).decode().splitlines()


def repo_resolve(repository):
    if '@' in str(repository):
        # looks like a remote repo - don't try and resolve the path
        return repository
    else:
        return repository.resolve()


class Importer:
    name = 'name-of-command'
    description = 'descriptive description describing this importer'
    epilog = 'epilog-y epilog epiloging about this importer (docstringy for multiple lines)'

    def populate_parser(self, parser):
        """
        Add arguments to argparse *parser*.

        Specify the callback for the importer like so::

            parser.set_defaults(function=self.import_something)

        Then you can define *import_something* like this in the class::

            def import_something(self, args):
                ...  # do something!
        """


class rsnapshotImporter(Importer):
    name = 'rsnapshot'
    description = 'import rsnapshot backups'
    epilog = """
    Imports from rsnapshot backup sets by renaming each snapshot
    to a common name independent of the snapshot (and the backup set),
    which allows the Borg files cache to work with maximum efficiency.

    The directory is called "borg-import-dir" inside the rsnapshot root,
    and borg-import will note which snapshot is currently located there
    in a file called "borg-import-dir.snapshot" besides it, in case
    things go wrong.

    Otherwise nothing in the rsnapshot root is modified, and neither
    are the contents of the snapshots.
    """

    def populate_parser(self, parser):
        parser.add_argument('--backup-set', help='Only consider given backup set (can be given multiple times).',
                            action='append', dest='backup_sets')
        parser.add_argument('rsnapshot_root', metavar='RSNAPSHOT_ROOT',
                            help='Path to rsnapshot root directory', type=Path)
        # TODO: support the full wealth of borg possibilities
        parser.add_argument('repository', metavar='BORG_REPOSITORY', help='Borg repository', type=Path)
        parser.set_defaults(function=self.import_rsnapshot)

    def import_rsnapshot(self, args):
        existing_archives = list_borg_archives(args)

        import_path = args.rsnapshot_root / 'borg-import-dir'
        import_journal = args.rsnapshot_root / 'borg-import-dir.snapshot'

        if import_path.exists():
            print('{} exists. Cannot continue.'.format(import_path))
            return 1

        for rsnapshot in get_snapshots(args.rsnapshot_root):
            timestamp = rsnapshot['timestamp'].replace(microsecond=0)
            snapshot_original_path = rsnapshot['path']
            name = rsnapshot['name']
            archive_name = args.prefix + name

            if args.backup_sets and rsnapshot['backup_set'] not in args.backup_sets:
                print('Skipping (backup set is not selected):', name)
                continue

            if archive_name in existing_archives:
                print('Skipping (already exists in repository):', name)
                continue

            print('Importing {} (timestamp {}) '.format(name, timestamp), end='')
            if archive_name != name:
                print('as', archive_name)
            else:
                print()
            log.debug('  Moving {} -> {}'.format(rsnapshot['path'], import_path))

            # We move the snapshots to import_path so that the files cache in Borg can work effectively.

            with import_journal.open('w') as fd:
                fd.write('Current snapshot: %s\n' % rsnapshot['name'])
                fd.write('Original path: %s\n' % snapshot_original_path)

            snapshot_original_path.rename(import_path)

            try:
                borg_import(args, archive_name, import_path, timestamp=timestamp)
            finally:
                log.debug('  Moving {} -> {}'.format(import_path, rsnapshot['path']))
                import_path.rename(snapshot_original_path)
                import_journal.unlink()


class rsynchlImporter(Importer):
    name = 'rsynchl'
    description = 'import rsync+hardlink backups'
    epilog = """
    Imports from rsync backup sets by renaming each snapshot to a common
    name independent of the snapshot, which allows the Borg files cache
    to work with maximum efficiency.

    An archive will be created for each folder in the rsync_root. The
    archive name will be the folder name and the archive timestamp will
    be the folder mtime. If the borg repository already contains an
    archive with the folder name, that folder will be skipped.

    The directory is called "borg-import-dir" inside the specified root,
    and borg-import will note which snapshot is currently located there
    in a file called "borg-import-dir.snapshot" besides it, in case
    things go wrong.

    Otherwise nothing in the rsync root is modified, and neither
    are the contents of the snapshots.
    """

    def populate_parser(self, parser):
        parser.add_argument('rsync_root', metavar='RSYNC_ROOT',
                            help='Path to root directory', type=Path)
        # TODO: support the full wealth of borg possibilities
        parser.add_argument('repository', metavar='BORG_REPOSITORY', help='Borg repository', type=Path)
        parser.set_defaults(function=self.import_rsynchl)

    def import_rsynchl(self, args):
        existing_archives = list_borg_archives(args)

        import_path = args.rsync_root / 'borg-import-dir'
        import_journal = args.rsync_root / 'borg-import-dir.snapshot'

        if import_path.exists():
            print('{} exists. Cannot continue.'.format(import_path))
            return 1

        for rsnapshot in get_rsyncsnapshots(args.rsync_root):
            timestamp = rsnapshot['timestamp'].replace(microsecond=0)
            snapshot_original_path = rsnapshot['path']
            name = rsnapshot['name']
            archive_name = args.prefix + name

            if archive_name in existing_archives:
                print('Skipping (already exists in repository):', name)
                continue

            print('Importing {} (timestamp {}) '.format(name, timestamp), end='')
            if archive_name != name:
                print('as', archive_name)
            else:
                print()
            log.debug('  Moving {} -> {}'.format(rsnapshot['path'], import_path))

            # We move the snapshots to import_path so that the files cache in Borg can work effectively.

            with import_journal.open('w') as fd:
                fd.write('Current snapshot: %s\n' % rsnapshot['name'])
                fd.write('Original path: %s\n' % snapshot_original_path)

            snapshot_original_path.rename(import_path)

            try:
                borg_import(args, archive_name, import_path, timestamp=timestamp)
            finally:
                log.debug('  Moving {} -> {}'.format(import_path, rsnapshot['path']))
                import_path.rename(snapshot_original_path)
                import_journal.unlink()


def build_parser():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_group = common_parser.add_argument_group('Common options')

    common_group.add_argument("--create-options", "-o",
                              help="Additional borg create options "
                                   "(note: Use -o=\"--foo --bar\" syntax to avoid parser confusion).")
    common_group.add_argument("--prefix", help="Add prefix to imported archive names", default='')

    common_group.add_argument("--debug", action='store_const', dest='log_level', const=logging.DEBUG,
                              help='Display debug/trace messages.')

    parser = argparse.ArgumentParser(description='Import existing backups from other software to Borg')
    parser.set_defaults(log_level=logging.WARNING)

    subparsers = parser.add_subparsers()

    for importer_class in Importer.__subclasses__():
        importer = importer_class()
        subparser = subparsers.add_parser(importer.name,
                                          help=importer.description, epilog=textwrap.dedent(importer.epilog),
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          parents=[common_parser])
        importer.populate_parser(subparser)

    return parser


def main():
    if not shutil.which('borg'):
        print('The \'borg\' command can\'t be found in the PATH. Please correctly install borgbackup first.')
        print('See instructions at https://borgbackup.readthedocs.io/en/stable/installation.html')
        return 1

    parser = build_parser()
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format='%(message)s')

    if 'function' not in args:
        return parser.print_help()
    try:
        return args.function(args)
    except subprocess.CalledProcessError as cpe:
        print('{} invocation failed with status {}'.format(cpe.cmd[0], cpe.returncode))
        print('Command line was:', *[shlex.quote(s) for s in cpe.cmd])
        return cpe.returncode


if __name__ == "__main__":
    sys.exit(main())
